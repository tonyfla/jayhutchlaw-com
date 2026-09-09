#!/usr/bin/env python3
"""Render /resources/ — the guide hub and its articles.

    python3 tools/build_resources.py

Gating: the article text is always open and indexed. Only the download card is
gateable, via GATE_ENABLED in js/resources.js. See that file.
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_pages import head, header, breadcrumb, footer, cta_band, write, BASE, TEL, PHONE  # noqa: E402
from resources import GUIDES, HUB  # noqa: E402


def footer_with_gate():
    """Guide pages also load resources.js (print support + the optional gate)."""
    return footer().replace(
        '<script src="/js/forms.js" defer></script>',
        '<script src="/js/forms.js" defer></script>\n<script src="/js/resources.js" defer></script>',
    )


def download_card(guide):
    """The designated gate point.

    Rendered open. When GATE_ENABLED is true in js/resources.js, the script
    intercepts this and asks for contact details before revealing the guide
    summary — without touching the article above it, which must stay indexable.
    """
    items = "\n".join(f"          <li>{html.escape(i)}</li>" for i in guide["takeaway"])
    return f"""      <div class="download-card" data-gate="{guide['source']}">
        <div class="download-head">
          <p class="eyebrow">The short version</p>
          <h2>{html.escape(guide['nav'])} — key points</h2>
        </div>
        <div class="download-body" data-gated-content>
          <ul class="takeaway">
{items}
          </ul>
          <div class="button-row">
            <button class="button button-outline" type="button" data-print>Save or print this guide</button>
            <a class="button button-gold" href="/#consultation">Discuss your situation</a>
          </div>
        </div>
      </div>
"""


def build_guide(guide):
    path = f"/resources/{guide['slug']}/"
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "@id": f"{BASE}{path}#article",
                "headline": guide["h1"],
                "description": guide["description"],
                "url": f"{BASE}{path}",
                "author": {"@id": f"{BASE}/#attorney"},
                "publisher": {"@id": f"{BASE}/#firm"},
                "inLanguage": "en-US",
                "isAccessibleForFree": True,
                "about": guide["related_practice"][1],
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{BASE}{path}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Resources", "item": f"{BASE}/resources/"},
                    {"@type": "ListItem", "position": 3, "name": guide["nav"], "item": f"{BASE}{path}"},
                ],
            },
            {
                "@type": "FAQPage",
                "@id": f"{BASE}{path}#faq",
                "mainEntity": [
                    {"@type": "Question", "name": q,
                     "acceptedAnswer": {"@type": "Answer", "text": a}}
                    for q, a in guide["faqs"]
                ],
            },
        ],
    }

    body = []
    for heading, paras in guide["sections"]:
        body.append(f"      <h2>{html.escape(heading)}</h2>")
        for para in paras:
            body.append(f"      <p>{para}</p>")

    faqs = "\n".join(
        f"""        <details>
          <summary>{html.escape(q)}</summary>
          <p>{html.escape(a)}</p>
        </details>"""
        for q, a in guide["faqs"]
    )

    urgent = f'      <div class="notice"><p>{guide["urgent"]}</p></div>\n' if guide.get("urgent") else ""
    slug, label = guide["related_practice"]

    others = [g for g in GUIDES if g["slug"] != guide["slug"]]
    more = "\n".join(
        f"""        <a class="practice-card" href="/resources/{g['slug']}/">
          <span>{html.escape(g['kicker'])}</span>
          <h3>{html.escape(g['nav'])}</h3>
          <p>{html.escape(g['lede'][:110].rsplit(' ', 1)[0])}…</p>
          <b>Read the guide →</b>
        </a>""" for g in others
    )

    return (
        head(guide["title"], guide["description"], path, ld)
        + header("resources")
        + breadcrumb([("Home", "/"), ("Resources", "/resources/"), (guide["nav"], None)])
        + f"""<main id="main">

  <section class="page-hero-light">
    <div class="shell">
      <p class="eyebrow">{html.escape(guide['kicker'])} · {html.escape(guide['read_time'])}</p>
      <h1>{html.escape(guide['h1'])}</h1>
      <p class="lede">{html.escape(guide['lede'])}</p>
    </div>
  </section>

  <section class="section-tight" id="consult">
    <div class="shell page-layout">
      <article class="page-body">
{urgent}{chr(10).join(body)}

