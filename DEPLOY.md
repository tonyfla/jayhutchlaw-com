# Deploy runbook

Taking jayhutchlaw.com from the current Wix site to Cloudflare Pages.

The old site stays live and untouched until step 7. Everything before that is
reversible, and nothing a visitor sees changes until you move the nameservers.

**Budget about 90 minutes**, split across two sittings — steps 1–6 can be done
whenever, step 7 is the one to do deliberately.

---

## What you need before starting

- [ ] GitHub login (`tonyfla`) — the repo already exists
- [ ] A Cloudflare account (free) — create at dash.cloudflare.com
- [ ] A Clio Grow account with developer access, for the API token
- [ ] **Network Solutions login** — the domain is registered there, and the
      nameserver change in step 7 happens at Network Solutions, not at Wix.
      Wix only runs the nameservers (`NS10/NS11.WIXDNS.NET`). If nobody knows
      this login, sort it out before you begin: recovering it is the single
      most likely thing to stall the launch.
- [ ] Attorney sign-off on the draft copy (see "Blockers" at the end)

---

## 1. Push the repo

There are **9 local commits that have never been pushed**. Cloudflare builds
from GitHub, so it cannot see any of the site until you do this.

```bash
cd ~/Projects/jayhutchlaw-com
git push origin main
```

- [ ] `git log origin/main --oneline -1` shows the latest commit

---

## 2. Create the Pages project

In the Cloudflare dashboard: **Workers & Pages → Create → Pages → Connect to Git**,
then pick `tonyfla/jayhutchlaw-com`.

Build settings — the important part is that there is **no build step**:

| Setting | Value |
|---|---|
| Framework preset | None |
| Build command | *(leave empty)* |
| Build output directory | `/` |
| Root directory | `/` |

Save and deploy. It should finish in well under a minute, since it is only
copying files.

Cloudflare finds `functions/api/lead.js` on its own and serves it at `/api/lead`.
There is nothing to configure for that.

- [ ] The build succeeded
- [ ] `https://<project>.pages.dev` loads the new homepage

If the deploy shows the old flat pages, check that `_redirects` and `_headers`
are at the repository root and that the output directory is `/`, not `dist`.

---

## 3. Create the R2 bucket

**R2 → Create bucket**, name it `jayhutchlaw-uploads`. Location: North America.

> **Leave the bucket private. Do not enable public access.**
>
> Uploaded citations contain names, addresses, dates of birth, and licence
> numbers. A public bucket means anyone holding the URL can read them, and
> that URL is stored in the Clio Grow lead. Object keys are random, but that
> is obscurity, not access control — and these are client documents.
>
> Kept private, the function records the object key in the Clio note instead
> of a link, and staff retrieve the file from the Cloudflare dashboard. That
> is one extra step for the firm and a great deal less exposure.

Then bind the bucket to the site: **the Pages project → Settings → Functions →
R2 bucket bindings → Add**.

| Variable name | Bucket |
|---|---|
| `UPLOADS` | `jayhutchlaw-uploads` |

The variable name must be exactly `UPLOADS` — that is what the function reads.

- [ ] Bucket created, public access **off**
- [ ] Binding added as `UPLOADS`

---

## 4. Get the Clio Grow token and IDs

From the Clio developer portal, create an application and generate a token with
access to Grow. Keep the tab open — you need four things:

| What | Where | Used for |
|---|---|---|
| API token | Developer portal | `CLIO_GROW_TOKEN` |
| Location ID | `GET /grow/locations` | Tags leads to the Atlanta office |
| Matter type IDs | `GET /grow/matter_types` | Categorising leads by practice area |
| Source IDs | `GET /grow/sources` | Campaign attribution |

