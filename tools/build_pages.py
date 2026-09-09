#!/usr/bin/env python3
"""Render the practice-area pages from tools/content.py.

The generated HTML is committed and deploys as-is — Cloudflare Pages runs no
build step. This script exists so the shared chrome (header, footer, CTA bands,
structured data) stays identical across seven pages when one of them changes.

    python3 tools/build_pages.py
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import PAGES, HUB, BY_SLUG, FIRM  # noqa: E402
from resources import GUIDES  # noqa: E402

# Inverted from each guide's own related_practice, so a guide added or
# repointed in tools/resources.py updates the practice pages automatically.
GUIDE_FOR_PRACTICE = {g["related_practice"][0]: g for g in GUIDES}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = FIRM["base"]
TEL = FIRM["phone_link"]
PHONE = FIRM["phone_display"]


def head(title, description, path, extra_ld=None, robots="index,follow,max-image-preview:large"):
    url = f"{BASE}{path}"
    ld = json.dumps(extra_ld, indent=2, ensure_ascii=False) if extra_ld else None
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">

<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0e2947">

<meta property="og:type" content="article">
<meta property="og:site_name" content="Jay Hutch Law">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/assets/hero-atlanta.jpg">
<meta name="twitter:card" content="summary_large_image">

<link rel="preload" href="/assets/fonts/dm-sans-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/libre-baskerville-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/styles.css">
<link rel="icon" href="/assets/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/assets/favicon.png">
{f'<script type="application/ld+json">{chr(10)}{ld}{chr(10)}</script>' if ld else ''}
</head>

<body>
<a class="skip-link" href="#main">Skip to main content</a>
"""


def header(active=""):
    def cls(name):
        return ' aria-current="page"' if name == active else ""
    return f"""<header class="site-header">
  <div class="shell nav-wrap">
    <a class="brand" href="/" aria-label="Jay Hutch Law — home">
      <picture>
        <source media="(max-width:560px)" srcset="/assets/logo-mark.png">
        <img src="/assets/logo.png" alt="" width="760" height="322">
      </picture>
    </a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Menu">
      <i aria-hidden="true"></i><i aria-hidden="true"></i><i aria-hidden="true"></i>
    </button>
    <nav class="site-nav" id="site-nav" aria-label="Primary">
      <a href="/"{cls('home')}>Home</a>
      <a href="/practice-areas/"{cls('practice')}>Practice Areas</a>
      <a href="/attorney/"{cls('attorney')}>Attorney</a>
      <a href="/resources/"{cls('resources')}>Resources</a>
      <a href="/#about">About</a>
      <a href="/#consultation">Contact</a>
    </nav>
    <div class="nav-actions">
      <a class="phone" href="tel:{TEL}">☎ <span>855-HUTCHLAW</span></a>
      <a class="button button-gold" href="/#consultation">Free Consultation</a>
    </div>
  </div>
</header>
"""


def breadcrumb(trail):
    items = []
    for i, (label, href) in enumerate(trail):
        if href and i < len(trail) - 1:
            items.append(f'<li><a href="{href}">{html.escape(label)}</a></li>')
        else:
            items.append(f'<li><span aria-current="page">{html.escape(label)}</span></li>')
    return f"""<nav class="breadcrumb" aria-label="Breadcrumb">
  <div class="shell"><ol>{''.join(items)}</ol></div>
</nav>
"""


