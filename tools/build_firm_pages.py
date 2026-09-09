#!/usr/bin/env python3
"""Render /attorney/ and /upload-citation/ using the shared chrome.

    python3 tools/build_firm_pages.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_pages import head, header, breadcrumb, footer, cta_band, write, BASE, TEL, PHONE  # noqa: E402

ATTORNEY_LD = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "Attorney",
            "@id": f"{BASE}/#attorney",
            "name": "James Hutchins",
            "honorificSuffix": "Esq.",
            "jobTitle": "Managing Attorney",
            "url": f"{BASE}/attorney/",
            "worksFor": {"@id": f"{BASE}/#firm"},
            "knowsAbout": [
                "Immigration Law", "Estate Planning", "Personal Injury", "DUI Defense",
            ],
            "areaServed": {"@type": "State", "name": "Georgia"},
        },
        {
            "@type": "BreadcrumbList",
            "@id": f"{BASE}/attorney/#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": "Attorney", "item": f"{BASE}/attorney/"},
            ],
        },
    ],
}


def build_attorney():
    return (
        head(
            "James Hutchins, Esq. | Atlanta Attorney | Jay Hutch Law",
            "Meet James Hutchins, managing attorney at Jay Hutch Law in Atlanta, Georgia — "
            "practising in immigration, estate planning, personal injury, and DUI defense.",
            "/attorney/",
            ATTORNEY_LD,
        )
        + header("attorney")
        + breadcrumb([("Home", "/"), ("Attorney", None)])
        + f"""<main id="main">

  <section class="section-tight">
    <div class="shell attorney-intro">
      <div>
        <p class="eyebrow">Meet Jay</p>
        <h1>Personal counsel.<br>Purposeful advocacy.</h1>
        <p class="attorney-name">James Hutchins, <span>Esq.</span></p>
        <p class="attorney-role">Managing Attorney</p>

        <p class="lede">Jay Hutch Law is grounded in a simple belief: people deserve clear counsel and steady support during difficult moments.</p>

        <p>Over the course of his legal career, Mr. Hutchins has focused on immigration law, estate planning, personal injury, and DUI defense. Whether guiding individuals through complex immigration processes, helping families secure their futures through thoughtful estate planning, advocating for those injured through no fault of their own, or protecting the rights of clients facing criminal charges, he remains focused on achieving practical, results-driven outcomes.</p>

        <p>He works closely with each client to understand their situation, explain the options actually available to them, and pursue a sensible path forward. Our purpose is simple: protect your rights, advocate efficiently on your behalf, and stand beside you every step of the way.</p>

        <div class="detail-list">
          <div><b>⌖</b>Licensed in Georgia</div>
          <div><b>♧</b>Client-Focused Representation</div>
          <div><b>▥</b>Strategic Legal Guidance</div>
        </div>

        <div class="button-row" style="margin-top:2rem">
          <a class="button button-gold button-lg" href="/#consultation">Request a Free Consultation</a>
          <a class="button button-outline button-lg" href="tel:{TEL}">☎ Call {PHONE}</a>
        </div>
      </div>

      <!-- Replace with a real portrait before launch. -->
      <div class="portrait-placeholder">JAMES HUTCHINS, ESQ.<br>PORTRAIT</div>
    </div>
  </section>

  <section class="section paper">
    <div class="shell values">
      <article class="value">
        <b aria-hidden="true">◇</b>
        <h2>Integrity</h2>
        <p>Honest guidance and straightforward counsel, including when the answer is not what you hoped for.</p>
      </article>
      <article class="value">
        <b aria-hidden="true">▥</b>
        <h2>Strategy</h2>
        <p>Practical solutions built around your circumstances rather than a standard template.</p>
      </article>
      <article class="value">
        <b aria-hidden="true">♧</b>
        <h2>Responsiveness</h2>
        <p>Direct attorney access and clear communication, so you are never guessing where things stand.</p>
      </article>
    </div>
  </section>

