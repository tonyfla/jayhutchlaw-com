#!/usr/bin/env python3
"""Render /privacy/ and /disclaimer/.

    python3 tools/build_legal.py

DRAFT. Both documents describe the site's actual behaviour accurately, but
they are not a substitute for review by counsel against the Georgia Rules of
Professional Conduct and applicable privacy law. Decision points needing an
answer are listed in marketing/copy/legal-review-notes.md.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_pages import head, header, breadcrumb, footer, write, BASE, TEL, PHONE  # noqa: E402

UPDATED = "9 September 2026"

CONTACT = f"""<h2>How to contact us</h2>
      <p>Jay Hutch Law<br>
      3355 Lenox Road NE, Suite 750<br>
      Atlanta, Georgia 30326<br>
      <a class="text-link" href="tel:{TEL}">{PHONE}</a> · <a class="text-link" href="mailto:contact@jayhutchlaw.com">contact@jayhutchlaw.com</a></p>"""


def page(title, description, path, crumb, h1, lede, body):
    return (
        head(title, description, path, None)
        + header()
        + breadcrumb([("Home", "/"), (crumb, None)])
        + f"""<main id="main">

  <section class="page-hero-light">
    <div class="shell">
      <p class="eyebrow">Legal</p>
      <h1>{h1}</h1>
      <p class="lede">{lede}</p>
    </div>
  </section>

  <section class="section-tight">
    <div class="shell">
      <article class="page-body">
      <p class="form-note">Last updated {UPDATED}</p>

{body}

{CONTACT}
      </article>
    </div>
  </section>

</main>

"""
        + footer()
    )


PRIVACY = """      <h2>Scope of this policy</h2>
      <p>This policy explains what information Jay Hutch Law collects through
      www.jayhutchlaw.com, why we collect it, who processes it on our behalf, and
      what choices you have. It applies to this website only. It does not govern
      information you provide to the firm by telephone, by post, or in person, and
      it does not alter the confidentiality obligations the firm owes to existing
      clients, which are broader than anything described here.</p>

      <h2>Information you give us</h2>
      <p>When you submit a form on this site, we receive what you type into it:
      your first and last name, email address, telephone number, the practice area
      you select, and your description of your legal matter. On the citation page,
      we also receive any files you choose to attach and any court date or detail
      you enter.</p>
      <p>You choose what to send. Please keep it brief and factual — see
      <strong>Do not send confidential information</strong> below.</p>

      <h2>Information collected automatically</h2>
      <p>When you arrive at the site we record marketing attribution data about
      how you got here, and hold it for the duration of your browsing session so
      it can be attached to a form you submit later. This consists of:</p>
      <ul>
        <li>the page you landed on and the page you submitted a form from;</li>
        <li>the website that referred you, if any;</li>
        <li>campaign parameters in the link you followed (commonly labelled
        <code>utm_source</code>, <code>utm_medium</code>, <code>utm_campaign</code>,
        <code>utm_term</code> and <code>utm_content</code>); and</li>
        <li>advertising click identifiers, if you arrived from an advertisement
        (<code>gclid</code>, <code>fbclid</code>, <code>msclkid</code>).</li>
      </ul>
      <p>This tells us which of our efforts brought you to the firm. It is stored
      in your browser's session storage and is discarded when you close the tab.
      We do not use it to build a profile of you, and we do not combine it with
      information from other sources.</p>
      <p>Our hosting provider also keeps standard server logs, which include IP
      addresses and request details, for security and reliability purposes.</p>

      <h2>Cookies</h2>
      <p>This site sets no advertising or analytics cookies of its own. The
      attribution data described above is held in session storage rather than in
      cookies, and is not readable by other websites.</p>

      <h2>How we use your information</h2>
      <p>We use what you submit to evaluate your enquiry, to contact you about it,
      to determine whether the firm can assist you, and to maintain our client
      intake records. We use attribution data in aggregate to understand which
      channels reach people who need our help.</p>
      <p>We do not sell your information. We do not share it with third parties
      for their own marketing purposes. We do not use it to make automated
      decisions that produce legal effects.</p>

      <h2>Who processes it for us</h2>
      <p>Two service providers handle this data on our behalf, under their own
      security and privacy commitments:</p>
      <ul>
        <li><strong>Clio Grow</strong> (Themis Solutions Inc.) — our client intake
        system. Form submissions are transmitted to Clio Grow and become an intake
        record there.</li>
        <li><strong>Cloudflare, Inc.</strong> — hosts the website and stores any
        files you upload.</li>
      </ul>
      <p>These providers act on our instructions. They are not permitted to use
      your information for their own purposes.</p>

      <h2>Files you upload</h2>
      <p>Files submitted through the citation page are stored in access-controlled
      storage. They are not published, not linked from any page, and not indexed by
      search engines. Only the firm can retrieve them.</p>

      <h2>Consent to be contacted</h2>
      <p>Each form asks you to confirm that you agree to be contacted about your
      enquiry. That consent covers our response to you. You may withdraw it at any
      time by replying to any message from us or by writing to the address below,
      and we will stop contacting you except where we are required to communicate
      with you about an existing matter.</p>

      <h2>Do not send confidential information</h2>
      <p>Please do not send confidential, privileged, or highly sensitive
      information through this website. <strong>Until an attorney-client
      relationship has been established in writing, information you send us is
      not protected by the attorney-client privilege.</strong> Send enough for us
      to understand the nature of your matter and no more; the detail belongs in a
      conversation once we have confirmed we can act for you.</p>
      <p>Email and web forms also travel over the public internet. We take
      reasonable measures to protect them, but no method of transmission is
      completely secure.</p>

      <h2>How long we keep it</h2>
      <p>We retain enquiry records for as long as needed to respond to you, to
      check for conflicts of interest in future, and to meet the firm's
      professional and record-keeping obligations. Where an enquiry does not
      become a matter, we keep a limited record for conflict-checking purposes.
      Records relating to matters the firm takes on are retained under the firm's
      file retention practices, which are separate from this policy.</p>

      <h2>Security</h2>
      <p>The site is served over HTTPS. Access to intake records and uploaded
      files is restricted to the firm. Credentials for our systems are held as
      encrypted secrets rather than in the website's code.</p>

      <h2>Your choices</h2>
      <p>You may ask us for a copy of the information we hold about you, ask us to
      correct it, or ask us to delete it. Write to us at the address below and we
      will respond to reasonable requests, subject to any legal or professional
      obligation that requires us to keep certain records. Some privacy laws give
      residents of particular states or countries specific rights; if a law of that
      kind applies to you, we will honour the rights it gives you.</p>

      <h2>Children</h2>
      <p>This website is intended for adults. We do not knowingly collect
      information from children under 13. If you believe a child has sent us
      information, please contact us and we will delete it.</p>

      <h2>Links to other sites</h2>
      <p>This site may link to websites we do not control. We are not responsible
      for their content or their privacy practices, and this policy does not apply
      to them.</p>

      <h2>Changes to this policy</h2>
      <p>We may update this policy as the site or the firm's practices change. The
      date at the top shows when it was last revised. Material changes will be
      reflected here, and continued use of the site after a change indicates
      acceptance of the revised policy.</p>