def sidebar_form(page):
    guide = GUIDE_FOR_PRACTICE.get(page["slug"])
    guide_card = ""
    if guide:
        guide_card = f"""
  <div class="aside-card">
    <p class="eyebrow">Free guide</p>
    <h2>{html.escape(guide['nav'])}</h2>
    <p class="form-note" style="margin-bottom:1rem">{html.escape(guide['read_time'])} · free to read, no form</p>
    <a class="button button-outline full" href="/resources/{guide['slug']}/">Read the guide →</a>
  </div>
"""

    return f"""<aside class="page-aside">
  <div class="aside-card">
    <p class="eyebrow">Free consultation</p>
    <h2>Talk to us about your {html.escape(page['nav'].lower())} matter.</h2>
    <form class="contact-form stacked" data-lead-form data-source="{page['source']}" novalidate>
      <div class="field full">
        <label for="sb_first">First Name <span class="req" aria-hidden="true">*</span></label>
        <input id="sb_first" name="first_name" data-label="First name" autocomplete="given-name" required>
        <span class="field-error" aria-live="polite"></span>
      </div>
      <div class="field full">
        <label for="sb_last">Last Name <span class="req" aria-hidden="true">*</span></label>
        <input id="sb_last" name="last_name" data-label="Last name" autocomplete="family-name" required>
        <span class="field-error" aria-live="polite"></span>
      </div>
      <div class="field full">
        <label for="sb_email">Email <span class="req" aria-hidden="true">*</span></label>
        <input id="sb_email" name="email" type="email" data-label="Email" autocomplete="email" required>
        <span class="field-error" aria-live="polite"></span>
      </div>
      <div class="field full">
        <label for="sb_phone">Phone <span class="req" aria-hidden="true">*</span></label>
        <input id="sb_phone" name="phone" type="tel" data-label="Phone" autocomplete="tel" required>
        <span class="field-error" aria-live="polite"></span>
      </div>
      <div class="field full">
        <label for="sb_message">Briefly, what happened? <span class="req" aria-hidden="true">*</span></label>
        <textarea id="sb_message" name="message" rows="4" data-label="Summary" required></textarea>
        <span class="field-error" aria-live="polite"></span>
      </div>
      <input type="hidden" name="practice_area" value="{html.escape(page['nav'])}">
      <div class="hp-field" aria-hidden="true">
        <label for="sb_company">Company</label>
        <input id="sb_company" name="company" type="text" tabindex="-1" autocomplete="off" data-honeypot>
      </div>
      <div class="field full">
        <label class="consent" for="sb_consent">
          <input id="sb_consent" name="consent" type="checkbox" value="yes" required data-label="Consent">
          <span>I agree to be contacted about my inquiry and have read the <a href="/privacy/">privacy policy</a>. <span class="req" aria-hidden="true">*</span></span>
        </label>
        <span class="field-error" aria-live="polite"></span>
      </div>
      <button class="button button-gold full" type="submit">Request a Free Consultation</button>
      <div class="form-status full" aria-live="polite"></div>
      <p class="form-note full">Submitting this form does not create an attorney-client relationship.</p>
    </form>
  </div>

  <div class="aside-card aside-call">
    <p class="eyebrow">Prefer to talk now?</p>
    <a class="aside-phone" href="tel:{TEL}">☎ {PHONE}</a>
    <p class="form-note">Atlanta, Georgia · Serving clients statewide</p>
  </div>
{guide_card}</aside>
"""