With the token in hand:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.clio.com/grow/sources
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.clio.com/grow/matter_types
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.clio.com/grow/locations
```

> **If these return 401 with a valid token, the auth scheme is the thing to
> check.** Clio's public docs do not state the header format, so the code
> assumes `Authorization: Bearer <token>`. If Clio uses something else, change
> the one line in `functions/api/lead.js` that sets `authorization`. This is
> the most likely single point of failure in the whole integration.

Then fill in `MARKETING_SOURCE_IDS` near the top of `functions/api/lead.js`
using the IDs from `/grow/sources`, and commit:

```js
const MARKETING_SOURCE_IDS = {
  google:   42,
  facebook: 43,
  bing:     44,
  referral: 45,
};
```

Until this is filled in, leads still arrive — they just have no marketing
source attached, so you cannot tell which campaign produced them.

- [ ] Token obtained and the three `curl` calls return data
- [ ] `MARKETING_SOURCE_IDS` filled in, committed, pushed

---

## 5. Set the environment variables

**Pages project → Settings → Environment variables → Production.**

| Name | Value | Type |
|---|---|---|
| `CLIO_GROW_TOKEN` | your token | **Encrypted** |
| `CLIO_REGION` | `us` | Plain text |
| `CLIO_LOCATION_ID` | from `/grow/locations` | Plain text |
| `PUBLIC_UPLOAD_BASE` | **leave unset** — see step 3 | — |

`CLIO_GROW_TOKEN` must be set as **Encrypted**, not plain text. Plain-text
variables are readable by anyone with dashboard access.

**Redeploy after adding variables.** They are read at request time, but the
deployment must be re-triggered to pick up new bindings: **Deployments →
latest → Retry deployment**.

- [ ] Variables set, token encrypted
- [ ] Redeployed

---

## 6. Test before touching DNS

This is the whole point of doing DNS last. Test on the `.pages.dev` URL while
the real site is still safely on Wix.

- [ ] Homepage, a practice page, a guide, and `/upload-citation/` all load
- [ ] Submit the homepage form with real details → lands on `/thank-you/`
- [ ] **The lead appears in the Clio Grow inbox**, untriaged
- [ ] Submit `/upload-citation/` with a photo attached
- [ ] The file appears in the R2 bucket, and its key is in the Clio note
- [ ] Visit with `?utm_source=facebook&utm_medium=cpc&utm_campaign=test`, submit,
      and confirm the campaign shows in the lead's message body
- [ ] Check on a phone: the sticky Call / Text / Consult bar works

If a form shows an error instead of redirecting, that is the design working —
it never fakes success. **Deployments → latest → Functions** shows the real
reason; the function logs the full lead on failure so nothing is lost.

Do not proceed until a test lead has actually arrived in Clio Grow.

---

## 7. Custom domain and DNS cutover

Now the visible change. Two parts, in order.

**7a. Add the site to Cloudflare.** From the dashboard, add `jayhutchlaw.com`
as a site on the Free plan. Cloudflare scans the existing DNS and shows you two
nameservers to use.

Before moving on, check the imported records — in particular that **MX records
for email came across**. If the firm's email runs through this domain, losing
those records takes down email, and it is the most common way this step causes
real damage.

**7b. Change the nameservers at Network Solutions.** Log in there, find the
domain's DNS or nameserver settings, and replace:

```
NS10.WIXDNS.NET
NS11.WIXDNS.NET
```

with the two Cloudflare gave you.

Propagation is usually under an hour, occasionally up to 24. Cloudflare emails
you when the domain is active.

**7c. Attach the domain to the Pages project.** Once Cloudflare shows the domain
as active: **Pages project → Custom domains → Set up a custom domain**, and add
both `jayhutchlaw.com` and `www.jayhutchlaw.com`. Cloudflare creates the records
and issues the certificate automatically.

Set the apex to redirect to `www`, since every canonical URL on the site uses
`www`. A **Redirect Rule** on `jayhutchlaw.com/*` → `https://www.jayhutchlaw.com/$1`
with a 301 does it.

- [ ] MX records verified before the switch
- [ ] Nameservers changed at Network Solutions
- [ ] Domain active in Cloudflare
- [ ] Both hostnames added to the Pages project, HTTPS working
- [ ] Apex redirects to `www`
- [ ] Email still working

---

## 8. After launch

- [ ] Google Search Console: add the property, verify by DNS, submit
      `https://www.jayhutchlaw.com/sitemap.xml`
- [ ] Request indexing for the homepage and the six practice pages
- [ ] Update the Google Business Profile URL, and check the name, address and
      phone match `marketing/copy/firm-boilerplate.md` character for character
- [ ] Update the link on every social profile
- [ ] Run the homepage through PageSpeed Insights
- [ ] Cancel the Wix subscription — **only after a week of the new site being
      live and taking leads.** Cancelling early removes your fallback.

---

## Rollback

Nothing here is one-way.

**A bad deploy** — Pages keeps every previous build. **Deployments → an earlier
one → Rollback.** Live again in seconds.

**Something fundamentally wrong after cutover** — set the nameservers at Network
Solutions back to `NS10.WIXDNS.NET` and `NS11.WIXDNS.NET`. The Wix site returns
as soon as DNS propagates. This is why you do not cancel Wix straight away.

**Forms failing but the site fine** — leads are not lost. The function logs the
complete submission on every failure, visible under the deployment's Functions
logs, so anything that came in during an outage can be recovered by hand.

---

## Troubleshooting

| Symptom | Cause |
|---|---|
| Form returns 503, "intake system is not connected" | `CLIO_GROW_TOKEN` not set, or not redeployed after setting it |
| Form returns 502 | Clio rejected the request — check the Functions log for its response |
| Clio returns 401 with a good token | The auth scheme; see step 4 |
| Uploads silently missing | `UPLOADS` binding absent or misnamed |
| Old pages still served | Output directory is not `/`, or `_redirects` is not at the repo root |
| Leads arrive with no campaign | `MARKETING_SOURCE_IDS` still empty |
| CSS looks stale locally | Use `python3 tools/serve.py`, not `python -m http.server` |

---

## Blockers before any of this goes live

1. **Attorney review of all draft copy** — six practice pages, three guides, and
   the privacy policy and disclaimer. Georgia code references are cited inline
   so it can be checked quickly. Nothing publishes under the firm's name
   unreviewed.
2. **Confirm the Clio auth header** (step 4).
3. **Photography** — the attorney page shows a placeholder block.
4. Convert the hero to WebP — the largest remaining performance item, and the
   only one on this list that is purely cosmetic.
