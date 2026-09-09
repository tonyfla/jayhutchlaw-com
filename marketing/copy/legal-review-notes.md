Status: DRAFT — for J. Hutchins. Do not publish the site until this is worked through.

# Legal review notes — privacy policy and disclaimer

The two pages are written and live at `/privacy/` and `/disclaimer/` in the
repo. They describe the site's **actual** behaviour accurately — I traced every
statement against the code rather than adapting a template. What follows is
everything I could not decide for you.

Edit the source at `tools/build_legal.py`, then run `python3 tools/build_legal.py`.

---

## Must be resolved before launch

### 1. Advertising and analytics trackers
The privacy policy currently states plainly: *"This site sets no advertising or
analytics cookies of its own."* **That is true today and will stop being true
the moment a Meta Pixel, Google Ads tag, or GA4 is added** — which the ad work
points toward.

A privacy policy that misdescribes tracking is the most common way a firm's own
policy becomes a liability. If pixels are going on, the policy needs rewriting
first, and you likely need a consent banner. Tell me before any tag goes live.

### 2. Text messaging and the consent checkbox
The mobile bar has a **Text** button, and the forms' checkbox reads *"I agree to
be contacted by Jay Hutch Law about my inquiry."*

That covers replying to an enquiry. It is probably **not** the express written
consent the TCPA requires for automated or marketing text messages. If Clio Grow
will send automated SMS follow-ups, the checkbox wording needs to change and the
consent needs to be recorded per-channel. Manual, individual replies to someone
who wrote to you are a different matter.

Confirm what Clio Grow will actually send automatically before the first
campaign runs.

### 3. Georgia Rules of Professional Conduct 7.1–7.5
I have written what is customary; I have not verified it against the current
Georgia rules. Specifically confirm:

- whether the advertising disclosure needs particular wording or placement;
- whether naming you as the attorney responsible for the content is required,
  and whether the wording used is right;
- whether the practice-area descriptions imply specialisation contrary to
  Rule 7.4. The disclaimer includes a line stating they do not.

### 4. Bar admissions
Both pages say the firm's attorneys are *licensed to practise in the State of
Georgia*. Correct it if there are admissions in other states, or before any
federal court worth naming.

### 5. Retention period
The policy says records are kept *"as long as needed"* for response, conflicts
checking, and professional obligations. Some firms prefer a stated period.
Decide which you want; vague is defensible, specific is stronger.

---

## Decide, but not blocking

### 6. Naming the processors
The policy names **Clio Grow** and **Cloudflare** explicitly. That is more
transparent than most firms are, and it is accurate. If you would rather
describe them generically ("our client intake provider"), say so — but naming
them is the better position if a client ever asks where their data went.

### 7. Out-of-state and international enquiries
The policy says that where a privacy law gives someone specific rights, we
honour them, without naming CCPA/CPRA or GDPR. For a firm this size that is
usually right. Two things could change it:

- meaningful volume of California clients;
- the **immigration practice attracting enquiries from outside the US**, which
  is more likely here than for most Georgia firms.

If either becomes real, the policy needs specific sections.

### 8. Children's age threshold
Set at 13, following COPPA. Some policies use 16. No practical difference for
this firm.

### 9. Case results and testimonials
Neither page addresses them, because the site currently has none. **If results,
testimonials, or reviews are ever added, both pages need updating** and Georgia
imposes specific requirements on how they must be presented.

### 10. Limitation of liability
Standard clause, included. Enforceability varies. Keep or cut as you prefer.

---

## Things I deliberately did not do

- **No claims about the firm I could not verify.** No years of experience, no
  client numbers, no results, no credentials beyond Georgia licensure.
- **No copied template.** Both documents describe this site's real data flow —
  what the forms collect, that attribution is held in session storage and not
  cookies, that uploads go to access-controlled storage and are not public.
- **No implied advice.** The disclaimer states repeatedly that deadlines keep
  running and that contacting the firm does not protect them, because that is
  the failure that actually harms people who use a site like this.

---

## Effective date

Both pages read **9 September 2026**. Change it to the date you actually
publish, in `UPDATED` at the top of `tools/build_legal.py`.