"""
        + cta_band()
        + "</main>\n\n"
        + footer()
    )


CITATION_LD = {
    "@context": "https://schema.org",
    "@graph": [{
        "@type": "BreadcrumbList",
        "@id": f"{BASE}/upload-citation/#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Upload Your Citation", "item": f"{BASE}/upload-citation/"},
        ],
    }],
}


def build_citation():
    return (
        head(
            "Upload Your Georgia Traffic Citation for Review | Jay Hutch Law",
            "Send a photo or PDF of your Georgia traffic citation. Jay Hutch Law will review "
            "the details and contact you about possible next steps. No obligation.",
            "/upload-citation/",
            CITATION_LD,
        )
        + header()
        + breadcrumb([("Home", "/"), ("Upload Your Citation", None)])
        + f"""<main id="main">

  <section class="page-hero-light">
    <div class="shell">
      <p class="eyebrow">Traffic citations</p>
      <h1>Upload your citation for review.</h1>
      <p class="lede">Send a clear photo or PDF of the front and back. Our office will review the details and contact you about possible next steps.</p>
    </div>
  </section>

  <section class="section-tight" id="consult">
    <div class="shell page-layout">
      <article class="page-body">
        <div class="notice">
          <p>Paying a citation online is a guilty plea, not a settlement. Before you pay, it is worth knowing what it adds to your record. Do not miss any date listed on your citation while waiting to hear from us.</p>
        </div>

        <h2>Submit your citation</h2>

        <form class="contact-form" data-lead-form data-source="citation_upload" novalidate>
          <div class="field">
            <label for="c_first">First Name <span class="req" aria-hidden="true">*</span></label>
            <input id="c_first" name="first_name" data-label="First name" autocomplete="given-name" required>
            <span class="field-error" aria-live="polite"></span>
          </div>
          <div class="field">
            <label for="c_last">Last Name <span class="req" aria-hidden="true">*</span></label>
            <input id="c_last" name="last_name" data-label="Last name" autocomplete="family-name" required>
            <span class="field-error" aria-live="polite"></span>
          </div>
          <div class="field">
            <label for="c_email">Email <span class="req" aria-hidden="true">*</span></label>
            <input id="c_email" name="email" type="email" data-label="Email" autocomplete="email" required>
            <span class="field-error" aria-live="polite"></span>
          </div>
          <div class="field">
            <label for="c_phone">Phone <span class="req" aria-hidden="true">*</span></label>
            <input id="c_phone" name="phone" type="tel" data-label="Phone" autocomplete="tel" required>
            <span class="field-error" aria-live="polite"></span>
          </div>

          <div class="field full">
            <label for="c_court">Court date, county, or other details</label>
            <textarea id="c_court" name="court_date" rows="3" data-label="Details"></textarea>
            <span class="field-error" aria-live="polite"></span>
          </div>

          <label class="upload-box full" for="c_files">
            <input id="c_files" name="files" type="file" accept="image/*,.pdf" multiple>
            <div>
              <span aria-hidden="true" style="font-size:1.5rem;color:var(--gold-deep)">⇧</span>
              <strong>Upload your citation</strong>
              <p>Photo or PDF · front and back · up to 4 files, 10 MB each</p>
            </div>
          </label>
          <p class="upload-list full" aria-live="polite"></p>

          <input type="hidden" name="practice_area" value="Traffic Citations">

          <div class="hp-field" aria-hidden="true">
            <label for="c_company">Company</label>
            <input id="c_company" name="company" type="text" tabindex="-1" autocomplete="off" data-honeypot>
          </div>

          <div class="field full">
            <label class="consent" for="c_consent">
              <input id="c_consent" name="consent" type="checkbox" value="yes" required data-label="Consent">
              <span>I agree to be contacted about my citation and have read the <a href="/privacy/">privacy policy</a>. <span class="req" aria-hidden="true">*</span></span>
            </label>
            <span class="field-error" aria-live="polite"></span>
          </div>

          <button class="button button-gold button-lg full" type="submit">Submit Citation for Review</button>
          <div class="form-status full" aria-live="polite"></div>

          <p class="form-note full">Submitting this form does not create an attorney-client relationship. Do not miss any listed court date, payment date, or response deadline while waiting for a response.</p>
        </form>

        <p class="disclaimer-note">This page is general information about Georgia traffic matters and is not legal advice. Whether any particular option is available depends on the charge, the court, and your driving history.</p>
      </article>

      <aside class="page-aside">
        <div class="aside-card">
          <p class="eyebrow">What happens next</p>
          <div class="step" style="margin:0 0 1.5rem">
            <span class="step-number" aria-hidden="true">1</span>
            <div><h3>You submit it</h3><p>Send a clear photo or PDF using the form.</p></div>
          </div>
          <div class="step" style="margin:0 0 1.5rem">
            <span class="step-number" aria-hidden="true">2</span>
            <div><h3>We review the details</h3><p>We check the charge, the points, and the court.</p></div>
          </div>
          <div class="step" style="margin:0">
            <span class="step-number" aria-hidden="true">3</span>
            <div><h3>We discuss your options</h3><p>We contact you about possible next steps.</p></div>
          </div>
        </div>

        <div class="aside-card aside-call">
          <p class="eyebrow">Prefer to talk now?</p>
          <a class="aside-phone" href="tel:{TEL}">☎ {PHONE}</a>
          <p class="form-note">Atlanta, Georgia · Serving clients statewide</p>
        </div>

        <div class="aside-card">
          <p class="eyebrow">Related</p>
          <p style="margin:0 0 .75rem"><a class="text-link" href="/practice-areas/traffic-citations/">Traffic citations in Georgia →</a></p>
          <p style="margin:0"><a class="text-link" href="/practice-areas/dui-defense/">DUI defense →</a></p>
        </div>
      </aside>
    </div>
  </section>

"""
        + cta_band()
        + "</main>\n\n"
        + footer()
    )


if __name__ == "__main__":
    for path, builder in [("/attorney/", build_attorney), ("/upload-citation/", build_citation)]:
        full, size = write(path, builder())
        print(f"  {size:>7,} B  {os.path.relpath(full, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))}")