{download_card(guide)}
      <h2>Common questions</h2>
      <div class="faq">
{faqs}
      </div>

      <p class="disclaimer-note">This guide describes general principles of Georgia law and is not legal advice. Statutes and procedures change, and how they apply depends on the facts of your situation. Speak with an attorney about your specific matter.</p>
      </article>

      <aside class="page-aside">
        <div class="aside-card">
          <p class="eyebrow">Related practice area</p>
          <h2>{html.escape(label)}</h2>
          <p class="form-note" style="margin-bottom:1rem">Read how the firm handles these matters.</p>
          <a class="button button-outline full" href="/practice-areas/{slug}/">{html.escape(label)} →</a>
        </div>

        <div class="aside-card aside-call">
          <p class="eyebrow">Questions about your situation?</p>
          <a class="aside-phone" href="tel:{TEL}">☎ {PHONE}</a>
          <p class="form-note">Free consultation · Atlanta, Georgia</p>
        </div>

        <div class="aside-card">
          <p class="eyebrow">More guides</p>
""" + "\n".join(
            f'          <p style="margin:0 0 .75rem"><a class="text-link" href="/resources/{g["slug"]}/">{html.escape(g["nav"])} →</a></p>'
            for g in others
        ) + f"""
        </div>
      </aside>
    </div>
  </section>

  <section class="section paper">
    <div class="shell">
      <div class="section-head">
        <p class="eyebrow">Keep reading</p>
        <h2>Other guides.</h2>
      </div>
      <div class="card-grid">
{more}
      </div>
    </div>
  </section>

"""
        + cta_band()
        + "</main>\n\n"
        + footer_with_gate()
    )


def build_hub():
    path = "/resources/"
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "@id": f"{BASE}{path}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Resources", "item": f"{BASE}{path}"},
                ],
            },
            {
                "@type": "ItemList",
                "@id": f"{BASE}{path}#list",
                "itemListElement": [
                    {"@type": "ListItem", "position": i + 1, "name": g["nav"],
                     "url": f"{BASE}/resources/{g['slug']}/"}
                    for i, g in enumerate(GUIDES)
                ],
            },
        ],
    }

    cards = "\n".join(
        f"""        <a class="practice-card guide-card" href="/resources/{g['slug']}/">
          <span>{html.escape(g['kicker'])} · {html.escape(g['read_time'])}</span>
          <h3>{html.escape(g['nav'])}</h3>
          <p>{html.escape(g['lede'])}</p>
          <b>Read the guide →</b>
        </a>""" for g in GUIDES
    )

    return (
        head(HUB["title"], HUB["description"], path, ld)
        + header("resources")
        + breadcrumb([("Home", "/"), ("Resources", None)])
        + f"""<main id="main">

  <section class="page-hero-light">
    <div class="shell hub-hero">
      <div>
        <p class="eyebrow">Resources</p>
        <h1>{html.escape(HUB['h1'])}</h1>
      </div>
      <p class="lede">{html.escape(HUB['lede'])}</p>
    </div>
  </section>

  <section class="section-tight">
    <div class="shell">
      <div class="card-grid">
{cards}
      </div>
    </div>
  </section>

  <section class="section paper">
    <div class="shell split">
      <div>
        <p class="eyebrow">A guide is not advice</p>
        <h2>These explain the general rules. Your situation has facts.</h2>
      </div>
      <div>
        <p class="lede">Everything here describes how Georgia law generally works. Whether it applies to you depends on details a guide cannot know — the charge, the court, your record, and what actually happened.</p>
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
        + footer_with_gate()
    )


if __name__ == "__main__":
    out = [write("/resources/", build_hub())]
    for g in GUIDES:
        out.append(write(f"/resources/{g['slug']}/", build_guide(g)))
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for full, size in out:
        print(f"  {size:>7,} B  {os.path.relpath(full, root)}")
