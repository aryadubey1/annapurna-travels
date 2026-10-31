(function () {
  'use strict';
  var WA = '919827054100', EMAIL = 'info@annapurnatravels.co.in';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var store = { get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
                set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} } };

  /* ---------- language */
  function setLang(lang) {
    var d = (window.I18N || {})[lang]; if (!d) return;
    document.documentElement.lang = lang;
    $$('[data-i18n]').forEach(function (el) { var v = d[el.getAttribute('data-i18n')]; if (v != null) el.innerHTML = v; });
    $$('[data-i18n-ph]').forEach(function (el) { var v = d[el.getAttribute('data-i18n-ph')]; if (v != null) el.placeholder = v; });
    $$('.lang button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.lang === lang)); });
    store.set('lang', lang);
  }
  $$('.lang button').forEach(function (b) { b.addEventListener('click', function () { setLang(b.dataset.lang); }); });
  if (store.get('lang') === 'hi') setLang('hi');

  /* ---------- header + drawer */
  var hdr = $('#hdr'), burger = $('#burger'), drawer = $('#drawer');
  function onScroll() { hdr.classList.toggle('scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  function closeDrawer() { drawer.hidden = true; burger.setAttribute('aria-expanded', 'false'); document.body.classList.remove('locked'); }
  burger.addEventListener('click', function () {
    var open = drawer.hidden; drawer.hidden = !open; burger.setAttribute('aria-expanded', String(open));
    document.body.classList.toggle('locked', open);
  });
  $$('a', drawer).forEach(function (a) { a.addEventListener('click', closeDrawer); });
  window.addEventListener('resize', function () { if (window.innerWidth >= 1180 && !drawer.hidden) closeDrawer(); });

  /* ---------- reveal on scroll */
  var els = $$('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    els.forEach(function (el) { io.observe(el); });
  } else els.forEach(function (el) { el.classList.add('in'); });

  /* ---------- fleet filter */
  $$('.tabs').forEach(function (tabs) {
    var grid = tabs.closest('.wrap').querySelector('.fleet');
    tabs.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      $$('button', tabs).forEach(function (x) { x.setAttribute('aria-selected', String(x === b)); });
      var f = b.dataset.filter;
      $$('.fc', grid).forEach(function (c) { c.hidden = !(f === 'all' || c.dataset.cat === f); if (!c.hidden) c.classList.add('in'); });
      grid.scrollTo && grid.scrollTo({ left: 0, behavior: 'smooth' });
    });
  });

  /* ---------- quote forms → WhatsApp / email */
  function collect(form) {
    var ok = true, data = {};
    $$('input,select,textarea', form).forEach(function (el) {
      var fld = el.closest('.fld'), v = el.value.trim();
      var bad = el.required && (!v || (el.pattern && !new RegExp('^' + el.pattern + '$').test(v)));
      if (fld) fld.classList.toggle('bad', !!bad);
      if (bad) ok = false;
      data[el.name] = v;
    });
    $('.qerr', form).hidden = ok;
    if (!ok) { var first = $('.bad input,.bad select', form); first && first.focus(); }
    return ok ? data : null;
  }
  function message(d) {
    var date = d.date ? new Date(d.date + 'T00:00').toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }) : '';
    var lines = ['Hello Annapurna Travels, I would like a quote.', '',
      'Trip: ' + d.trip, 'Vehicle: ' + d.vehicle, 'Route: ' + d.from + ' → ' + d.to, 'Date: ' + date, 'Passengers: ' + d.pax];
    if (d.name) lines.push('Name: ' + d.name);
    if (d.phone) lines.push('Phone: ' + d.phone);
    if (d.msg) lines.push('', d.msg);
    return lines.join('\n');
  }
  $$('.qform').forEach(function (form) {
    var dt = $('input[type=date]', form); if (dt) dt.min = new Date().toISOString().slice(0, 10);
    form.addEventListener('submit', function (e) {
      e.preventDefault(); var d = collect(form); if (!d) return;
      window.open('https://wa.me/' + WA + '?text=' + encodeURIComponent(message(d)), '_blank', 'noopener');
    });
    var mb = $('[data-mail]', form);
    if (mb) mb.addEventListener('click', function () {
      var d = collect(form); if (!d) return;
      location.href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent('Quote request: ' + d.from + ' to ' + d.to) + '&body=' + encodeURIComponent(message(d));
    });
    $$('input,select', form).forEach(function (el) { el.addEventListener('input', function () { var f = el.closest('.fld'); f && f.classList.remove('bad'); }); });
  });
  // vehicle "Enquire" links carry a ready message
  $$('[data-vehicle]').forEach(function (a) {
    a.href = 'https://wa.me/' + WA + '?text=' + encodeURIComponent('Hello Annapurna Travels, I would like a quote for the ' + a.dataset.vehicle + '.\n\nRoute:\nDate:\nPassengers:');
  });
  // destination cards prefill "To"
  $$('.dest[data-to]').forEach(function (a) {
    a.addEventListener('click', function () { store.set('to', a.dataset.to); });
  });
  var to = store.get('to'), toIn = $('#qcontact input[name=to]');
  if (to && toIn && location.hash === '#enquiry') { toIn.value = to; $('#qcontact select[name=trip]').value = 'Tour / pilgrimage'; }

  /* ---------- lightbox */
  var lb = $('#lb'), lbImg = $('img', lb), items = [], idx = 0;
  function show(i) { idx = (i + items.length) % items.length; lbImg.src = items[idx].dataset.full; lbImg.alt = items[idx].getAttribute('aria-label') || ''; }
  $$('.gal').forEach(function (g) {
    $$('.gal-i', g).forEach(function (b, i) {
      b.addEventListener('click', function () { items = $$('.gal-i', g); show(i); lb.hidden = false; document.body.classList.add('locked'); $('.lb-x', lb).focus(); });
    });
  });
  function closeLb() { lb.hidden = true; document.body.classList.remove('locked'); }
  $('.lb-x', lb).addEventListener('click', closeLb);
  $('.lb-p', lb).addEventListener('click', function () { show(idx - 1); });
  $('.lb-n', lb).addEventListener('click', function () { show(idx + 1); });
  lb.addEventListener('click', function (e) { if (e.target === lb) closeLb(); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { if (!lb.hidden) closeLb(); if (!drawer.hidden) closeDrawer(); }
    if (!lb.hidden && e.key === 'ArrowRight') show(idx + 1);
    if (!lb.hidden && e.key === 'ArrowLeft') show(idx - 1);
  });
  var sx = 0;
  lb.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener('touchend', function (e) { var dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1)); });

  var yr = $('#yr'); if (yr) yr.textContent = new Date().getFullYear();
})();