def footer():
    links = "\n        ".join(
        f'<a href="/practice-areas/{p["slug"]}/">{html.escape(p["nav"])}</a>' for p in PAGES
    )
    return f"""<footer class="site-footer">
  <div class="shell">
    <div class="footer-grid">
      <div>
        <a class="brand" href="/" aria-label="Jay Hutch Law — home">
          <img src="/assets/logo.png" alt="" width="760" height="322">
        </a>
        <p style="margin-top:1.25rem;color:#93a3b6">Strategic legal representation for individuals and families throughout Georgia.</p>
      </div>
      <div>
        <h3>Practice Areas</h3>
        {links}
      </div>
      <div>
        <h3>Firm</h3>
        <a href="/attorney/">Attorney</a>
        <a href="/resources/">Resources</a>
        <a href="/#about">About</a>
        <a href="/upload-citation/">Upload a Citation</a>
        <a href="/#consultation">Contact</a>
      </div>
      <div>
        <h3>Contact</h3>
        <a href="tel:{TEL}">{PHONE}</a>
        <a href="mailto:{FIRM['email']}">{FIRM['email']}</a>
        <p style="margin-top:.75rem;color:#93a3b6">3355 Lenox Road NE<br>Suite 750<br>Atlanta, Georgia 30326</p>
        <div class="footer-social">
          <a href="https://www.instagram.com/jayhutchlaw_ga" aria-label="Jay Hutch Law on Instagram" target="_blank" rel="noopener">
            <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>
          </a>
          <a href="https://www.facebook.com/profile.php?id=61564563643201" aria-label="Jay Hutch Law on Facebook" target="_blank" rel="noopener">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>
          </a>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© <span class="year">2026</span> Jay Hutch Law. All rights reserved. The information on this website is for general informational purposes only and is not legal advice. Viewing this site or contacting the firm does not create an attorney-client relationship.</p>
      <div class="footer-legal">
        <a href="/privacy/">Privacy Policy</a>
        <a href="/disclaimer/">Disclaimer</a>
      </div>
    </div>
  </div>
</footer>

<nav class="action-bar" aria-label="Quick contact">
  <a href="tel:{TEL}">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>
    Call
  </a>
  <a href="sms:{TEL}">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 11.5a8.4 8.4 0 0 1-9 8.4 9 9 0 0 1-4.2-1L3 20l1.1-4.7A8.4 8.4 0 0 1 3 11.5a8.4 8.4 0 0 1 9-8.4 8.4 8.4 0 0 1 9 8.4z"/></svg>
    Text
  </a>
  <a class="primary" href="#consult">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4h16v12H7l-3 3V4z"/></svg>
    Free Consult
  </a>
</nav>

<script src="/js/site.js" defer></script>
<script src="/js/forms.js" defer></script>
</body>
</html>
"""


def cta_band():
    return f"""<section class="cta-band">
  <div class="shell">
    <p class="eyebrow eyebrow-light">Your matter deserves personal attention</p>
    <h2>Let's talk about where you stand.</h2>
    <div class="button-row">
      <a class="button button-gold button-lg" href="#consult">Request a Free Consultation</a>
      <a class="button button-ghost button-lg" href="tel:{TEL}">☎ Call {PHONE}</a>
    </div>
  </div>
</section>
"""


def build_practice_page(page):
    path = f"/practice-areas/{page['slug']}/"

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Service",
                "@id": f"{BASE}{path}#service",
                "name": page["nav"],
                "serviceType": page["nav"],
                "description": page["description"],
                "provider": {"@id": f"{BASE}/#firm"},
                "areaServed": [
                    {"@type": "State", "name": "Georgia"},
                    {"@type": "City", "name": "Atlanta"},
                ],
                "url": f"{BASE}{path}",
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{BASE}{path}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Practice Areas", "item": f"{BASE}/practice-areas/"},
                    {"@type": "ListItem", "position": 3, "name": page["nav"], "item": f"{BASE}{path}"},
                ],
            },
            {
                "@type": "FAQPage",
                "@id": f"{BASE}{path}#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a},
                    }
                    for q, a in page["faqs"]
                ],
            },
        ],
    }

    body = []
    for heading, paras in page["sections"]:
        body.append(f"      <h2>{html.escape(heading)}</h2>")
        for p in paras:
            body.append(f"      <p>{p}</p>")

    check_title, check_items = page["checklist"]
    checklist = "\n".join(f"        <li>{html.escape(i)}</li>" for i in check_items)

    faqs = "\n".join(
        f"""        <details>
          <summary>{html.escape(q)}</summary>
          <p>{html.escape(a)}</p>
        </details>"""
        for q, a in page["faqs"]
    )

    related = "\n".join(
        f"""        <a class="practice-card" href="/practice-areas/{BY_SLUG[s]['slug']}/">
          <span>{BY_SLUG[s]['num']}</span>
          <h3>{html.escape(BY_SLUG[s]['nav'])}</h3>
          <p>{html.escape(BY_SLUG[s]['lede'][:110].rsplit(' ', 1)[0])}…</p>
          <b>Learn more →</b>
        </a>"""
        for s in page["related"]
    )

    urgent = (
        f'      <div class="notice"><p>{page["urgent"]}</p></div>\n'
        if page.get("urgent") else ""
    )

    return (
        head(page["title"], page["description"], path, ld)
        + header("practice")
        + breadcrumb([("Home", "/"), ("Practice Areas", "/practice-areas/"), (page["nav"], None)])
        + f"""<main id="main">

  <section class="page-hero-light">
    <div class="shell">
      <p class="eyebrow">Practice area {page['num']}</p>
      <h1>{html.escape(page['h1'])}</h1>
      <p class="lede">{html.escape(page['lede'])}</p>
    </div>
  </section>

  <section class="section-tight" id="consult">
    <div class="shell page-layout">
      <article class="page-body">
{urgent}{chr(10).join(body)}

      <div class="checklist">
        <h3>{html.escape(check_title)}</h3>
        <ul>
{checklist}
        </ul>
      </div>

      <h2>Common questions</h2>
      <div class="faq">
{faqs}
      </div>

      <p class="disclaimer-note">This page describes general principles of Georgia law and is not legal advice. Statutes and procedures change, and how they apply depends on the facts of your situation. Speak with an attorney about your specific matter.</p>
      </article>

{sidebar_form(page)}
    </div>
  </section>

  <section class="section paper">
    <div class="shell">
      <div class="section-head">
        <p class="eyebrow">Related</p>
        <h2>Other ways the firm can help.</h2>
      </div>
      <div class="card-grid">
{related}
      </div>
    </div>
  </section>

"""
        + cta_band()
        + "</main>\n\n"
        + footer()
    )


