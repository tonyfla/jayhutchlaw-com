#!/usr/bin/env python3
"""Render /attorney/ and /upload-citation/ using the shared chrome.

    python3 tools/build_firm_pages.py
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_pages import head, header, breadcrumb, footer, cta_band, write, BASE, TEL, PHONE  # noqa: E402
from content import PAGES, FIRM  # noqa: E402

EMAIL = FIRM["email"]

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
                "Immigration Law", "Personal Injury", "DUI Defense", "Traffic Citations",
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
    # Built with a plain loop rather than a nested f-string: Python 3.9's
    # f-string parser rejects the quoting this needs.
    cards = []
    for pa in PAGES:
        blurb = pa["lede"][:105].rsplit(" ", 1)[0] + "\u2026"
        cards.append(
            '        <a class="practice-card" href="/practice-areas/%s/">\n'
            '          <span>%s</span>\n'
            '          <h3>%s</h3>\n'
            '          <p>%s</p>\n'
            '          <b>Learn more \u2192</b>\n'
            '        </a>' % (pa["slug"], pa["num"], html.escape(pa["nav"]), html.escape(blurb))
        )
    practice_cards = "\n".join(cards)

    return (
        head(
            "James Hutchins, Esq. | Atlanta Attorney | Jay Hutch Law",
            "Meet James Hutchins, managing attorney at Jay Hutch Law in Atlanta, Georgia — "
            "practising in immigration, personal injury, DUI defense, and traffic matters.",
            "/attorney/",
            ATTORNEY_LD,
        )
        + header("attorney")
        + breadcrumb([("Home", "/"), ("Attorney", None)])
        + f"""<main id="main">

  <section class="page-hero-light">
    <div class="shell">
      <p class="eyebrow">The attorney</p>
      <h1>Meet James Hutchins, Esq.</h1>
      <p class="lede">Jay Hutch Law was founded on a simple belief: people deserve clear counsel and steady support during the moments that matter most.</p>
    </div>
  </section>

  <section class="section-tight">
    <div class="shell attorney-intro">
      <div>
        <p class="attorney-name">James Hutchins, <span>Esq.</span></p>
        <p class="attorney-role">Managing Attorney · Atlanta, Georgia</p>

        <p>Mr. Hutchins founded the firm to practise law the way he believed it should be practised — with integrity, with a strategy built around the person rather than the file, and with the responsiveness people in difficult situations actually need.</p>

        <p>Over the course of his career he has focused on immigration law, personal injury, and criminal defense. Whether guiding individuals through complex immigration processes, advocating for those injured through no fault of their own, or protecting the rights of clients facing DUI and traffic charges, he stays focused on practical, results-driven outcomes.</p>

        <p>He works directly with each client to understand what happened, explain the options actually available, and pursue a sensible path forward. The firm pairs that attention with a technology-driven approach to intake and case management — which is what makes it possible to stay responsive without giving any matter less thought than it deserves.</p>

        <p>The purpose is straightforward: protect your rights, advocate efficiently on your behalf, and stand beside you at every step.</p>

        <div class="detail-list">
          <div><b>⌖</b>Licensed in Georgia</div>
          <div><b>♧</b>Direct Attorney Access</div>
          <div><b>▥</b>Strategic Legal Guidance</div>
        </div>

        <div class="button-row" style="margin-top:2rem">
          <a class="button button-gold button-lg" href="/#consultation">Request a Free Consultation</a>
          <a class="button button-outline button-lg" href="tel:{TEL}">☎ Call {PHONE}</a>
        </div>
      </div>

      <img class="portrait" src="/assets/portrait-james-hutchins.jpg"
           alt="James Hutchins, managing attorney at Jay Hutch Law"
           width="900" height="1350" loading="lazy">
    </div>
  </section>

  <section class="section paper">
    <div class="shell">
      <div class="section-head">
        <p class="eyebrow">How the firm works</p>
        <h2>Three things every client gets.</h2>
      </div>
      <div class="values">
        <article class="value">
          <b aria-hidden="true">◇</b>
          <h3>Integrity</h3>
          <p>Honest guidance and straightforward counsel, including when the answer is not the one you hoped for.</p>
        </article>
        <article class="value">
          <b aria-hidden="true">▥</b>
          <h3>Strategy</h3>
          <p>An approach built around your circumstances and your goals, rather than a standard template.</p>
        </article>
        <article class="value">
          <b aria-hidden="true">♧</b>
          <h3>Responsiveness</h3>
          <p>Direct attorney access and clear communication, so you are never guessing where things stand.</p>
        </article>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="shell">
      <div class="section-kicker">
        <div>
          <p class="eyebrow">Where the firm practises</p>
          <h2>Areas Mr. Hutchins handles.</h2>
        </div>
        <a class="text-link" href="/practice-areas/">All practice areas →</a>
      </div>
      <div class="card-grid">
{practice_cards}
      </div>
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



