/* Lead capture layer.
   Handles attribution tracking, validation, spam screening, and submission
   to /api/lead (a Cloudflare Pages Function), which forwards to Clio Grow.

   Any <form data-lead-form> on the site is wired automatically.
   Optional attributes:
     data-source       -> Clio Grow `from_source`      (default "website")
     data-matter-type  -> Clio Grow matter type id
     data-redirect     -> success URL (default /thank-you/)
*/
(function () {
  'use strict';

  var ENDPOINT = '/api/lead';
  var ATTRIB_KEY = 'jhl_attribution';
  var MIN_FILL_SECONDS = 3;      // faster than this is almost certainly a bot
  var MAX_FILE_MB = 10;
  var MAX_FILES = 4;

  /* ---------------------------------------------------------------
     Attribution — captured once on first landing and kept for the
     session, so a visitor who arrives on an ad and submits three
     pages later still carries the campaign that brought them.
     --------------------------------------------------------------- */
  function captureAttribution() {
    var stored = null;
    try { stored = JSON.parse(sessionStorage.getItem(ATTRIB_KEY) || 'null'); } catch (e) {}
    if (stored) return stored;

    var params = new URLSearchParams(location.search);
    var data = { landing_page: location.href, referrer: document.referrer || '', captured_at: new Date().toISOString() };

    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'fbclid', 'msclkid']
      .forEach(function (key) {
        var v = params.get(key);
        if (v) data[key] = v;
      });

    try { sessionStorage.setItem(ATTRIB_KEY, JSON.stringify(data)); } catch (e) {}
    return data;
  }

  var attribution = captureAttribution();

  /* --- Email and phone validation ---------------------------------
     Mirrored server-side in functions/api/lead.js. A lead with a mistyped
     email or an unreachable number is worse than no lead: the firm believes
     it has a client to call and cannot reach them.
     ----------------------------------------------------------------- */

  // Domains that people actually mistype, and what they meant.
  var DOMAIN_TYPOS = {
    'gmail.co': 'gmail.com', 'gmial.com': 'gmail.com', 'gmai.com': 'gmail.com',
    'gnail.com': 'gmail.com', 'gmaill.com': 'gmail.com', 'gmail.cm': 'gmail.com',
    'yahoo.co': 'yahoo.com', 'yaho.com': 'yahoo.com', 'yahooo.com': 'yahoo.com',
    'hotmial.com': 'hotmail.com', 'hotmai.com': 'hotmail.com', 'hotmal.com': 'hotmail.com',
    'outlok.com': 'outlook.com', 'outloo.com': 'outlook.com',
    'icloud.co': 'icloud.com', 'iclould.com': 'icloud.com',
    'aol.co': 'aol.com', 'comcast.ent': 'comcast.net', 'bellsouth.ent': 'bellsouth.net'
  };
  var TLD_TYPOS = { con: 'com', cmo: 'com', vom: 'com', comm: 'com', ocm: 'com', ner: 'net', nte: 'net', ogr: 'org' };

  var EMAIL_RE = /^[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*@[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+$/;

  function checkEmail(raw) {
    var value = raw.trim();
    if (value.length > 254) return { ok: false, message: 'That email address is too long.' };
    if (!EMAIL_RE.test(value)) return { ok: false, message: 'Enter a valid email address, like name@example.com.' };

    var at = value.lastIndexOf('@');
    if (value.slice(0, at).length > 64) return { ok: false, message: 'Enter a valid email address.' };

    var domain = value.slice(at + 1).toLowerCase();
    var tld = domain.split('.').pop();
    if (!/^[a-z]{2,24}$/.test(tld)) return { ok: false, message: 'That email address does not have a valid domain.' };

    // Likely typo — offered as a correction, never enforced. Real addresses
    // at odd domains must still be able to submit.
    var suggestion = null;
    if (DOMAIN_TYPOS[domain]) suggestion = DOMAIN_TYPOS[domain];
    else if (TLD_TYPOS[tld]) suggestion = domain.slice(0, -tld.length) + TLD_TYPOS[tld];
    if (suggestion) return { ok: true, suggestion: value.slice(0, at + 1) + suggestion };

    return { ok: true };
  }

  function checkPhone(raw) {
    var digits = raw.replace(/\D/g, '');
    if (digits.length === 11 && digits.charAt(0) === '1') digits = digits.slice(1);

    if (digits.length < 10) return { ok: false, message: 'Enter a 10-digit phone number, including the area code.' };
    if (digits.length > 10) return { ok: false, message: 'That is more digits than a US phone number has.' };

    var npa = digits.slice(0, 3);
    var nxx = digits.slice(3, 6);

    if (npa.charAt(0) < '2') return { ok: false, message: 'An area code cannot start with 0 or 1.' };
    if (nxx.charAt(0) < '2') return { ok: false, message: 'That does not look like a valid phone number.' };
    // N11 codes (411, 911 and the rest) are reserved for services.
    if (npa.charAt(1) === '1' && npa.charAt(2) === '1') return { ok: false, message: 'That is not a valid area code.' };
    if (nxx.charAt(1) === '1' && nxx.charAt(2) === '1') return { ok: false, message: 'That does not look like a valid phone number.' };
    if (/^(\d)\1{9}$/.test(digits)) return { ok: false, message: 'Enter a real phone number we can reach you on.' };
    // 555-0100 to 555-0199 are reserved for fiction.
    if (nxx === '555' && /^01\d\d$/.test(digits.slice(6))) return { ok: false, message: 'Enter a real phone number we can reach you on.' };

    return { ok: true, pretty: '(' + npa + ') ' + nxx + '-' + digits.slice(6), e164: '+1' + digits };
  }

  /* --- Field validation -------------------------------------------- */
  function fieldError(input, message) {
    var wrap = input.closest('.field') || input.parentElement;
    var slot = wrap && wrap.querySelector('.field-error');
    input.setAttribute('aria-invalid', message ? 'true' : 'false');
    if (slot) {
      slot.textContent = message || '';
      slot.classList.remove('is-hint');
    }
    return !message;
  }

  // A "did you mean" offer: advisory, dismissible by ignoring it, and fixable
  // in one click. Announced politely because the slot is already aria-live.
  function fieldHint(input, suggestion) {
    var wrap = input.closest('.field') || input.parentElement;
    var slot = wrap && wrap.querySelector('.field-error');
    input.setAttribute('aria-invalid', 'false');
    if (!slot) return true;
    slot.textContent = '';
    slot.classList.add('is-hint');
    slot.appendChild(document.createTextNode('Did you mean '));
    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'hint-fix';
    button.textContent = suggestion;
    button.addEventListener('click', function () {
      input.value = suggestion;
      validateField(input);
      input.focus();
    });
    slot.appendChild(button);
    slot.appendChild(document.createTextNode('?'));
    return true;
  }

  function validateField(input) {
    var value = (input.value || '').trim();
    var label = input.dataset.label || input.name || 'This field';

    if (input.type === 'checkbox') {
      return input.required && !input.checked
        ? fieldError(input, 'Please check this box to continue.')
        : fieldError(input, '');
    }
    if (input.required && !value) return fieldError(input, label + ' is required.');
    if (!value) return fieldError(input, '');

    if (input.type === 'email') {
      var email = checkEmail(value);
      if (!email.ok) return fieldError(input, email.message);
      if (email.suggestion) return fieldHint(input, email.suggestion);
      return fieldError(input, '');
    }

    if (input.type === 'tel') {
      var phone = checkPhone(value);
      if (!phone.ok) return fieldError(input, phone.message);
      // Normalise on the way out so the CRM receives one consistent shape.
      input.value = phone.pretty;
      return fieldError(input, '');
    }

    return fieldError(input, '');
  }

  function validateForm(form) {
    var ok = true;
    var first = null;
    form.querySelectorAll('input, textarea, select').forEach(function (input) {
      if (input.type === 'file' || input.dataset.honeypot !== undefined) return;
      if (!validateField(input)) {
        ok = false;
        if (!first) first = input;
      }
    });
    if (first) first.focus();
    return ok;
  }

  /* --- Status messaging ------------------------------------------ */
  function setStatus(form, kind, message) {
    var box = form.querySelector('.form-status');
    if (!box) return;
    box.className = 'form-status show is-' + kind;
    box.textContent = message;
    box.setAttribute('role', kind === 'error' ? 'alert' : 'status');
  }

  function clearStatus(form) {
    var box = form.querySelector('.form-status');
    if (box) box.className = 'form-status';
  }

  /* --- File input feedback --------------------------------------- */
  function wireUploads(form) {
    form.querySelectorAll('.upload-box input[type="file"]').forEach(function (input) {
      var box = input.closest('.upload-box');
      var list = form.querySelector('.upload-list');

      input.addEventListener('change', function () {
        var files = Array.prototype.slice.call(input.files || []);
        var problems = [];

        if (files.length > MAX_FILES) problems.push('Please attach no more than ' + MAX_FILES + ' files.');
        files.forEach(function (f) {
          if (f.size > MAX_FILE_MB * 1024 * 1024) problems.push(f.name + ' is larger than ' + MAX_FILE_MB + ' MB.');
        });

        if (problems.length) {
          input.value = '';
          if (list) list.textContent = '';
          setStatus(form, 'error', problems.join(' '));
          return;
        }

        clearStatus(form);
        if (list) {
          list.textContent = files.length
            ? files.length + ' file' + (files.length > 1 ? 's' : '') + ' attached: ' + files.map(function (f) { return f.name; }).join(', ')
            : '';
        }
      });

      ['dragenter', 'dragover'].forEach(function (evt) {
        box.addEventListener(evt, function (e) { e.preventDefault(); box.classList.add('dragover'); });
      });
      ['dragleave', 'drop'].forEach(function (evt) {
        box.addEventListener(evt, function () { box.classList.remove('dragover'); });
      });
    });
  }

  /* --- Submission ------------------------------------------------- */
  var errorSlotSeq = 0;

  /* Link every input to its error slot with aria-describedby.
     aria-invalid alone tells a screen reader something is wrong but not what;
     without this the message is visible only to sighted users. */
  function associateErrors(form) {
    form.querySelectorAll('.field').forEach(function (field) {
      var slot = field.querySelector('.field-error');
      var input = field.querySelector('input, textarea, select');
      if (!slot || !input) return;

      if (!slot.id) slot.id = 'err-' + (++errorSlotSeq);

      var described = (input.getAttribute('aria-describedby') || '').split(/\s+/).filter(Boolean);
      if (described.indexOf(slot.id) === -1) described.push(slot.id);
      input.setAttribute('aria-describedby', described.join(' '));
    });
  }

  function wireForm(form) {
    var loadedAt = Date.now();
    var submitting = false;

    associateErrors(form);
    wireUploads(form);

    form.querySelectorAll('input, textarea, select').forEach(function (input) {
      input.addEventListener('blur', function () { validateField(input); });
      input.addEventListener('input', function () {
        if (input.getAttribute('aria-invalid') === 'true') validateField(input);
      });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (submitting) return;

      // Spam screen 1: hidden field only a bot would fill.
      var hp = form.querySelector('[data-honeypot]');
      if (hp && hp.value) return;

      // Spam screen 2: humans do not complete a form in under 3 seconds.
      if ((Date.now() - loadedAt) / 1000 < MIN_FILL_SECONDS) return;

      if (!validateForm(form)) {
        setStatus(form, 'error', 'Please correct the highlighted fields.');
        return;
      }

      var button = form.querySelector('[type="submit"]');
      var originalText = button ? button.textContent : '';
      submitting = true;
      if (button) { button.disabled = true; button.textContent = 'Sending…'; }
      clearStatus(form);

      var payload = new FormData(form);
      payload.append('_attribution', JSON.stringify(attribution));
      payload.append('_page', location.href);
      payload.append('_source', form.dataset.source || 'website');
      payload.append('_elapsed', String(Math.round((Date.now() - loadedAt) / 1000)));
      if (form.dataset.matterType) payload.append('_matter_type', form.dataset.matterType);

      fetch(ENDPOINT, { method: 'POST', body: payload })
        .then(function (res) {
          return res.json().catch(function () { return {}; }).then(function (body) {
            if (!res.ok) throw new Error(body.message || 'Request failed (' + res.status + ')');
            return body;
          });
        })
        .then(function (body) {
          form.reset();
          var list = form.querySelector('.upload-list');
          if (list) list.textContent = '';

          // Let an in-page handler (the resource gate) react and reveal
          // content instead of navigating away. data-redirect="#" opts out
          // of the redirect entirely.
          form.dispatchEvent(new CustomEvent('jhl:submitted', { detail: body, bubbles: true }));
          if (form.dataset.redirect === '#') {
            submitting = false;
            if (button) { button.disabled = false; button.textContent = originalText; }
            return;
          }
          window.location.assign(form.dataset.redirect || '/thank-you/');
        })
        .catch(function (err) {
          // Never show a false success — a silent failure is a lost client.
          submitting = false;
          if (button) { button.disabled = false; button.textContent = originalText; }
          setStatus(
            form,
            'error',
            'We could not send your message. Please call 855-488-2452 or email contact@jayhutchlaw.com. (' + err.message + ')'
          );
        });
    });
  }

  document.querySelectorAll('form[data-lead-form]').forEach(wireForm);
})();
