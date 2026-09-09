/* Resource guides: print support, and the optional download gate.
   Loaded only on /resources/ pages. */
(function () {
  'use strict';

  /* ---------------------------------------------------------------
     GATING SWITCH

     false = the key-points card is open to everyone (current setting).
     true  = visitors give contact details before it is revealed, which
             creates a Clio Grow lead tagged with the guide they wanted.

     Only this card is ever gated. The article above it always stays open
     and indexable — gating the guide text would remove it from search
     results, which is the entire reason the guide exists.
     --------------------------------------------------------------- */
  var GATE_ENABLED = false;

  var UNLOCKED_KEY = 'jhl_guides_unlocked';

  /* --- Save / print ------------------------------------------------ */
  document.querySelectorAll('[data-print]').forEach(function (button) {
    button.addEventListener('click', function () { window.print(); });
  });

  if (!GATE_ENABLED) return;

  /* --- Already unlocked this session? ------------------------------ */
  var unlocked = false;
  try { unlocked = sessionStorage.getItem(UNLOCKED_KEY) === 'yes'; } catch (e) {}
  if (unlocked) return;

  /* --- Build the gate --------------------------------------------- */
  document.querySelectorAll('[data-gate]').forEach(function (card) {
    var content = card.querySelector('[data-gated-content]');
    if (!content) return;

    var source = card.getAttribute('data-gate');
    content.hidden = true;

    var gate = document.createElement('div');
    gate.className = 'gate';
    gate.innerHTML = [
      '<p class="gate-intro">Tell us where to send it and the summary opens below. ',
      'The full guide above stays free to read either way.</p>',
      '<form class="contact-form stacked" data-lead-form data-source="', source, '" ',
      'data-redirect="#" novalidate>',
      '  <div class="field full"><label>First Name <span class="req">*</span>',
      '    <input name="first_name" data-label="First name" autocomplete="given-name" required></label>',
      '    <span class="field-error" aria-live="polite"></span></div>',
      '  <div class="field full"><label>Last Name <span class="req">*</span>',
      '    <input name="last_name" data-label="Last name" autocomplete="family-name" required></label>',
      '    <span class="field-error" aria-live="polite"></span></div>',
      '  <div class="field full"><label>Email <span class="req">*</span>',
      '    <input name="email" type="email" data-label="Email" autocomplete="email" required></label>',
      '    <span class="field-error" aria-live="polite"></span></div>',
      '  <input type="hidden" name="message" value="Requested the guide summary: ', source, '">',
      '  <div class="hp-field" aria-hidden="true"><input name="company" type="text" tabindex="-1" autocomplete="off" data-honeypot></div>',
      '  <div class="field full"><label class="consent">',
      '    <input name="consent" type="checkbox" value="yes" required data-label="Consent">',
      '    <span>I agree to be contacted and have read the <a href="/privacy/">privacy policy</a>. <span class="req">*</span></span>',
      '  </label><span class="field-error" aria-live="polite"></span></div>',
      '  <button class="button button-gold full" type="submit">Show me the key points</button>',
      '  <div class="form-status full" aria-live="polite"></div>',
      '</form>'
    ].join('');

    content.parentNode.insertBefore(gate, content);

    /* forms.js redirects on success; here we reveal in place instead. */
    gate.querySelector('form').addEventListener('jhl:submitted', function () {
      try { sessionStorage.setItem(UNLOCKED_KEY, 'yes'); } catch (e) {}
      gate.remove();
      content.hidden = false;
      content.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });
  });
})();