FAQS = [
    ("How much does an initial consultation cost?",
     "Initial consultations are free. We will discuss your situation, explain the options available to you, and outline what representation would involve before you make any commitment."),
    ("Do I have to appear in court for a Georgia traffic citation?",
     "It depends on the charge and the court. Some citations can be resolved without a personal appearance, while others require one. Do not miss any date listed on your citation while you are waiting to hear back from our office."),
    ("What areas of Georgia does Jay Hutch Law serve?",
     "The firm is based in Atlanta and represents clients throughout Georgia. Contact us to confirm whether we can assist with a matter in your county."),
    ("How quickly will someone respond to my inquiry?",
     "Our office reviews inquiries as they arrive and aims to respond promptly. If your matter is time-sensitive or you have an approaching court date, please call 855-488-2452 rather than waiting on a form response."),
]

CONTACT_LD = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "ContactPage",
            "@id": BASE + "/contact/#page",
            "url": BASE + "/contact/",
            "name": "Contact Jay Hutch Law",
            "about": {"@id": BASE + "/#firm"},
        },
        {
            "@type": "BreadcrumbList",
            "@id": BASE + "/contact/#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Contact", "item": BASE + "/contact/"},
            ],
        },
        {
            "@type": "FAQPage",
            "@id": BASE + "/contact/#faq",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in FAQS
            ],
        },
    ],
}


