/**
 * POST /api/lead — Cloudflare Pages Function
 *
 * Receives a website form submission, stores any attachments in R2, and
 * creates an Inbox Lead in Clio Grow.
 *
 * Clio Grow API v2:  POST https://api.clio.com/grow/inbox_leads
 *   required: first_name, last_name, from_message, referring_url, from_source
 *   optional: email, phone_number, marketing_source{id}, matter_type{id},
 *             matter_location{id}
 *
 * Environment (Cloudflare Pages → Settings → Environment variables):
 *   CLIO_GROW_TOKEN     secret. API token from the Clio developer portal.
 *   CLIO_REGION         optional: us | eu | au | ca   (default: us)
 *   CLIO_LOCATION_ID    optional: Grow location id for the Atlanta office
 *   NOTIFY_EMAIL        optional: fallback inbox if Clio rejects the lead
 *
 * Bindings:
 *   UPLOADS             R2 bucket for citation attachments
 *   PUBLIC_UPLOAD_BASE  public URL base for that bucket
 *
 * NOTE: the auth scheme below (Bearer) still needs confirming against a live
 * Clio developer-portal token — the public docs do not spell out the header.
 * If Clio returns 401 with a valid token, this is the first line to check.
 */

const REGION_HOSTS = {
  us: 'https://api.clio.com',
  eu: 'https://eu.api.clio.com',
  au: 'https://au.api.clio.com',
  ca: 'https://ca.api.clio.com',
};

/* utm_source value -> Clio Grow marketing source id.
   Fill these in from GET /grow/sources once the Clio account exists.
   Unmapped sources still create the lead; the campaign detail is preserved
   in the message body either way. */
const MARKETING_SOURCE_IDS = {
  // google:   0,
  // facebook: 0,
  // bing:     0,
  // referral: 0,
};

const MAX_FILES = 4;
const MAX_FILE_BYTES = 10 * 1024 * 1024;
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/heic', 'image/webp', 'application/pdf'];

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
  });

const clean = (v, max = 2000) => String(v ?? '').trim().slice(0, max);