def build_hub():
    path = "/practice-areas/"
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "@id": f"{BASE}{path}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Practice Areas", "item": f"{BASE}{path}"},
                ],
            },
            {
                "@type": "ItemList",
                "@id": f"{BASE}{path}#list",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": i + 1,
                        "name": p["nav"],
                        "url": f"{BASE}/practice-areas/{p['slug']}/",
                    }
                    for i, p in enumerate(PAGES)
                ],
            },
        ],
    }

    cards = "\n".join(
        f"""        <a class="practice-card" href="/practice-areas/{p['slug']}/">
          <span>{p['num']}</span>
          <h3>{html.escape(p['nav'])}</h3>
          <p>{html.escape(p['lede'][:130].rsplit(' ', 1)[0])}…</p>
          <b>Learn more →</b>
        </a>"""
        for p in PAGES
    )

    return (
        head(HUB["title"], HUB["description"], path, ld)
        + header("practice")
        + breadcrumb([("Home", "/"), ("Practice Areas", None)])
        + f"""<main id="main">

  <section class="page-hero-light">
    <div class="shell hub-hero">
      <div>
        <p class="eyebrow">Practice areas</p>
        <h1>{html.escape(HUB['h1'])}</h1>
      </div>
      <p class="lede">{html.escape(HUB['lede'])}</p>
    </div>
  </section>

  <section class="section-tight">
    <div class="shell">
      <h2 class="sr-only">Practice areas</h2>
      <div class="card-grid">
{cards}
      </div>
    </div>
  </section>

  <section class="section paper">
    <div class="shell split">
      <div>
        <p class="eyebrow">Not sure where you fit?</p>
        <h2>Describe what happened, and we will tell you.</h2>
      </div>
      <div>
        <p class="lede">Many matters cross more than one of these areas, and some do not fit neatly into any of them. A short conversation is usually enough to work out what you are actually dealing with and what your options are.</p>
        <div class="button-row">
          <a class="button button-gold button-lg" href="/#consultation">Request a Free Consultation</a>
          <a class="button button-outline button-lg" href="tel:{TEL}">☎ Call {PHONE}</a>
        </div>
      </div>
    </div>
  </section>

"""
        + cta_band()
        + "</main>\n\n"
        + footer()
    )


def write(path, content):
    full = os.path.join(ROOT, path.lstrip("/"), "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(content)
    return full, len(content)


if __name__ == "__main__":
    written = [write("/practice-areas/", build_hub())]
    for page in PAGES:
        written.append(write(f"/practice-areas/{page['slug']}/", build_practice_page(page)))
    for full, size in written:
        print(f"  {size:>7,} B  {os.path.relpath(full, ROOT)}")
    print(f"\n{len(written)} pages written.")