def build_contact():
    options = "\n".join("              <option>%s</option>" % html.escape(pa["nav"]) for pa in PAGES)
    faq_html = "\n".join(
        '        <details>\n'
        '          <summary>%s</summary>\n'
        '          <p>%s</p>\n'
        '        </details>' % (html.escape(q), html.escape(a))
        for q, a in FAQS
    )
    return (
        head(
            "Contact Jay Hutch Law | Atlanta, Georgia | Free Consultation",
            "Contact Jay Hutch Law in Atlanta. Tell us about your matter and we will "
            "review it and respond. Free consultation - call 855-488-2452.",
            "/contact/",
            CONTACT_LD,
        )
        + header("contact")
        + breadcrumb([("Home", "/"), ("Contact", None)])
        + f"""<main id="main">

  <section class="page-hero-light">
    <div class="shell">
      <p class="eyebrow">Contact</p>
      <h1>Tell us what happened.</h1>
      <p class="lede">Share your contact details and a brief summary of your matter, including any court dates or deadlines. We will review it and come back to you about next steps.</p>
    </div>
  </section>

  <section class="section-tight" id="consult">
    <div class="shell page-layout">
      <article class="page-body">
        <div class="notice">
          <p>If you have an approaching court date or a deadline within the next few days, please call <a href="tel:{TEL}">{PHONE}</a> rather than waiting on a reply to this form.</p>
        </div>

        <h2>Send us a message</h2>

        <form class="contact-form" data-lead-form data-source="contact_page" novalidate>
          <div class="field">
            <label for="ct_first">First Name <span class="req" aria-hidden="true">*</span></label>
            <input id="ct_first" name="first_name" data-label="First name" autocomplete="given-name" required>
            <span class="field-error" aria-live="polite"></span>
          </div>
          <div class="field">
            <label for="ct_last">Last Name <span class="req" aria-hidden="true">*</span></label>
            <input id="ct_last" name="last_name" data-label="Last name" autocomplete="family-name" required>
            <span class="field-error" aria-live="polite"></span>
          </div>
          <div class="field">
            <label for="ct_email">Email <span class="req" aria-hidden="true">*</span></label>
            <input id="ct_email" name="email" type="email" data-label="Email" autocomplete="email" required>
            <span class="field-error" aria-live="polite"></span>
          </div>
          <div class="field">
            <label for="ct_phone">Phone <span class="req" aria-hidden="true">*</span></label>
            <input id="ct_phone" name="phone" type="tel" data-label="Phone" autocomplete="tel" required>
            <span class="field-error" aria-live="polite"></span>
          </div>
          <div class="field full">
            <label for="ct_area">What is your matter about?</label>
            <select id="ct_area" name="practice_area">
              <option value="">Select an area (optional)</option>
{options}
              <option>Something else</option>
            </select>
            <span class="field-error" aria-live="polite"></span>
          </div>
          <div class="field full">
            <label for="ct_message">Tell us about your case <span class="req" aria-hidden="true">*</span></label>
            <textarea id="ct_message" name="message" rows="6" data-label="Case summary" required></textarea>
            <span class="field-error" aria-live="polite"></span>
          </div>
          <div class="hp-field" aria-hidden="true">
            <label for="ct_company">Company</label>
            <input id="ct_company" name="company" type="text" tabindex="-1" autocomplete="off" data-honeypot>
          </div>
          <div class="field full">
            <label class="consent" for="ct_consent">
              <input id="ct_consent" name="consent" type="checkbox" value="yes" required data-label="Consent">
              <span>I agree to be contacted by Jay Hutch Law about my inquiry and have read the <a href="/privacy/">privacy policy</a>. <span class="req" aria-hidden="true">*</span></span>
            </label>
            <span class="field-error" aria-live="polite"></span>
          </div>
          <button class="button button-gold button-lg full" type="submit">Request a Free Consultation</button>
          <div class="form-status full" aria-live="polite"></div>
          <p class="form-note full">Submitting this form does not create an attorney-client relationship. Please do not include confidential or sensitive information in your message.</p>
        </form>

        <h2>Common questions</h2>
        <div class="faq">
{faq_html}
        </div>

        <p class="disclaimer-note">Contacting the firm does not create an attorney-client relationship, and does not pause or extend any deadline in your matter.</p>
      </article>

      <aside class="page-aside">
        <div class="aside-card aside-call">
          <p class="eyebrow">Prefer to talk now?</p>
          <a class="aside-phone" href="tel:{TEL}">☎ {PHONE}</a>
          <p class="form-note">Free consultation · No obligation</p>
        </div>

        <div class="aside-card">
          <p class="eyebrow">Our office</p>
          <p style="color:var(--muted);margin-bottom:1rem">3355 Lenox Road NE<br>Suite 750<br>Atlanta, Georgia 30326</p>
          <p style="margin:0"><a class="text-link" href="mailto:{EMAIL}">{EMAIL}</a></p>
        </div>

        <div class="aside-card">
          <p class="eyebrow">Traffic citation?</p>
          <p class="form-note" style="margin-bottom:1rem">Send a photo of it and we will review the charge.</p>
          <a class="button button-outline full" href="/upload-citation/">Upload Your Citation →</a>
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
    for path, builder in [("/attorney/", build_attorney), ("/upload-citation/", build_citation), ("/contact/", build_contact)]:
        full, size = write(path, builder())
        print(f"  {size:>7,} B  {os.path.relpath(full, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))}")
