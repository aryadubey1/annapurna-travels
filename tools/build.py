#!/usr/bin/env python3
"""Builds the static Annapurna Travels site into ../site (HTML + i18n.js). Run: python3 tools/build.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import S, FLEET, GOOGLE, REVIEWS
import html as H

OUT = os.path.join(os.path.dirname(__file__), '..', 'site')
PHONE, PHONE_TXT, WA = '+919827054100', '+91 98270 54100', '919827054100'
EMAIL = 'info@annapurnatravels.co.in'
IG = 'https://www.instagram.com/annapurna.travels/'
MAP_Q = 'Annapurna+Tour+and+Travels,+Raisen+Road,+Kalpana+Nagar,+Bhopal'
MAP_TERM = 'Annapurna+bus+terminal+bhopal'
SITE = 'https://annapurna.clarifyweb.com'
VER = '6'

def t(k, tag='span', cls='', attrs=''):
    c = f' class="{cls}"' if cls else ''
    return f'<{tag}{c} data-i18n="{k}"{attrs}>{S[k][0]}</{tag}>'

def ph(k):
    return f'placeholder="{S[k][0]}" data-i18n-ph="{k}"'

# ---------- icons (24px stroke, lucide-style)
P = {
 'phone': '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
 'mail': '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
 'pin': '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
 'clock': '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
 'arrow': '<path d="M5 12h14M13 5l7 7-7 7"/>',
 'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
 'x': '<path d="M18 6 6 18M6 6l12 12"/>',
 'globe': '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20"/>',
 'users': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
 'seat': '<path d="M7 3v9a2 2 0 0 0 2 2h7l2 7M7 12H5M9 18h6"/><path d="M16 14v-3a2 2 0 0 0-2-2H9"/>',
 'leaf': '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10Z"/><path d="M2 21c0-3 1.9-5.4 5.1-6"/>',
 'bag': '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 13h18"/>',
 'wave': '<path d="M2 12c2-3 4-3 6 0s4 3 6 0 4-3 6 0M2 18c2-3 4-3 6 0s4 3 6 0 4-3 6 0M2 6c2-3 4-3 6 0s4 3 6 0 4-3 6 0"/>',
 'snow': '<path d="M12 2v20M4.9 4.9l14.2 14.2M2 12h20M4.9 19.1 19.1 4.9"/>',
 'spark': '<path d="M12 3l1.9 5.8L20 10l-6.1 1.2L12 17l-1.9-5.8L4 10l6.1-1.2z"/><path d="M19 17v4M17 19h4"/>',
 'mic': '<rect x="9" y="2" width="6" height="12" rx="3"/><path d="M19 10v1a7 7 0 0 1-14 0v-1M12 18v4"/>',
 'fan': '<circle cx="12" cy="12" r="2"/><path d="M12 10c0-4 1-7 4-7 2 0 3 2 2 4l-4 4M14 12c4 0 7 1 7 4 0 2-2 3-4 2l-4-4M12 14c0 4-1 7-4 7-2 0-3-2-2-4l4-4M10 12c-4 0-7-1-7-4 0-2 2-3 4-2l4 4"/>',
 'box': '<path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="m3 8 9 5 9-5M12 13v8"/>',
 'music': '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>',
 'plug': '<path d="M12 22v-5M9 8V2M15 8V2M18 8v5a6 6 0 0 1-12 0V8z"/>',
 'recline': '<path d="M5 3l3 11h8l2 7M8 14l-2 4M16 10h-6"/>',
 'legs': '<path d="M3 21h18M6 21V8M18 21V8M9 12h6M12 9l3 3-3 3"/>',
 'wifi': '<path d="M5 13a10 10 0 0 1 14 0M8.5 16.5a5 5 0 0 1 7 0M2 9a15 15 0 0 1 20 0"/><circle cx="12" cy="20" r="1"/>',
 'grid': '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
 'gps': '<circle cx="12" cy="12" r="7"/><circle cx="12" cy="12" r="2"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/>',
 'shield': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
 'wrench': '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9z"/>',
 'drop': '<path d="M12 2.7 5.6 9.1a9 9 0 1 0 12.8 0z"/>',
 'parking': '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 17V7h4a3 3 0 0 1 0 6H9"/>',
 'bed': '<path d="M2 4v16M2 8h18a2 2 0 0 1 2 2v10M2 17h20M6 8v9"/>',
 'cal': '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
 'eye': '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>',
 'heart': '<path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/>',
 'brief': '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
 'school': '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
 'route': '<circle cx="6" cy="19" r="3"/><path d="M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15"/><circle cx="18" cy="5" r="3"/>',
 'tag': '<path d="M12.6 2.6A2 2 0 0 0 11.2 2H4a2 2 0 0 0-2 2v7.2a2 2 0 0 0 .6 1.4l8.7 8.7a2.4 2.4 0 0 0 3.4 0l6.6-6.6a2.4 2.4 0 0 0 0-3.4z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
 'check': '<path d="M20 6 9 17l-5-5"/>',
 'plane': '<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>',
 'flag': '<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1zM4 22v-7"/>',
 'insta': '<rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".5"/>',
}
WA_SVG = '<svg class="ic" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4A9.8 9.8 0 1 1 12 21.8zm8.4-18.2A11.8 11.8 0 0 0 1.6 17.9L0 24l6.3-1.6A11.8 11.8 0 0 0 24 12c0-3.2-1.2-6.1-3.5-8.4z"/></svg>'

def ic(name, cls='ic'):
    if name == 'wa': return WA_SVG
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{P[name]}</svg>'

def img(name, alt, cls='', sizes='100vw', eager=False, pos=''):
    st = f' style="object-position:{pos}"' if pos else ''
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img class="{cls}" src="/img/{name}-sm.webp" srcset="/img/{name}-sm.webp 800w, /img/{name}.webp 1600w" '
            f'sizes="{sizes}" alt="{alt}" {load} decoding="async"{st}>')

NAV = [('/', 'nav.home'), ('/about', 'nav.about'), ('/fleet', 'nav.fleet'), ('/features', 'nav.features'),
       ('/group-bookings', 'nav.groups'), ('/terminal', 'nav.terminal'), ('/clients', 'nav.clients'), ('/contact', 'nav.contact')]

def header(active):
    links = ''.join(f'<a href="{h}"{" aria-current=page" if h == active else ""}>{t(k)}</a>' for h, k in NAV)
    return f'''
<a class="skip" href="#main">Skip to content</a>
<header class="hdr" id="hdr">
  <div class="wrap hdr-in">
    <a class="logo" href="/" aria-label="Annapurna Travels, home"><img src="/img/logo.webp" alt="Annapurna Travels" width="132" height="72"></a>
    <nav class="nav" aria-label="Main">{links}</nav>
    <div class="hdr-act">
      <div class="lang" role="group" aria-label="Language">
        <button type="button" data-lang="en" aria-pressed="true">EN</button><button type="button" data-lang="hi" aria-pressed="false" lang="hi">हिं</button>
      </div>
      <a class="btn btn-sm btn-coral hide-sm" href="tel:{PHONE}">{ic('phone')}<span>{PHONE_TXT}</span></a>
      <button class="burger" id="burger" aria-expanded="false" aria-controls="drawer" aria-label="Menu">{ic('menu', 'ic ic-m')}{ic('x', 'ic ic-x')}</button>
    </div>
  </div>
</header>
<div class="drawer" id="drawer" hidden>
  <nav aria-label="Mobile">{links}</nav>
  <div class="drawer-cta">
    <a class="btn btn-coral" href="tel:{PHONE}">{ic('phone')}{t('cta.call')}</a>
    <a class="btn btn-wa" href="https://wa.me/{WA}" target="_blank" rel="noopener">{ic('wa')}{t('cta.whatsapp')}</a>
  </div>
  <p class="drawer-addr">{ic('pin')}{t('addr')}</p>
</div>'''

def footer():
    links = ''.join(f'<li><a href="{h}">{t(k)}</a></li>' for h, k in NAV[1:])
    return f'''
<section class="cta-band">
  <div class="wrap cta-in reveal">
    <div><h2>{t('cta.title')}</h2><p>{t('cta.text')}</p></div>
    <div class="cta-btns">
      <a class="btn btn-coral btn-lg" href="/contact#enquiry">{t('cta.quote')}{ic('arrow')}</a>
      <a class="btn btn-wa btn-lg" href="https://wa.me/{WA}" target="_blank" rel="noopener">{ic('wa')}{t('cta.whatsapp_us')}</a>
    </div>
  </div>
</section>
<footer class="ftr">
  <div class="wrap ftr-grid">
    <div class="ftr-brand">
      <img src="/img/logo.webp" alt="Annapurna Travels" width="150" height="82" loading="lazy">
      <p>{t('ft.about')}</p>
      <a class="ftr-social" href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">{ic('insta')}<span>@annapurna.travels</span></a>
    </div>
    <div><h3>{t('ft.explore')}</h3><ul>{links}</ul></div>
    <div><h3>{t('ft.reach')}</h3>
      <ul class="ftr-contact">
        <li>{ic('pin')}<a href="https://maps.google.com/?q={MAP_Q}" target="_blank" rel="noopener">{t('addr')}</a></li>
        <li>{ic('phone')}<a href="tel:{PHONE}">{PHONE_TXT}</a></li>
        <li>{ic('mail')}<a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li>{ic('clock')}{t('ct.hours.v')}</li>
      </ul>
    </div>
  </div>
  <div class="wrap ftr-base">
    <span>© <span id="yr">2026</span> Annapurna Tour &amp; Travels, Bhopal. {t('ft.rights')}</span>
    <span>Website by <a href="https://clarifyweb.com" target="_blank" rel="noopener">ClarifyWeb</a></span>
  </div>
</footer>
<nav class="mbar" aria-label="Quick contact">
  <a href="tel:{PHONE}">{ic('phone')}{t('cta.call')}</a>
  <a href="https://wa.me/{WA}" target="_blank" rel="noopener" class="mbar-wa">{ic('wa')}{t('cta.whatsapp')}</a>
  <a href="/contact#enquiry" class="mbar-q">{ic('tag')}{t('cta.enquire')}</a>
</nav>
<div class="lb" id="lb" hidden><button class="lb-x" aria-label="Close">{ic('x')}</button><button class="lb-p" aria-label="Previous">‹</button><img alt=""><button class="lb-n" aria-label="Next">›</button></div>'''

LD = {
  "@context": "https://schema.org", "@type": "TravelAgency", "name": "Annapurna Tour and Travels",
  "url": SITE, "logo": SITE + "/img/logo.png", "image": SITE + "/img/hero-sunset.webp",
  "telephone": PHONE, "email": EMAIL, "foundingDate": "1989",
  "address": {"@type": "PostalAddress", "streetAddress": "26, Sahakari Parisar, Raisen Road, Kalpana Nagar",
              "addressLocality": "Bhopal", "addressRegion": "Madhya Pradesh", "postalCode": "462022", "addressCountry": "IN"},
  "sameAs": [IG], "areaServed": "India"}

def page(path, title, desc, body, active, hero_img='hero-sunset'):
    canon = SITE + ('' if path == 'index' else '/' + path)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#16204a">
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/img/{hero_img}.webp"><meta property="og:url" content="{canon}">
<link rel="icon" href="/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Manrope:wght@400;500;600;700;800&family=Noto+Sans+Devanagari:wght@400;500;600;700&family=Tiro+Devanagari+Hindi&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/style.css?v={VER}">
<script>try{{var l=localStorage.getItem('lang');if(l==='hi')document.documentElement.lang='hi'}}catch(e){{}}</script>
<script type="application/ld+json">{json.dumps(LD)}</script>
</head>
<body>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
<script src="/js/i18n.js?v={VER}"></script>
<script src="/js/main.js?v={VER}" defer></script>
</body>
</html>'''

# ---------- shared sections
def page_hero(img_name, eyebrow, title_k, lead_k, pos='center'):
    return f'''
<section class="phero">
  {img(img_name, '', 'phero-img', eager=True, pos=pos)}
  <div class="wrap phero-in">
    <p class="eyebrow light">{t(eyebrow)}</p>
    <h1>{t(title_k)}</h1>
    <p class="lead">{t(lead_k)}</p>
  </div>
</section>'''

def sec_head(eb, title, lead=None, center=False):
    l = f'<p class="lead">{t(lead)}</p>' if lead else ''
    return f'<div class="shead{" center" if center else ""} reveal"><p class="eyebrow">{t(eb)}</p><h2>{t(title)}</h2>{l}</div>'

def quote_form(compact=False, fid='q'):
    trips = [('heart','tc.wedding'),('brief','tc.corp'),('school','tc.school'),('route','tc.tour'),('plane','tc.airport'),('spark','tc.other')]
    trip = ''.join(f'<label class="chip-opt"><input type="radio" name="trip" value="{S[k][0]}"{" checked" if n == 0 else ""}><span>{ic(i)}{t(k)}</span></label>' for n, (i, k) in enumerate(trips))
    vehs = [('v.bus','Bus'),('v.trav','Tempo traveller'),('v.car','Car / SUV'),('v.unsure','Not sure, please suggest')]
    veh = ''.join(f'<label class="veh-opt"><input type="radio" name="vehicle" value="{v}"{" checked" if n == 0 else ""}><span><b data-i18n="{k}">{S[k][0]}</b><small data-i18n="{k}.s">{S[k + ".s"][0]}</small></span></label>' for n, (k, v) in enumerate(vehs))
    extra = '' if compact else f'''
      <label class="fld"><span data-i18n="f.name">{S['f.name'][0]}</span><input name="name" autocomplete="name" required {ph('ph.name')}></label>
      <label class="fld"><span data-i18n="f.phone">{S['f.phone'][0]}</span><input name="phone" type="tel" inputmode="tel" autocomplete="tel" pattern="[0-9+ ]{{10,15}}" required {ph('ph.phone')}></label>
      <label class="fld span2"><span data-i18n="f.msg">{S['f.msg'][0]}</span><textarea name="msg" rows="3"></textarea></label>'''
    return f'''
<form class="qform{' compact' if compact else ''}" id="{fid}" novalidate>
  <fieldset class="fset"><legend data-i18n="f.trip">{S['f.trip'][0]}</legend><div class="chip-row">{trip}</div></fieldset>
  <fieldset class="fset"><legend data-i18n="f.vehicle">{S['f.vehicle'][0]}</legend><div class="veh-row">{veh}</div></fieldset>
  <div class="qgrid">
    <label class="fld"><span data-i18n="f.from">{S['f.from'][0]}</span><span class="inp-ic">{ic('pin')}<input name="from" required autocomplete="address-level2" {ph('ph.from')}></span></label>
    <label class="fld"><span data-i18n="f.to">{S['f.to'][0]}</span><span class="inp-ic">{ic('flag')}<input name="to" required {ph('ph.to')}></span></label>
    <div class="fld"><span data-i18n="f.date">{S['f.date'][0]}</span>
      <span class="datebox">{ic('cal')}<span class="date-txt" data-i18n="f.pick">{S['f.pick'][0]}</span><input name="date" type="date" required aria-label="{S['f.date'][0]}"></span></div>
    <div class="fld"><span data-i18n="f.pax">{S['f.pax'][0]}</span>
      <span class="stepper"><button type="button" data-step="-1" aria-label="{S['f.less'][0]}">−</button><input name="pax" type="number" min="1" max="500" inputmode="numeric" required {ph('ph.pax')}><button type="button" data-step="1" aria-label="{S['f.more_p'][0]}">+</button></span></div>{extra}
  </div>
  <p class="qerr" role="alert" hidden>{t('f.err')}</p>
  <button class="btn btn-wa btn-block" type="submit">{ic('wa')}{t('f.send')}</button>
  {'' if compact else f'<button class="linkbtn" type="button" data-mail>{t("f.email")}</button>'}
</form>'''

def stats():
    items = [('1989', 'st.year'), ('100+', 'st.vehicles'), ('200+', 'st.staff'), ('25+', 'st.clients')]
    return '<section class="stats"><div class="wrap stats-in">' + ''.join(
        f'<div class="stat reveal"><b data-count="{n}">{n}</b>{t(k)}</div>' for n, k in items) + '</div></section>'

def fleet_cards(items):
    out = []
    for fid, cat, en, hi, seats, im, tags in items:
        S[f'fleet.{fid}'] = (en, hi)
        if im and im.startswith('svg:'):
            media = f'<img class="fc-img" src="/img/{im[4:]}.svg" alt="{en}" loading="lazy"><span class="fc-note" data-i18n="fl.illus">{S["fl.illus"][0]}</span>'
        else: media = img(im, en, 'fc-img', sizes='(max-width:700px) 85vw, 400px') if im else \
            f'<div class="fc-ph">{ic("users")}<span data-i18n="fl.photo_soon">{S["fl.photo_soon"][0]}</span></div>'
        chips = ''.join(f'<span class="chip">{x}</span>' for x in tags)
        out.append(f'''<article class="fc reveal" data-cat="{cat}">
  <div class="fc-media">{media}<span class="fc-seats">{ic('seat')}<b>{seats}</b> {t('fl.seats')}</span></div>
  <div class="fc-body"><h3>{t('fleet.' + fid)}</h3><div class="chips">{chips}</div>
  <a class="fc-cta" href="https://wa.me/{WA}?text={en.replace(' ', '%20').replace('×','x')}%20-%20enquiry" target="_blank" rel="noopener" data-vehicle="{en}">{t('cta.enquire')}{ic('arrow')}</a></div>
</article>''')
    return ''.join(out)

def fleet_tabs():
    return '<div class="tabs" role="tablist">' + ''.join(
        f'<button role="tab" data-filter="{f}" aria-selected="{"true" if f == "all" else "false"}">{t(k)}</button>'
        for f, k in [('all', 'fl.all'), ('bus', 'fl.buses'), ('traveller', 'fl.travellers'), ('car', 'fl.cars')]) + '</div>'

FEATS = {
 'outside': [('leaf', 'f.eco'), ('bag', 'f.luggage'), ('wave', 'f.air')],
 'inside': [('snow', 'f.ac'), ('spark', 'f.light'), ('mic', 'f.pa'), ('fan', 'f.fan'), ('box', 'f.overhead'), ('music', 'f.sound')],
 'seat': [('plug', 'f.power'), ('recline', 'f.recline'), ('legs', 'f.legroom'), ('wifi', 'f.wifi'), ('grid', 'f.nomid')],
}
def feat(i, k):
    return f'<div class="feat reveal"><span class="feat-ic">{ic(i)}</span><div><h3>{t(k)}</h3><p>{t(k + ".d")}</p></div></div>'

GALLERY = [('coach-dawn', 'Annapurna coach at dawn'), ('interior-fabric', 'Coach interior with reclining seats'),
           ('coach-orange', 'Orange and white Annapurna tourist coach'), ('interior-purple', 'Business class leather seats'),
           ('coach-road', 'Coach on the highway'), ('interior-blue', 'Night interior with ambient lighting'),
           ('coach-blue', 'Blue and white coach'), ('interior-fabric2', 'Seats with extra legroom'),
           ('bus-red', 'Red Annapurna bus'), ('yard-sunset', 'Buses at the terminal at sunset'),
           ('coach-pair', 'Two Annapurna coaches'), ('bus-side', 'Annapurna bus side view')]
def gallery(items):
    return '<div class="gal">' + ''.join(
        f'<button class="gal-i reveal" data-full="/img/{n}.webp" aria-label="{a}">{img(n, a, sizes="(max-width:700px) 50vw, 33vw")}</button>'
        for n, a in items) + '</div>'

def clients_marquee():
    logos = ''.join(f'<img src="/img/clients/c{i:02d}.webp" alt="" width="140" height="72">' for i in range(1, 27))
    return f'<div class="marq" aria-label="Client logos"><div class="marq-track">{logos}{logos}</div></div>'

G_LOGO = '<svg class="g-logo" viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/><path fill="#FF3D00" d="m6.3 14.7 6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>'
STAR = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 1.5l2.6 5.4 5.9.8-4.3 4.1 1 5.9L10 15l-5.2 2.7 1-5.9L1.5 7.7l5.9-.8z"/></svg>'
def stars(n, frac=None):
    w = (frac if frac is not None else n) / 5 * 100
    return f'<span class="stars" role="img" aria-label="{frac or n} out of 5"><span class="stars-bg">{STAR * 5}</span><span class="stars-fg" style="width:{w:.0f}%">{STAR * 5}</span></span>'

def reviews():
    cards = ''
    for name, n, guide, ctx, text in REVIEWS:
        ini = ''.join(w[0] for w in name.split()[:2])
        body = '</p><p>'.join(H.escape(x) for x in text.split('\n') if x.strip())
        long = ' long' if len(text) > 230 else ''
        g = f' · {t("rv.guide")}' if guide else ''
        cards += f'''<figure class="rv reveal{long}">
  <div class="rv-top">{stars(n)}{G_LOGO}</div>
  <blockquote class="rv-text" lang="en"><p>{body}</p></blockquote>
  {'<button class="rv-more" type="button" aria-expanded="false">' + t('rv.more') + '</button>' if long else ''}
  <figcaption><span class="rv-av">{ini}</span><span><b>{H.escape(name)}</b><small>{H.escape(ctx)}{g}</small></span></figcaption>
</figure>'''
    return f'''
<section class="sec reviews-sec">
  <div class="wrap">
    <div class="rv-head">
      {sec_head('rv.eyebrow', 'rv.title')}
      <a class="g-badge reveal" href="{GOOGLE['url']}" target="_blank" rel="noopener">{G_LOGO}<span class="g-num">{GOOGLE['rating']}</span><span class="g-meta">{stars(4, float(GOOGLE['rating']))}<small>{t('rv.count')}</small></span></a>
    </div>
    <div class="rvs scroller">{cards}</div>
    <div class="rv-foot"><a class="more" href="{GOOGLE['url']}" target="_blank" rel="noopener">{t('rv.all')}{ic('arrow')}</a><small>{t('rv.note')}</small></div>
  </div>
</section>'''

# ---------- pages
def home():
    services = [('heart', 'sv.wed', 'interior-blue'), ('brief', 'sv.corp', 'coach-pair'), ('school', 'sv.school', 'coach-45'), ('route', 'sv.tour', 'dest-ujjain')]
    sv = ''.join(f'''<a class="svc reveal" href="/group-bookings">{img(im, '', 'svc-img', sizes='(max-width:700px) 90vw, 25vw')}
<div class="svc-body"><span class="svc-ic">{ic(i)}</span><h3>{t(k)}</h3><p>{t(k + '.d')}</p></div></a>''' for i, k, im in services)
    dests = [('dest-ujjain', 'ds.ujjain', 'ds.pilgrim', '≈190 km'), ('dest-bandhavgarh', 'ds.bandhavgarh', 'ds.wildlife', '≈500 km'),
             ('dest-mandu', 'ds.mandu', 'ds.heritage', '≈290 km'), ('dest-indore', 'ds.indore', 'ds.city', '≈195 km'),
             ('dest-kanha', 'ds.kanha', 'ds.wildlife', '≈450 km')]
    ds = ''.join(f'''<a class="dest reveal" href="/contact#enquiry" data-to="{S[k][0].split(' ·')[0]}">{img(im, S[k][0], sizes='(max-width:700px) 75vw, 30vw')}
<div class="dest-cap"><span class="chip chip-light">{t(c)}</span><h3>{t(k)}</h3>{f'<small>Bhopal → {km}</small>' if km else ''}</div></a>''' for im, k, c, km in dests)
    why = [('recline', 'f.recline'), ('grid', 'f.nomid'), ('wifi', 'f.wifi'), ('plug', 'f.power'), ('wave', 'f.air'), ('music', 'f.sound'), ('gps', 'f.gps'), ('shield', 'f.drivers')]
    return f'''
<section class="hero">
  {img('coach-50', 'Annapurna Travels coach at sunset', 'hero-img', eager=True, pos='70% 60%')}
  <div class="wrap hero-in">
    <div class="hero-copy">
      <p class="eyebrow light">{t('tag.since')}</p>
      <h1>{t('home.h1')}</h1>
      <p class="lead">{t('home.lead')}</p>
      <div class="hero-btns">
        <a class="btn btn-coral btn-lg" href="#quote">{t('cta.quote')}{ic('arrow')}</a>
        <a class="btn btn-glass btn-lg" href="tel:{PHONE}">{ic('phone')}{PHONE_TXT}</a>
      </div>
    </div>
    <div class="qcard" id="quote">
      <h2>{t('quick.title')}</h2>
      {quote_form(compact=True, fid='qhero')}
      <p class="qnote">{ic('clock')}{t('quick.note')}</p>
    </div>
  </div>
</section>
{stats()}
<section class="sec">
  <div class="wrap">{sec_head('sv.eyebrow', 'sv.title')}<div class="svcs">{sv}</div></div>
</section>
<section class="sec sec-tint">
  <div class="wrap">
    <div class="row-head">{sec_head('fl.eyebrow', 'fl.title', 'fl.lead')}{fleet_tabs()}</div>
    <div class="fleet scroller" id="fleet">{fleet_cards([f for f in FLEET if f[0] in ('b51','b50','b45','b33','t26','c-innova','c-fortuner','c-audi')])}</div>
    <a class="more" href="/fleet">{t('cta.view_fleet')}{ic('arrow')}</a>
  </div>
</section>
<section class="sec">
  <div class="wrap split">
    <div class="split-media reveal">{img('interior-leather', 'Business class leather seats inside an Annapurna coach', 'rounded', sizes='(max-width:900px) 100vw, 50vw')}</div>
    <div>{sec_head('why.eyebrow', 'why.title')}<div class="mini-feats">{''.join(f'<div class="mf reveal">{ic(i)}{t(k)}</div>' for i, k in why)}</div>
    <a class="more" href="/features">{t('nav.features')}{ic('arrow')}</a></div>
  </div>
</section>
<section class="sec sec-dark">
  <div class="wrap">{sec_head('ds.eyebrow', 'ds.title')}<div class="dests scroller">{ds}</div></div>
</section>
<section class="sec">
  <div class="wrap split split-rev">
    <figure class="story-fig reveal">{img('founder-1989', 'Mr. Narendra Ratnawat with one of the first Annapurna buses', 'rounded sepia', sizes='(max-width:900px) 100vw, 45vw')}<figcaption>{t('story.caption')}</figcaption></figure>
    <div class="reveal">
      <p class="eyebrow">{t('story.eyebrow')}</p><h2 class="display">{t('story.title')}</h2>
      <p>{t('story.p1')}</p><p>{t('story.p2')}</p>
      <a class="btn btn-ink" href="/about">{t('cta.our_story')}{ic('arrow')}</a>
    </div>
  </div>
</section>
{reviews()}
<section class="sec sec-tint">
  <div class="wrap">{sec_head('gl.eyebrow', 'gl.title')}{gallery(GALLERY[:8])}</div>
</section>
<section class="sec clients-sec">
  <div class="wrap">{sec_head('cl.eyebrow', 'cl.title', center=True)}</div>
  {clients_marquee()}
  <div class="wrap center"><a class="more" href="/clients">{t('cta.all_clients')}{ic('arrow')}</a></div>
</section>'''

def about():
    tl = [('1989', 'tl.1989'), ('tl.growth', 'tl.grow'), ('tl.trust', 'tl.corp'), ('tl.today_l', 'tl.today')]
    tli = ''.join(f'<li class="reveal"><b>{y if y == "1989" else t(y)}</b><p>{t(k)}</p></li>' for y, k in tl)
    return page_hero('yard-sunset', 'tag.since', 'ab.title', 'ab.lead') + f'''
<section class="sec">
  <div class="wrap split">
    <figure class="story-fig reveal">{img('founder-1989', 'Mr. Narendra Ratnawat with one of the first Annapurna buses', 'rounded sepia', sizes='(max-width:900px) 100vw, 45vw')}<figcaption>{t('story.caption')}</figcaption></figure>
    <div class="prose reveal">
      <h2 class="display">{t('story.title')}</h2>
      <p>{t('story.p1')}</p><p>{t('story.p2')}</p><p>{t('ab.p3')}</p><p>{t('ab.p4')}</p><p>{t('ab.p5')}</p>
      <blockquote>{t('ab.quote')}</blockquote>
    </div>
  </div>
</section>
{stats()}
<section class="sec">
  <div class="wrap">
    <div class="shead reveal"><h2>{t('ab.tl')}</h2></div>
    <ol class="timeline">{tli}</ol>
  </div>
</section>
<section class="sec sec-tint">
  <div class="wrap people">
    <div class="person reveal"><span class="avatar">NR</span><p class="eyebrow">{t('ab.founder')}</p><h3>{t('ab.narendra')}</h3><p>{t('ab.narendra.d')}</p></div>
    <div class="person reveal"><span class="avatar">NR</span><p class="eyebrow">{t('ab.cofounder')}</p><h3>{t('ab.naman')}</h3><p>{t('ab.naman.d')}</p></div>
  </div>
</section>'''

def fleet():
    return page_hero('fleet-line', 'fl.eyebrow', 'fl.title', 'fl.lead') + f'''
<section class="sec">
  <div class="wrap">
    <div class="row-head sticky-tabs">{fleet_tabs()}</div>
    <div class="fleet grid" id="fleet">{fleet_cards(FLEET)}</div>
  </div>
</section>'''

def features():
    blocks = ''
    for key, title, im in [('outside', 'ft.outside', 'coach-dawn'), ('inside', 'ft.inside', 'interior-blue'), ('seat', 'ft.seat', 'interior-purple')]:
        blocks += f'''<div class="fblock">
  <div class="fblock-media reveal">{img(im, '', 'rounded', sizes='(max-width:900px) 100vw, 40vw')}</div>
  <div><h2 class="fblock-t reveal">{t(title)}</h2><div class="feats">{''.join(feat(i, k) for i, k in FEATS[key])}</div></div>
</div>'''
    return page_hero('interior-fabric', 'ft.eyebrow', 'ft.title', 'ft.lead') + f'''
<section class="sec"><div class="wrap fblocks">{blocks}</div></section>
<section class="sec sec-tint"><div class="wrap">{sec_head('gl.eyebrow', 'gl.title')}{gallery([g for g in GALLERY if 'interior' in g[0]] + [GALLERY[0], GALLERY[2]])}</div></section>'''

def groups():
    gtypes = [('heart', 'g.wedding'), ('users', 'g.sports'), ('route', 'g.tourist'), ('brief', 'g.business'), ('heart', 'g.family'),
              ('shield', 'g.scouts'), ('school', 'g.college'), ('wrench', 'g.workers'), ('school', 'g.school'), ('globe', 'g.intl'), ('music', 'g.dance'), ('spark', 'g.more')]
    steps = ''.join(f'<li class="step reveal"><span>{n}</span><h3>{t(f"how.{n}")}</h3><p>{t(f"how.{n}.d")}</p></li>' for n in (1, 2, 3))
    return page_hero('coach-pair', 'nav.groups', 'gr.title', 'gr.lead') + f'''
<section class="sec">
  <div class="wrap split">
    <div class="reveal">
      <p class="lead dark">{t('gr.p')}</p>
      <ul class="ticks">{''.join(f'<li>{ic("check")}{t(k)}</li>' for k in ['gr.b1','gr.b2','gr.b3','gr.b4'])}</ul>
      <a class="btn btn-coral" href="#enquiry">{t('cta.quote')}{ic('arrow')}</a>
    </div>
    <div class="split-media reveal">{img('group', 'Illustration of a group boarding a bus', 'rounded contain', sizes='(max-width:900px) 100vw, 50vw')}</div>
  </div>
</section>
<section class="sec sec-tint">
  <div class="wrap">
    <div class="shead reveal"><h2>{t('gr.types')}</h2><p class="lead">{t('gr.vision')}</p></div>
    <div class="gtypes">{''.join(f'<div class="gt reveal">{ic(i)}{t(k)}</div>' for i, k in gtypes)}</div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="shead reveal"><h2>{t('gr.how')}</h2></div>
    <ol class="steps">{steps}</ol>
  </div>
</section>
{reviews()}
<section class="sec sec-tint" id="enquiry">
  <div class="wrap narrow"><div class="card-form reveal"><h2>{t('ct.form')}</h2>{quote_form(fid='qgroup')}</div></div>
</section>'''

def terminal():
    fs = [('wrench', 'tm.f1'), ('drop', 'tm.f2'), ('parking', 'tm.f3'), ('bed', 'tm.f4'), ('cal', 'tm.f5'), ('eye', 'tm.f6')]
    return page_hero('yard-row', 'nav.terminal', 'tm.title', 'tm.lead') + f'''
<section class="sec">
  <div class="wrap split">
    <div class="reveal"><p class="lead dark">{t('tm.p1')}</p>
      <a class="btn btn-ink" href="https://maps.google.com/?q={MAP_TERM}" target="_blank" rel="noopener">{ic('pin')}{t('cta.directions')}</a></div>
    <div class="split-media reveal">{img('office', 'Annapurna bus terminal office', 'rounded', sizes='(max-width:900px) 100vw, 50vw')}</div>
  </div>
</section>
<section class="sec sec-tint"><div class="wrap"><div class="feats feats-3">{''.join(feat(i, k) for i, k in fs)}</div></div></section>
<section class="sec"><div class="wrap">{sec_head('gl.eyebrow', 'nav.terminal')}{gallery([('yard-sunset','Terminal at sunset'),('garage','Service bay with buses'),('yard-row','Buses parked at the terminal'),('office','Terminal office'),('yard-row2','Rows of buses at the terminal'),('fleet-line','Fleet lined up')])}</div></section>
<section class="sec sec-tint"><div class="wrap">
  <div class="shead reveal"><h2>{t('tm.map')}</h2></div>
  <div class="map reveal"><iframe title="Map: Annapurna Bus Terminal" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q={MAP_TERM}&z=15&output=embed"></iframe></div>
</div></section>'''

def clients():
    logos = ''.join(f'<div class="logo-card reveal"><img src="/img/clients/c{i:02d}.webp" alt="Client logo" loading="lazy"></div>' for i in range(1, 27))
    return page_hero('coach-pair', 'cl.eyebrow', 'cp.title', 'cp.lead') + f'''
<section class="sec"><div class="wrap"><div class="logos">{logos}</div></div></section>'''

def contact():
    return page_hero('office', 'nav.contact', 'ct.title', 'ct.lead') + f'''
<section class="sec">
  <div class="wrap contact">
    <div class="cinfo">
      <a class="ci reveal" href="tel:{PHONE}"><span class="feat-ic">{ic('phone')}</span><div><small>{t('ct.phone')}</small><b>{PHONE_TXT}</b></div></a>
      <a class="ci reveal" href="https://wa.me/{WA}" target="_blank" rel="noopener"><span class="feat-ic wa">{ic('wa')}</span><div><small>{t('cta.whatsapp')}</small><b>{PHONE_TXT}</b></div></a>
      <a class="ci reveal" href="mailto:{EMAIL}"><span class="feat-ic">{ic('mail')}</span><div><small>{t('ct.email')}</small><b>{EMAIL}</b></div></a>
      <a class="ci reveal" href="https://maps.google.com/?q={MAP_Q}" target="_blank" rel="noopener"><span class="feat-ic">{ic('pin')}</span><div><small>{t('ct.office')}</small><b>{t('addr')}</b></div></a>
      <div class="ci reveal"><span class="feat-ic">{ic('clock')}</span><div><small>{t('ct.hours')}</small><b>{t('ct.hours.v')}</b></div></div>
    </div>
    <div class="card-form reveal" id="enquiry"><h2>{t('ct.form')}</h2>{quote_form(fid='qcontact')}</div>
  </div>
</section>
<section class="sec sec-tint"><div class="wrap">
  <div class="map reveal"><iframe title="Map: Annapurna Travels office" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q={MAP_Q}&z=15&output=embed"></iframe></div>
</div></section>'''

PAGES = [
 ('index', '/', 'Annapurna Travels · Bus, Tempo Traveller & Car Rental in Bhopal since 1989', 'Book luxury buses (26–51 seats), tempo travellers and cars in Bhopal for weddings, corporate travel, school transport and tours. Trusted since 1989.', home, 'coach-50'),
 ('about', '/about', 'Our Story · Annapurna Travels, Bhopal', 'From one bus in 1989 to 100+ vehicles: the story of Annapurna Travels, Bhopal.', about, 'founder-1989'),
 ('fleet', '/fleet', 'Fleet · Buses, Tempo Travellers & Cars · Annapurna Travels', '51, 50, 49, 48, 45, 41 and 33 seater coaches, 17–26 seat tempo travellers and cars from Dzire to Audi Q3, in Bhopal.', fleet, 'fleet-line'),
 ('features', '/features', 'Bus Features · Annapurna Travels', 'Reclining leather seats, no middle seats, free Wi-Fi, charging at every seat, air suspension and 360° sound.', features, 'interior-leather'),
 ('group-bookings', '/group-bookings', 'Group Bus Bookings in Bhopal · Annapurna Travels', 'Group buses for weddings, sports teams, corporate events, schools and tours. Get a quote on WhatsApp.', groups, 'coach-pair'),
 ('terminal', '/terminal', 'Annapurna Bus Terminal · Bhopal', 'Our own terminal for maintenance, cleaning and staging. Come and see the buses before you book.', terminal, 'yard-row'),
 ('clients', '/clients', 'Clients · Annapurna Travels', 'P&G, Crompton Greaves, Welspun, Dilip Buildcon, MP Tourism, Sony and more travel with Annapurna.', clients, 'coach-pair'),
 ('contact', '/contact', 'Contact · Annapurna Travels, Bhopal', 'Call or WhatsApp +91 98270 54100. 26, Sahakari Parisar, Raisen Road, Kalpana Nagar, Bhopal.', contact, 'office'),
]

def main():
    for name, path, title, desc, fn, og in PAGES:
        body = fn()
        with open(os.path.join(OUT, name + '.html'), 'w', encoding='utf-8') as f:
            f.write(page(name, title, desc, body, path, og))
    os.makedirs(os.path.join(OUT, 'js'), exist_ok=True)
    with open(os.path.join(OUT, 'js', 'i18n.js'), 'w', encoding='utf-8') as f:
        f.write('window.I18N=' + json.dumps({'en': {k: v[0] for k, v in S.items()}, 'hi': {k: v[1] for k, v in S.items()}}, ensure_ascii=False) + ';\n')
    with open(os.path.join(OUT, 'sitemap.xml'), 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
                ''.join(f'<url><loc>{SITE}{"" if p == "/" else p}</loc></url>' for _, p, *_ in PAGES) + '</urlset>')
    with open(os.path.join(OUT, 'robots.txt'), 'w') as f:
        f.write('User-agent: *\nDisallow: /\n')  # demo: keep out of search until it replaces the live site
    print('built', len(PAGES), 'pages,', len(S), 'strings')

if __name__ == '__main__':
    main()
