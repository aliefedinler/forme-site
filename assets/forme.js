/* FORME — consent gate + event tracking, shared by Journal pages.
   Same storage key and behaviour as the homepage: no third-party script
   loads until the visitor accepts. */
window.FORME = (function () {
  var GA_ID = 'G-DM67XJS2PV';
  var ADSENSE_ID = 'ca-pub-1368713087096295';
  var STORAGE_KEY = 'forme_consent';
  var DEBUG = false;
  try { DEBUG = new URLSearchParams(window.location.search).has('debug'); } catch (e) {}
  var events = [];

  function readConsent() {
    try { return window.localStorage.getItem(STORAGE_KEY); } catch (e) { return null; }
  }
  function writeConsent(v) {
    try { window.localStorage.setItem(STORAGE_KEY, v); } catch (e) {}
  }

  var gaLoaded = false;
  function loadGA() {
    if (gaLoaded) return;
    gaLoaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID);
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
    if (DEBUG) console.info('[FORME debug] GA4 loaded', GA_ID);
  }

  var adsLoaded = false;
  function loadAds() {
    if (adsLoaded) return;
    adsLoaded = true;
    var a = document.createElement('script');
    a.async = true;
    a.crossOrigin = 'anonymous';
    a.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + ADSENSE_ID;
    document.head.appendChild(a);
    if (DEBUG) console.info('[FORME debug] AdSense loaded', ADSENSE_ID);
  }

  function send(name, payload) {
    var evt = Object.assign({ event: name, at: new Date().toISOString() }, payload || {});
    events.push(evt);
    if (DEBUG) console.info('[FORME debug]', evt.event, evt);
    if (window.gtag) window.gtag('event', name, payload || {});
  }

  return { track: send, events: events, debug: DEBUG, gaId: GA_ID, adsenseId: ADSENSE_ID,
           consent: { read: readConsent, write: writeConsent, load: loadGA, loadAds: loadAds } };
})();

(function () {
  'use strict';
  var track = window.FORME.track;
  var store = window.FORME.consent;

  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-event]');
    if (!el) return;
    var payload = { source: el.getAttribute('data-source') || null };
    var pid = el.getAttribute('data-product');
    if (pid) payload.product_id = pid;
    if (el.tagName === 'A' && el.hostname && el.hostname !== window.location.hostname) {
      payload.destination = el.hostname;
    }
    track(el.getAttribute('data-event'), payload);
  });

  var bar = document.getElementById('consent');
  var accept = document.getElementById('consent-accept');
  var decline = document.getElementById('consent-decline');
  var reopen = document.getElementById('consent-reopen');

  if (bar) {
    var saved = store.read();
    if (saved === 'granted') { store.load(); store.loadAds(); }
    else if (saved !== 'denied') { bar.hidden = false; }

    accept.addEventListener('click', function () {
      store.write('granted'); store.load(); store.loadAds();
      bar.hidden = true; track('consent_granted', {});
      if (reopen) reopen.focus();
    });
    decline.addEventListener('click', function () {
      store.write('denied'); bar.hidden = true;
      if (reopen) reopen.focus();
    });
    if (reopen) reopen.addEventListener('click', function () {
      bar.hidden = false; accept.focus();
    });
  }

  /* article read-depth: fires once when the reader reaches the end of the body copy */
  var end = document.getElementById('article-end');
  if (end && 'IntersectionObserver' in window) {
    var fired = false;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && !fired) {
          fired = true;
          track('article_read_complete', { slug: document.body.getAttribute('data-slug') || null });
          io.disconnect();
        }
      });
    }, { threshold: 0.6 });
    io.observe(end);
  }
})();
