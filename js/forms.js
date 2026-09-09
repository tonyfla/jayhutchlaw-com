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

  /* --- Validation ------------------------------------------------ */
  function fieldError(input, message) {
    var wrap = input.closest('.field') || input.parentElement;
    var slot = wrap && wrap.querySelector('.field-error');
    input.setAttribute('aria-invalid', message ? 'true' : 'false');
    if (slot) slot.textContent = message || '';
    return !message;
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

    if (input.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value)) {
      return fieldError(input, 'Enter a valid email address.');
    }
    if (input.type === 'tel' && (value.replace(/\D/g, '').length < 10)) {
      return fieldError(input, 'Enter a valid phone number.');
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
      if (hp) payload.delete(hp.name);
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
