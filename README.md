# Jay Hutch Law

Marketing site for Jay Hutch Law (Atlanta, Georgia). Static HTML, CSS, and
JavaScript with no build step, deployed to **Cloudflare Pages**. Lead capture
runs through a Pages Function that creates an Inbox Lead in **Clio Grow**.

## Structure

```
index.html            single-page overview (hero, practice areas, firm, FAQ, form)
practice-areas/       hub + six deep pages, generated from tools/
attorney/             James Hutchins bio
resources/            guide hub + 3 open, indexed articles
upload-citation/      citation intake with file upload
privacy/  disclaimer/ legal pages — DRAFT, need attorney review
thank-you/            conversion page (noindex) — form success target
404.html
tools/                page generators (see below) — not deployed
css/styles.css        the whole design system, one file
js/site.js            nav, scroll reveal, current year
js/forms.js           attribution, validation, spam screening, submission
functions/api/lead.js Cloudflare Pages Function → Clio Grow inbox_leads
assets/               hero imagery, self-hosted fonts, favicon
marketing/            internal marketing repo — NOT deployed (see .cfignore)
marketing/ads/        social ad files, one folder per ad
_headers _redirects   Cloudflare configuration
robots.txt sitemap.xml
```

## Local preview

```bash
python3 tools/serve.py 8789
```

Serves directory-style URLs and sends `no-store`, so an edited stylesheet is
actually picked up on reload. `python3 -m http.server` caches aggressively and
will quietly show you stale CSS.

The static site works, but `/api/lead` will not — form submissions show their
error state. To exercise the function you need Wrangler:

```bash
npx wrangler pages dev .
```

Put local secrets in `.dev.vars` (gitignored):

```
CLIO_GROW_TOKEN=...
PUBLIC_UPLOAD_BASE=https://uploads.jayhutchlaw.com
```

## Deploying

1. Create the Cloudflare account and a Pages project connected to this repo.
2. Build command: none. Output directory: `/`.
3. Create the R2 bucket: `npx wrangler r2 bucket create jayhutchlaw-uploads`
4. Set environment variables in **Pages → Settings → Environment variables**:

   | Name | Type | Notes |
   |---|---|---|
   | `CLIO_GROW_TOKEN` | secret | from the Clio developer portal |
   | `CLIO_REGION` | plain | `us` |
   | `CLIO_LOCATION_ID` | plain | optional, Grow location id |
   | `PUBLIC_UPLOAD_BASE` | plain | public URL of the R2 bucket |

5. Bind the R2 bucket to `UPLOADS` in the Pages project settings.
6. Point DNS at Cloudflare. The existing Wix site stays live until this step,
   so there is no risky cutover.

## Clio Grow integration

`functions/api/lead.js` posts to `POST https://api.clio.com/grow/inbox_leads`.

Two things to finish once the Clio account exists:

- **Confirm the auth header.** The code sends `Authorization: Bearer <token>`.
  Clio's public docs do not state the scheme explicitly. If a valid token
  returns 401, this is the first thing to check.
- **Fill in `MARKETING_SOURCE_IDS`** in that file by calling
  `GET /grow/sources`. This maps `utm_source` values onto Clio Grow marketing
  sources so campaign attribution lands in the CRM automatically. Leads are
  still created without it; only the source tag is missing.

Attribution the site captures on every submission: UTM parameters, `gclid`,
`fbclid`, `msclkid`, first referrer, landing page, submitting page, and consent.
Clio Grow's endpoint has no custom fields, so these are written into
`from_message` as a readable block.

### Forms

Any form marked `data-lead-form` is wired automatically:

```html
<form data-lead-form data-source="website_consultation" data-matter-type="17">
```

`data-source` → Clio `from_source`, `data-matter-type` → Clio matter type id,
`data-redirect` → success URL (defaults to `/thank-you/`).

Spam is handled by a honeypot field plus a minimum fill time. No CAPTCHA —
CAPTCHAs measurably reduce law-firm form completion.

## Conventions worth knowing

- **Tap targets are 44px on mobile** for the phone link, footer links, and
  breadcrumbs. Calling is the primary conversion action; do not shrink these.
- **`--muted-light` is the floor for text colour.** Anything lighter fails AA.
- **`--gold` is decorative only.** `#b38a4d` is 3.4:1 on white and fails WCAG AA
  for text. Use `--gold-deep` for anything readable or clickable.
- **`--gold-deep` is reserved for calls to action.** Using it as a decorative
  fill weakens every CTA on the page.
- **The FAQ appears twice** — as markup and as `FAQPage` JSON-LD in the head.
  Edit both or the structured data goes stale.
- **A failed submission must never show success.** The previous version of this
  site faked it, which loses leads silently.
- **`--section-y`** is the single knob for vertical page rhythm.

## Regenerating pages

The sub-pages share their header, footer, breadcrumbs, CTA bands, and structured
data. Rather than editing that chrome in nine files, it lives in one template:

```bash
python3 tools/build_pages.py        # practice-areas hub + 6 deep pages
python3 tools/build_firm_pages.py   # attorney + upload-citation
python3 tools/build_resources.py    # resources hub + guides
python3 tools/build_legal.py        # privacy + disclaimer
```

Ad links (not part of the site build):

```bash
python3 tools/adlink.py dui-atlanta /practice-areas/dui-defense/
```

Practice-area copy lives in `tools/content.py`; guide copy in
`tools/resources.py`. **Edit the content there and
regenerate — hand edits to the generated `index.html` files will be overwritten.**
The generated HTML is committed and deploys as-is; Cloudflare runs no build step.

`index.html`, `thank-you/`, and `404.html` are hand-written and are not touched
by the generators. Legal copy lives in `tools/build_legal.py`.

## Still to do

- **Legal review.** Practice-area copy in `tools/content.py`, guides in
  `tools/resources.py`, and the privacy policy and disclaimer in
  `tools/build_legal.py` are all DRAFT. Open questions for counsel are listed
  in `marketing/copy/legal-review-notes.md`.
- **Every page in `tools/content.py` is marked DRAFT.** Georgia code references (O.C.G.A. § 9-3-33, § 51-12-33,
  § 51-3-1, § 40-6-189) are cited so they can be checked quickly.
- Decide whether to switch the resource gate on (see below).
- Attorney review of `privacy/` and `disclaimer/` — **launch blockers.**
- Logo, favicon, and the attorney portrait were taken from the existing Wix
  site; masters are in `marketing/brand/source/`. Confirm they are the versions
  the firm wants used.
- Convert the hero to WebP — no encoder was available on the build machine, so
  it ships as JPEG (376 KB desktop / 128 KB mobile). WebP would roughly halve
  both; it is the largest remaining performance item.
- Confirm bar admissions and any credentials worth listing.
- Google Business Profile using the exact NAP block in
  `marketing/copy/firm-boilerplate.md`.

## The resource gate

`/resources/` is currently **open** — guides are free to read, no form.

To capture leads from them later, set `GATE_ENABLED = true` at the top of
`js/resources.js`. That is the whole change. A form then appears in front of
the *key points* card on each guide, and a successful submission creates a
Clio Grow lead tagged with which guide the visitor wanted
(`guide_car_accident`, `guide_dui_48h`, `guide_ticket_cost`).

**The article text is never gated, and must not be.** Hiding it behind a form
removes it from search results, which is the only reason it earns anything.
Only the summary card is gateable, and the gate has been tested in both states.

Enabling the gate means emailing people who fill it in — so `privacy/` and the
consent checkbox need to be live and reviewed first.