"""

DISCLAIMER = """      <h2>This website is not legal advice</h2>
      <p>Everything published on www.jayhutchlaw.com is general information about
      the law. It is not legal advice, and it is not a substitute for advice from a
      lawyer who knows the facts of your situation.</p>
      <p>The law changes, and its application depends on details that a website
      cannot know — the charge, the court, the county, your history, and precisely
      what happened. Do not act or refrain from acting on the strength of anything
      you read here. Speak to a lawyer about your own matter.</p>

      <h2>No attorney-client relationship</h2>
      <p>Reading this website, submitting a form, sending an email, or speaking
      with the firm about a possible matter <strong>does not create an
      attorney-client relationship</strong>. That relationship is formed only when
      the firm and the client have both signed a written engagement agreement.</p>
      <p>Until that has happened, the firm has not agreed to act for you, is not
      responsible for your matter, and is not tracking your deadlines.</p>

      <h2>Information you send is not privileged</h2>
      <p>Information you send before an engagement agreement is signed is not
      protected by the attorney-client privilege. The firm may already act for
      someone with interests adverse to yours, which could prevent us from acting
      for you and could affect how unsolicited information must be handled. Please
      send only what is needed to describe the nature of your enquiry.</p>

      <h2>Deadlines are your responsibility until we are engaged</h2>
      <p>Legal matters carry deadlines that cannot be extended once they pass.
      Court dates, response dates, filing deadlines, statutes of limitation, and
      licence-related time limits all continue to run while you are waiting to
      hear from us.</p>
      <p><strong>Contacting the firm does not pause, extend, or protect any
      deadline.</strong> If a date appears on a citation, a summons, or any notice
      you have received, meet it. If a deadline is close, telephone the office at
      <a class="text-link" href="tel:%s">%s</a> rather than waiting on a reply to a
      web form.</p>

      <h2>No guarantee of results</h2>
      <p>Every matter is different, and the outcome of one says nothing about the
      outcome of another. Nothing on this website is a promise, guarantee, warranty,
      or prediction about the result of any legal matter.</p>

      <h2>Attorney advertising</h2>
      <p>This website may be considered attorney advertising in some jurisdictions.
      It is published by Jay Hutch Law, whose office is at 3355 Lenox Road NE,
      Suite 750, Atlanta, Georgia 30326. James Hutchins is the attorney responsible
      for its content.</p>

      <h2>Where the firm is licensed</h2>
      <p>The firm's attorneys are licensed to practise in the State of Georgia.
      Nothing on this site is an offer to represent you in a jurisdiction where the
      firm is not licensed, or where this website would not comply with that
      jurisdiction's rules. Immigration matters are governed by federal law, which
      applies regardless of the state you live in.</p>
      <p>Describing an area as a practice area of the firm is not a claim of
      certification or specialisation in that area.</p>

      <h2>Accuracy and currency</h2>
      <p>We aim to keep the information here accurate, but we do not warrant that
      it is complete, current, or free of error. Statutes are amended, rules change,
      and courts reach new decisions. Material on this site may not reflect the most
      recent developments.</p>

      <h2>Links to other websites</h2>
      <p>Links to third-party websites are provided for convenience. The firm does
      not endorse, control, or take responsibility for their content.</p>

      <h2>Limitation of liability</h2>
      <p>To the fullest extent permitted by law, Jay Hutch Law is not liable for any
      loss or damage arising from your use of, or reliance on, this website or its
      content.</p>
""" % (TEL, PHONE)


if __name__ == "__main__":
    write("/privacy/", page(
        "Privacy Policy | Jay Hutch Law",
        "How Jay Hutch Law collects, uses, stores, and protects information submitted through this website.",
        "/privacy/", "Privacy Policy", "Privacy Policy",
        "What this website collects, why, who processes it, and what choices you have.",
        PRIVACY))
    write("/disclaimer/", page(
        "Disclaimer | Jay Hutch Law",
        "Legal notices and attorney advertising disclosures for the Jay Hutch Law website.",
        "/disclaimer/", "Disclaimer", "Disclaimer",
        "Please read these notices before relying on anything published here.",
        DISCLAIMER))
    print("  privacy/index.html")
    print("  disclaimer/index.html")
