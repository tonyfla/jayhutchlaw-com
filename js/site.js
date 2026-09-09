/* Site chrome: mobile nav, scroll reveal, current year.
   No dependencies. Loaded with `defer`. */
(function () {
  'use strict';

  /* --- Mobile navigation --- */
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.querySelector('.site-nav');

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
    });

    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  /* --- Scroll reveal ---
     Progressive enhancement: .reveal starts hidden in CSS, so if
     IntersectionObserver is missing we reveal everything immediately. */
  var revealables = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) {
    revealables.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealables.forEach(function (el) { io.observe(el); });
  }

  /* --- Footer year --- */
  var year = String(new Date().getFullYear());
  document.querySelectorAll('.year').forEach(function (el) { el.textContent = year; });

  /* --- Mark the current page in the nav --- */
  var here = location.pathname.replace(/index\.html$/, '').replace(/\/$/, '') || '/';
  document.querySelectorAll('.site-nav a').forEach(function (a) {
    var href = a.getAttribute('href') || '';
    if (href.charAt(0) === '#') return;
    var path = new URL(href, location.origin + location.pathname).pathname
      .replace(/index\.html$/, '').replace(/\/$/, '') || '/';
    if (path === here) a.setAttribute('aria-current', 'page');
  });
})();