export async function onRequestPost({ request, env }) {
  let form;
  try {
    form = await request.formData();
  } catch {
    return json({ ok: false, message: 'Could not read the submission.' }, 400);
  }

  /* --- Required fields ------------------------------------------------- */
  const firstName = clean(form.get('first_name'), 100);
  const lastName = clean(form.get('last_name'), 100);
  const email = clean(form.get('email'), 200);
  const phone = clean(form.get('phone'), 50);
  const message = clean(form.get('message'), 5000);

  if (!firstName || !lastName) {
    return json({ ok: false, message: 'First and last name are required.' }, 422);
  }
  if (!email && !phone) {
    return json({ ok: false, message: 'An email address or phone number is required.' }, 422);
  }
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
    return json({ ok: false, message: 'That email address is not valid.' }, 422);
  }

  /* --- Attribution ------------------------------------------------------ */
  let attribution = {};
  try {
    attribution = JSON.parse(form.get('_attribution') || '{}');
  } catch {
    /* malformed attribution must never block a real lead */
  }

  const pageUrl = clean(form.get('_page'), 500) || request.headers.get('referer') || 'https://www.jayhutchlaw.com/';
  const fromSource = clean(form.get('_source'), 100) || 'website';
  const matterTypeId = parseInt(form.get('_matter_type'), 10);

  /* --- Attachments ------------------------------------------------------ */
  const files = form.getAll('files').filter((f) => f && typeof f === 'object' && f.size > 0);
  const uploaded = [];
  const uploadErrors = [];

  if (files.length > MAX_FILES) {
    return json({ ok: false, message: `Please attach no more than ${MAX_FILES} files.` }, 422);
  }

  for (const file of files) {
    if (file.size > MAX_FILE_BYTES) {
      uploadErrors.push(`${file.name} exceeded the 10 MB limit and was not attached.`);
      continue;
    }
    if (file.type && !ALLOWED_TYPES.includes(file.type)) {
      uploadErrors.push(`${file.name} is not an accepted file type and was not attached.`);
      continue;
    }
    if (!env.UPLOADS) {
      uploadErrors.push('File storage is not configured; attachments were not saved.');
      break;
    }

    const safeName = file.name.replace(/[^a-zA-Z0-9._-]/g, '_').slice(-80);
    const key = `citations/${new Date().toISOString().slice(0, 10)}/${crypto.randomUUID()}-${safeName}`;

    try {
      await env.UPLOADS.put(key, file.stream(), {
        httpMetadata: { contentType: file.type || 'application/octet-stream' },
        customMetadata: { submittedBy: `${firstName} ${lastName}`, email, phone },
      });
      const base = (env.PUBLIC_UPLOAD_BASE || '').replace(/\/$/, '');
      uploaded.push(base ? `${base}/${key}` : key);
    } catch (err) {
      uploadErrors.push(`${file.name} could not be stored (${err.message}).`);
    }
  }

  /* --- Compose the message body ----------------------------------------
     Clio Grow's inbox_leads endpoint has no custom fields, so everything
     the intake team needs is packed into from_message as a readable block.
     --------------------------------------------------------------------- */
  const lines = [];
  if (message) lines.push(message, '');

  const detail = (label, value) => { if (value) lines.push(`${label}: ${value}`); };

  detail('Court date / details', clean(form.get('court_date'), 300));
  detail('Practice area', clean(form.get('practice_area'), 100));

  if (uploaded.length) {
    lines.push('', 'Attachments:');
    uploaded.forEach((url) => lines.push(`  ${url}`));
  }
  if (uploadErrors.length) {
    lines.push('', 'Attachment problems:');
    uploadErrors.forEach((e) => lines.push(`  ${e}`));
  }

  lines.push('', '--- Marketing attribution ---');
  detail('Submitted from', pageUrl);
  detail('Landing page', attribution.landing_page);
  detail('Referrer', attribution.referrer || '(direct)');
  detail('Campaign', attribution.utm_campaign);
  detail('Source / medium', [attribution.utm_source, attribution.utm_medium].filter(Boolean).join(' / '));
  detail('Term', attribution.utm_term);
  detail('Content', attribution.utm_content);
  detail('Google click id', attribution.gclid);
  detail('Meta click id', attribution.fbclid);
  detail('Consent to contact', form.get('consent') ? 'Yes' : 'Not given');
  detail('Submitted at', new Date().toISOString());

  /* --- Build the Clio Grow payload -------------------------------------- */
  const lead = {
    first_name: firstName,
    last_name: lastName,
    from_message: lines.join('\n').slice(0, 10000),
    referring_url: pageUrl,
    from_source: fromSource,
  };
  if (email) lead.email = email;
  if (phone) lead.phone_number = phone;

  const sourceId = MARKETING_SOURCE_IDS[(attribution.utm_source || '').toLowerCase()];
  if (sourceId) lead.marketing_source = { id: sourceId };
  if (Number.isInteger(matterTypeId)) lead.matter_type = { id: matterTypeId };
  if (env.CLIO_LOCATION_ID) lead.matter_location = { id: parseInt(env.CLIO_LOCATION_ID, 10) };

  /* --- Send -------------------------------------------------------------- */
  if (!env.CLIO_GROW_TOKEN) {
    // Not configured yet. Log it so nothing is lost during the build phase,
    // and tell the visitor the truth rather than showing a fake success.
    console.log('CLIO_GROW_TOKEN missing. Lead received:', JSON.stringify(lead));
    return json(
      { ok: false, message: 'The intake system is not connected yet. Please call 855-488-2452.' },
      503
    );
  }

  const host = REGION_HOSTS[(env.CLIO_REGION || 'us').toLowerCase()] || REGION_HOSTS.us;

  let response;
  try {
    response = await fetch(`${host}/grow/inbox_leads`, {
      method: 'POST',
      headers: {
        authorization: `Bearer ${env.CLIO_GROW_TOKEN}`,
        'content-type': 'application/json',
        accept: 'application/json',
      },
      body: JSON.stringify({ data: lead }),
    });
  } catch (err) {
    console.error('Clio Grow unreachable:', err.message, JSON.stringify(lead));
    return json({ ok: false, message: 'We could not reach our intake system. Please call 855-488-2452.' }, 502);
  }

  if (!response.ok) {
    const body = await response.text().catch(() => '');
    // Log the full lead so a CRM outage never silently loses a client.
    console.error(`Clio Grow ${response.status}: ${body}`, JSON.stringify(lead));
    return json({ ok: false, message: 'We could not record your request. Please call 855-488-2452.' }, 502);
  }

  const created = await response.json().catch(() => ({}));
  return json({ ok: true, id: created?.data?.id ?? null, warnings: uploadErrors });
}
