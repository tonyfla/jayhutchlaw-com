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
 *   NOTIFY_EMAIL        recipient for the email fallback
 *   NOTIFY_FROM_EMAIL   verified sender for the email fallback
 *
 * Bindings:
 *   UPLOADS             private R2 bucket for citation attachments
 *   EMAIL               Cloudflare Email Service send binding
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
const MAX_REQUEST_BYTES = MAX_FILES * MAX_FILE_BYTES + 1024 * 1024;
const MIN_FILL_SECONDS = 3;
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/heic', 'image/webp', 'application/pdf'];

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
  });

const clean = (v, max = 2000) => String(v ?? '').trim().slice(0, max);

/* Email and phone rules, mirroring js/forms.js. The client copy is for
   feedback; this one is the rule, since anything can POST to this endpoint. */
const EMAIL_RE = /^[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*@[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+$/;

function validEmail(value) {
  if (!value || value.length > 254) return false;
  if (!EMAIL_RE.test(value)) return false;
  const at = value.lastIndexOf('@');
  if (value.slice(0, at).length > 64) return false;
  const tld = value.slice(at + 1).toLowerCase().split('.').pop();
  return /^[a-z]{2,24}$/.test(tld);
}

/* Returns the number in E.164 for Clio, or null if it is not a usable
   North American number. */
function normalisePhone(value) {
  let digits = String(value || '').replace(/\D/g, '');
  if (digits.length === 11 && digits.startsWith('1')) digits = digits.slice(1);
  if (digits.length !== 10) return null;

  const npa = digits.slice(0, 3);
  const nxx = digits.slice(3, 6);

  if (npa[0] < '2' || nxx[0] < '2') return null;
  if (npa[1] === '1' && npa[2] === '1') return null;   // N11 service codes
  if (nxx[1] === '1' && nxx[2] === '1') return null;
  if (/^(\d)\1{9}$/.test(digits)) return null;
  if (nxx === '555' && /^01\d\d$/.test(digits.slice(6))) return null;  // reserved for fiction

  return `+1${digits}`;
}

const bytesStartWith = (bytes, signature) =>
  signature.every((byte, index) => bytes[index] === byte);

async function detectedFileType(file) {
  const bytes = new Uint8Array(await file.slice(0, 32).arrayBuffer());
  if (bytesStartWith(bytes, [0xff, 0xd8, 0xff])) return 'image/jpeg';
  if (bytesStartWith(bytes, [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a])) return 'image/png';
  if (bytesStartWith(bytes, [0x25, 0x50, 0x44, 0x46, 0x2d])) return 'application/pdf';
  if (bytesStartWith(bytes, [0x52, 0x49, 0x46, 0x46]) && bytesStartWith(bytes.slice(8), [0x57, 0x45, 0x42, 0x50])) return 'image/webp';

  const brand = new TextDecoder().decode(bytes.slice(4, 12));
  if (/^ftyp(?:heic|heix|hevc|hevx|mif1|msf1)$/.test(brand)) return 'image/heic';
  return null;
}

async function sendFallbackEmail(env, lead, reason) {
  if (!env.EMAIL || !env.NOTIFY_EMAIL || !env.NOTIFY_FROM_EMAIL) return false;

  try {
    await env.EMAIL.send({
      to: env.NOTIFY_EMAIL,
      from: env.NOTIFY_FROM_EMAIL,
      replyTo: lead.email || undefined,
      subject: `Jay Hutch Law website lead - CRM delivery failed (${reason})`,
      text: [
        'A website lead could not be delivered to Clio Grow.',
        `Reason: ${reason}`,
        '',
        `Name: ${lead.first_name} ${lead.last_name}`,
        lead.email ? `Email: ${lead.email}` : '',
        lead.phone_number ? `Phone: ${lead.phone_number}` : '',
        '',
        lead.from_message,
      ].filter(Boolean).join('\n'),
    });
    return true;
  } catch (error) {
    console.error('Lead fallback email failed:', error?.code || 'unknown_error');
    return false;
  }
}

export async function onRequestPost({ request, env }) {
  const contentLength = Number(request.headers.get('content-length'));
  if (Number.isFinite(contentLength) && contentLength > MAX_REQUEST_BYTES) {
    return json({ ok: false, message: 'The submission is too large.' }, 413);
  }

  const origin = request.headers.get('origin');
  if (origin && origin !== new URL(request.url).origin) {
    return json({ ok: false, message: 'This submission is not allowed.' }, 403);
  }

  if (env.LEAD_RATE_LIMITER) {
    const visitor = request.headers.get('cf-connecting-ip') || 'unknown';
    const { success } = await env.LEAD_RATE_LIMITER.limit({ key: visitor });
    if (!success) return json({ ok: false, message: 'Please wait a moment before trying again.' }, 429);
  }

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

  if (clean(form.get('company'), 200)) {
    return json({ ok: false, message: 'Could not process the submission.' }, 422);
  }
  const elapsed = Number(form.get('_elapsed'));
  if (!Number.isFinite(elapsed) || elapsed < MIN_FILL_SECONDS || elapsed > 4 * 60 * 60) {
    return json({ ok: false, message: 'Please wait a moment and try again.' }, 422);
  }
  if (form.get('consent') !== 'yes') {
    return json({ ok: false, message: 'Consent to contact is required.' }, 422);
  }

  if (!firstName || !lastName) {
    return json({ ok: false, message: 'First and last name are required.' }, 422);
  }
  if (!email && !phone) {
    return json({ ok: false, message: 'An email address or phone number is required.' }, 422);
  }
  if (email && !validEmail(email)) {
    return json({ ok: false, message: 'That email address is not valid.' }, 422);
  }

  const phoneE164 = phone ? normalisePhone(phone) : null;
  if (phone && !phoneE164) {
    return json({ ok: false, message: 'That phone number is not a valid US number.' }, 422);
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
    const fileType = await detectedFileType(file);
    if (!fileType || !ALLOWED_TYPES.includes(fileType)) {
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
        httpMetadata: { contentType: fileType },
        customMetadata: { intake: 'citation' },
      });
      uploaded.push(key);
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
  if (phoneE164) lead.phone_number = phoneE164;   // E.164, as Clio's examples use

  const sourceId = MARKETING_SOURCE_IDS[(attribution.utm_source || '').toLowerCase()];
  if (sourceId) lead.marketing_source = { id: sourceId };
  if (Number.isInteger(matterTypeId)) lead.matter_type = { id: matterTypeId };
  if (env.CLIO_LOCATION_ID) lead.matter_location = { id: parseInt(env.CLIO_LOCATION_ID, 10) };

  /* --- Send -------------------------------------------------------------- */
  if (!env.CLIO_GROW_TOKEN) {
    const emailed = await sendFallbackEmail(env, lead, 'CRM credentials are not configured');
    console.error('Clio Grow is not configured; fallback email:', emailed ? 'sent' : 'unavailable');
    return json(
      emailed
        ? { ok: true, warnings: ['Our intake system is being connected. Your request was sent to the firm directly.'] }
        : { ok: false, message: 'The intake system is not connected yet. Please call 855-488-2452.' },
      emailed ? 200 : 503
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
  } catch {
    const emailed = await sendFallbackEmail(env, lead, 'Clio Grow could not be reached');
    console.error('Clio Grow request failed; fallback email:', emailed ? 'sent' : 'unavailable');
    return json(
      emailed
        ? { ok: true, warnings: ['Your request was sent to the firm directly.'] }
        : { ok: false, message: 'We could not reach our intake system. Please call 855-488-2452.' },
      emailed ? 200 : 502
    );
  }

  if (!response.ok) {
    const emailed = await sendFallbackEmail(env, lead, `Clio Grow returned HTTP ${response.status}`);
    console.error(`Clio Grow returned HTTP ${response.status}; fallback email:`, emailed ? 'sent' : 'unavailable');
    return json(
      emailed
        ? { ok: true, warnings: ['Your request was sent to the firm directly.'] }
        : { ok: false, message: 'We could not record your request. Please call 855-488-2452.' },
      emailed ? 200 : 502
    );
  }

  const created = await response.json().catch(() => ({}));
  return json({ ok: true, id: created?.data?.id ?? null, warnings: uploadErrors });
}
