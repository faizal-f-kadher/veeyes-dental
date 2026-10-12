#!/usr/bin/env python3
"""Generate the Veeyes Dental static site into ./site  (python build.py)"""
import html, json, os, shutil
from urllib.parse import quote
from content import *
from icons import sprite, ic, TX_ICON, WHY_ICON, HOSPITAL_ICON, TOOTH

BAND_ART = '<svg class="band__art" viewBox="2 3 20 13" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-width=".14" stroke-linecap="round"><path d="M4 15c0-5.6 3.6-10 8-10s8 4.4 8 10"/><path d="M7.5 15c0-3.8 2-6.8 4.5-6.8s4.5 3 4.5 6.8"/><path d="M4.27 12.41L7.65 13.24"/><path d="M5.07 10.00L8.10 11.60"/><path d="M6.34 7.93L8.82 10.19"/><path d="M8.00 6.34L9.75 9.11"/><path d="M9.93 5.34L10.84 8.43"/><path d="M12.00 5.00L12.00 8.20"/><path d="M14.07 5.34L13.16 8.43"/><path d="M16.00 6.34L14.25 9.11"/><path d="M17.66 7.93L15.18 10.19"/><path d="M18.93 10.00L15.90 11.60"/><path d="M19.73 12.41L16.35 13.24"/></g><path d="M2.6 15h18.8" stroke="var(--cyan)" stroke-width=".18" stroke-linecap="round" opacity=".55"/></svg>'

# original 404 illustration: a tooth under a magnifying glass
LOST_SVG = f'''<svg class="lost" viewBox="0 0 220 180" aria-hidden="true" focusable="false">
  <ellipse cx="104" cy="164" rx="70" ry="8" fill="var(--mist)"/>
  <path d="{TOOTH}" transform="translate(34 6) scale(6.2)" fill="#fff" stroke="var(--navy)" stroke-width=".32" stroke-linejoin="round"/>
  <path d="M74 48c2-6 6-9 12-9" transform="translate(0 4)" fill="none" stroke="var(--cyan)" stroke-width="2.4" stroke-linecap="round"/>
  <circle cx="150" cy="78" r="30" fill="rgba(18,194,210,.12)" stroke="var(--navy)" stroke-width="3"/>
  <path d="M171 100l26 26" stroke="var(--navy)" stroke-width="9" stroke-linecap="round"/>
  <path d="M146 70a9 9 0 1 1 9 10v5" fill="none" stroke="var(--cyan)" stroke-width="4" stroke-linecap="round"/>
  <circle cx="155" cy="94" r="2.6" fill="var(--cyan)"/>
</svg>'''

OUT = "site"
import hashlib
ASSET_V = hashlib.md5(open("static/css/site.css","rb").read() + open("static/js/site.js","rb").read()).hexdigest()[:8]
DOMAIN = "https://www.veeyesdental.com"
esc = html.escape
META = json.load(open("meta.json")) if os.path.exists("meta.json") else {}
CO, TI = CLINICS
GROUP_NAME = dict(GROUPS)
def by_group(g): return [x for x in T if x["group"] == g]

# ------------------------------------------------------------------ icons (inline SVG, stroke = currentColor)
_P = {
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "chev": '<path d="m6 9 6 6 6-6"/>',
 "plus": '<path d="M12 5v14M5 12h14"/>',
 "menu": '<path d="M4 8h16M4 16h16"/>',
 "close": '<path d="M6 6l12 12M18 6 6 18"/>',
 "knob": '<path d="m9 6-6 6 6 6M15 6l6 6-6 6"/>',
 "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
 "chat": '<path d="M20 11.5a8.5 8.5 0 0 1-12.6 7.4L3 20l1.2-4.2A8.5 8.5 0 1 1 20 11.5Z"/>',
 "pin": '<path d="M12 21s-7-6.1-7-11a7 7 0 0 1 14 0c0 4.9-7 11-7 11Z"/><circle cx="12" cy="10" r="2.5"/>',
 "cal": '<rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
}
def icon(name, cls="i"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_P[name]}</svg>'
QUOTE = '<svg class="quote-mark" viewBox="0 0 32 32" fill="currentColor" aria-hidden="true"><path d="M13 8H7a3 3 0 0 0-3 3v6a3 3 0 0 0 3 3h3v1a3 3 0 0 1-3 3H6v3h1a6 6 0 0 0 6-6zM28 8h-6a3 3 0 0 0-3 3v6a3 3 0 0 0 3 3h3v1a3 3 0 0 1-3 3h-1v3h1a6 6 0 0 0 6-6z"/></svg>'
ARROW = icon("arrow")

# ------------------------------------------------------------------ media helpers
def _local_meta(url):
    if url.startswith("assets/") and url not in META:
        from PIL import Image as _I
        with _I.open(os.path.join("static", url[len("assets/"):])) as im:
            META[url] = {"w": im.width, "h": im.height, "grid": [], "avg": "#e6eff0"}
    return META.get(url, {})

def img(url, alt, eager=False, sizes=None, extra="", depth=0):
    m = _local_meta(url)
    src = ("../" * depth + url) if url.startswith("assets/") else url
    wh = f' width="{m["w"]}" height="{m["h"]}"' if m else ""
    load = ' fetchpriority="high"' if eager else ' loading="lazy"'
    sz = f' sizes="{sizes}"' if sizes else ""
    return f'<img src="{esc(src)}" alt="{esc(alt)}"{wh}{load} decoding="async"{sz}{extra}>'

def media(url, alt, cls="", eager=False, style=""):
    bg = META.get(url, {}).get("avg", "#d9e3e5")
    return f'<div class="media {cls}" style="background-color:{bg};{style}">{img(url, alt, eager)}</div>'

def photo(key, cls="", eager=False):
    return media(PH[key], PH_ALT[key], cls, eager)

def video(key, vid_id=None, cls=""):
    v = VIDEO[key]
    bg = META.get(v["poster"], {}).get("avg", "#18384a")
    i = f' id="{vid_id}"' if vid_id else ""
    return (f'<div class="media {cls}" style="background-color:{bg}"><video{i} data-src="{v["src"]}" data-src-small="{v["small"]}" '
            f'poster="{v["poster"]}" muted loop playsinline preload="none" aria-hidden="true" tabindex="-1"></video></div>')

def href(slug, depth): return "../" * depth + slug + ".html"

# ------------------------------------------------------------------ head / header / footer
FONT_PRELOAD = ["lexend-latin-300-normal.woff2", "figtree-latin-400-normal.woff2"]
def head(title, desc, path, depth, og_img=None, extra_head=""):
    p = "../" * depth
    canon = DOMAIN + ("/" if path == "index" else "/" + path)
    pre = "".join(f'<link rel="preload" href="{p}assets/fonts/{f}" as="font" type="font/woff2" crossorigin>' for f in FONT_PRELOAD)
    return f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Veeyes Dental Hospital">
<meta property="og:locale" content="en_IN">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{esc(og_img or PH['reception'])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#18384a">
<link rel="icon" href="{LOGO_FAVICON}">
<link rel="apple-touch-icon" href="{LOGO_FAVICON}">
{pre}
<script>(function(d){{if(!window.matchMedia||matchMedia("(prefers-reduced-motion: reduce)").matches||!("IntersectionObserver" in window))return;d.classList.add("motion");setTimeout(function(){{if(!window.__vyMotion)d.classList.remove("motion")}},2500)}})(document.documentElement)</script>
<link rel="stylesheet" href="{p}assets/css/site.css?v={ASSET_V}">
{extra_head}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{sprite()}
"""

def mega_cols(depth, cur_slug):
    out = ""
    for g, gname in GROUPS:
        lis = "".join(f'<li><a href="{href(x["slug"], depth)}"{" aria-current=\"page\"" if x["slug"] == cur_slug else ""}>{ic(TX_ICON[x["slug"]])}{esc(x["name"])}</a></li>' for x in by_group(g))
        out += f'<div class="mega__col"><h2>{esc(gname)}</h2><ul>{lis}</ul></div>'
    return out

def header(depth, current="", cur_slug=""):
    p = "../" * depth
    def cur(k): return ' aria-current="page"' if current == k else ""
    links = [("about", "About"), ("smile-gallery", "Smile Gallery"), ("clinic-gallery", "Hospital"), ("blog", "Blog"), ("contact", "Contact")]
    nav = "".join(f'<a class="nav__link" href="{p}{k}.html"{cur(k)}>{n}</a>' for k, n in links)
    dgroups = "".join(f'<h2>{esc(gn)}</h2>' + "".join(f'<a href="{href(x["slug"], depth)}">{ic(TX_ICON[x["slug"]])}{esc(x["name"])}</a>' for x in by_group(g)) for g, gn in GROUPS)
    dlinks = "".join(f'<a href="{p}{k}.html"{cur(k)}>{n}</a>' for k, n in links)
    tel = lambda c, i=0: f'<a href="tel:{c["phones"][i][1]}">{c["phones"][i][0]}</a>'
    return f"""<div class="topbar"><div class="wrap">
  <ul class="topbar__list"><li><b>Coimbatore</b>{tel(CO)} · {tel(CO,1)}</li><li><b>Tiruppur</b>{tel(TI)} · {tel(TI,1)}</li></ul>
  <ul class="topbar__list">{''.join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u in SOCIAL)}</ul>
</div></div>
<header class="header">
  <div class="wrap header__bar">
    <a class="brand" href="{p}index.html"><img src="{LOGO}" alt="Veeyes Dental Hospital home" width="640" height="259"></a>
    <nav class="nav" aria-label="Main">
      <div class="nav__item"><button class="nav__link{' is-current' if current == 'treatments' else ''}" type="button" aria-expanded="false" aria-controls="mega" data-mega-trigger>Treatments {icon('chev')}</button></div>
      {nav}
    </nav>
    <a class="btn header__cta" href="{p}appointment.html">Book appointment</a>
    <button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="drawer" data-drawer-open>{icon('menu')}</button>
  </div>
  <div class="mega" id="mega" hidden>
    <div class="wrap"><div class="mega__grid">{mega_cols(depth, cur_slug)}</div>
      <div class="mega__foot"><span class="muted">Not sure which treatment you need? A consultation is the place to start.</span><a class="more" href="{p}treatments.html">All treatments {ARROW}</a></div></div>
  </div>
</header>
<div class="drawer" id="drawer" role="dialog" aria-modal="true" aria-label="Menu" hidden>
  <div class="drawer__top"><img src="{LOGO}" alt="Veeyes Dental Hospital" width="640" height="259"><button class="burger" type="button" aria-label="Close menu" data-drawer-close>{icon('close')}</button></div>
  <nav class="drawer__nav" aria-label="Mobile">
    <a href="{p}index.html"{cur('index')}>Home</a>
    <details{' open' if current == 'treatments' else ''}><summary>Treatments {icon('plus')}</summary><div class="drawer__group">{dgroups}<h2>Overview</h2><a href="{p}treatments.html">All treatments</a></div></details>
    {dlinks}
  </nav>
  <div class="drawer__foot">
    <a class="btn btn--block" href="{p}appointment.html">Book appointment</a>
    <div class="drawer__phones"><div>Coimbatore{tel(CO)}</div><div>Tiruppur{tel(TI)}</div></div>
  </div>
</div>
<main id="main">
"""

def actionbar(depth):
    p = "../" * depth
    calls = "".join(f'<a href="tel:{c["phones"][0][1]}">{c["phones"][0][0]} <span>{c["city"]}</span></a><a href="tel:{c["phones"][1][1]}">{c["phones"][1][0]} <span>{c["city"]}</span></a>' for c in CLINICS)
    return f"""<div class="actionbar" aria-label="Quick contact">
  <details><summary class="btn btn--line btn--block">{icon('phone')} Call</summary><div class="actionbar__pop">{calls}</div></details>
  <a class="btn btn--line" href="https://wa.me/{CO['whatsapp']}" target="_blank" rel="noopener">{icon('chat')} WhatsApp</a>
  <a class="btn" href="{p}appointment.html">{icon('cal')} Book</a>
</div>"""

def footer(depth):
    p = "../" * depth
    def addr(c):
        return (f'<address><b>{c["city"]}</b><br>{"<br>".join(esc(a) for a in c["address"])}<br>'
                + " · ".join(f'<a href="tel:{t}">{n}</a>' for n, t in c["phones"]) + "</address>")
    top = ["teeth-alignment", "teeth-replacement", "teeth-in-an-hour", "cosmetic-dentistry", "teeth-management", "kids-family-dentistry"]
    tl = "".join(f'<li><a href="{href(s, depth)}">{esc(T_BY[s]["name"])}</a></li>' for s in top)
    return f"""</main>
<footer class="footer"><div class="wrap">
  <div class="footer__top">
    <div class="footer__brand"><img src="{LOGO}" alt="Veeyes Dental Hospital" width="640" height="259" loading="lazy">
      <p>Multi-speciality dental hospital in Coimbatore and Tiruppur, caring for families since 2004.</p></div>
    <div><h2>Treatments</h2><ul>{tl}<li><a href="{p}treatments.html">All treatments</a></li></ul></div>
    <div><h2>Veeyes</h2><ul><li><a href="{p}about.html">About us</a></li><li><a href="{p}about.html#team">Our specialists</a></li><li><a href="{p}clinic-gallery.html">Hospital &amp; facilities</a></li><li><a href="{p}smile-gallery.html">Smile Gallery</a></li><li><a href="{p}blog.html">Blog</a></li><li><a href="{p}contact.html">Contact</a></li></ul></div>
    <div><h2>Visit</h2>{addr(CO)}{addr(TI)}</div>
  </div>
  <div class="footer__bot"><p>© <span id="year">2026</span> Veeyes Dental Care™ · <a href="mailto:{TI['email']}">{TI['email']}</a></p>
    <ul class="footer__social">{''.join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u in SOCIAL)}</ul></div>
</div></footer>
{actionbar(depth)}
<script src="{p}assets/js/site.js?v={ASSET_V}" defer></script>
</body>
</html>
"""

# ------------------------------------------------------------------ components
_n = [0]
def ba(pair, label, cls="", eager=False):
    _n[0] += 1
    b, a = pair
    bg = META.get(b, {}).get("avg", "#2a1d1e")
    return f"""<div class="ba {cls}" style="background-color:{bg}">
  {img(b, label + ", before treatment", eager)}
  {img(a, label + ", after treatment", eager, extra=' class="ba__after"')}
  <span class="ba__tag ba__tag--b">Before</span><span class="ba__tag ba__tag--a">After</span><span class="ba__line"></span>
  <label class="sr-only" for="ba{_n[0]}">Slide to compare before and after: {esc(label)}</label>
  <input id="ba{_n[0]}" type="range" min="0" max="100" value="50">
  <span class="ba__knob">{icon('knob')}</span>
</div>"""

def ba_card(cat, pair, eager=False):
    return f'<figure class="ba-card" data-cat="{esc(cat)}">{ba(pair, cat, eager=eager)}<figcaption>{esc(cat)}</figcaption></figure>'

def sh(title, aside="", label=""):
    lab = f'<p class="label">{esc(label)}</p>' if label else ""
    side = f'<div class="sh__aside">{aside}</div>' if aside else ""
    return f'<div class="sh"><div class="sh__title">{lab}<h2>{title}</h2></div>{side}</div>'

def book_card(depth, title="Book a consultation", button=True):
    p = "../" * depth
    btn = f'<a class="btn btn--cyan btn--block" href="{p}appointment.html">Request an appointment</a>' if button else ""
    ph = "".join(f'<div>{c["city"]}<a href="tel:{c["phones"][0][1]}">{c["phones"][0][0]}</a><a href="tel:{c["phones"][1][1]}">{c["phones"][1][0]}</a></div>' for c in CLINICS)
    return f'<div class="book"><h2>{esc(title)}</h2><p>Tell us what is bothering you and which hospital suits you, and we will arrange a time.</p>{btn}<div class="book__phones">{ph}</div></div>'

def band(depth, title="Healthy teeth, healthy lifestyle", text="Book a consultation at our Coimbatore or Tiruppur hospital. Your dentist will explain your options and costs before any treatment begins.", pic="building"):
    p = "../" * depth
    return f"""<section class="sec sec--tight-top"><div class="wrap"><div class="band">
  <div class="band__copy">{BAND_ART}<h2>{esc(title)}</h2><p>{esc(text)}</p>
    <div class="btns"><a class="btn btn--cyan" href="{p}appointment.html">Book appointment</a><a class="btn btn--line-light" href="{p}contact.html">Find a hospital</a></div></div>
  {photo(pic)}
</div></div></section>"""

def clinic_cards(maps=False):
    out = ""
    for c in CLINICS:
        q = c["map"].split("query=")[1]
        m = (f'<iframe class="clinic__map" title="Map: Veeyes Dental Hospital, {c["city"]}" src="https://www.google.com/maps?q={q}&amp;output=embed" '
             f'loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>') if maps else ""
        phones = "<br>".join(f'<a href="tel:{t}">{n}</a>' for n, t in c["phones"])
        out += f"""<article class="clinic">{m}<div class="clinic__body">
  <div class="clinic__head"><h3><span class="tile">{ic('pin')}</span>{c['city']}</h3><span class="clinic__note">{esc(c['tag'])}</span></div>
  <dl><dt>Address</dt><dd>{'<br>'.join(esc(a) for a in c['address'])}</dd><dt>Phone</dt><dd>{phones}</dd><dt>Email</dt><dd><a href="mailto:{c['email']}">{c['email']}</a></dd></dl>
  <div class="btns"><a class="btn" href="{c['map']}" target="_blank" rel="noopener">{icon('pin')} Directions</a><a class="btn btn--line" href="https://wa.me/{c['whatsapp']}" target="_blank" rel="noopener">{icon('chat')} WhatsApp</a></div>
</div></article>"""
    return f'<div class="clinics">{out}</div>'

def jsonld():
    data = [{"@context": "https://schema.org", "@type": "Dentist", "name": f"Veeyes Dental Hospital, {c['city']}", "url": DOMAIN,
             "logo": LOGO, "image": PH["building"], "telephone": c["phones"][0][1], "email": c["email"],
             "address": {"@type": "PostalAddress", "streetAddress": ", ".join(c["address"][:2]), "addressLocality": c["city"],
                         "addressRegion": "Tamil Nadu", "postalCode": c["address"][-1][-6:], "addressCountry": "IN"},
             "sameAs": [u for _, u in SOCIAL]} for c in CLINICS]
    return f'<script type="application/ld+json">{json.dumps(data)}</script>\n'

def write(path, s):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full) or OUT, exist_ok=True)
    with open(full, "w", encoding="utf-8") as f: f.write(s)

def cases_total(): return sum(len(p) for _, p in GALLERY) + len(SINGLES)

# ------------------------------------------------------------------ home
def home():
    facts = "".join(f"<li><b>{n}</b><span>{esc(l)}</span></li>" for n, l in FACTS)
    pairs = [("Teeth alignment", GALLERY_BY["Teeth alignment"][0]), ("Smile designing", GALLERY_BY["Smile designing"][0]), ("Full mouth rehabilitation", GALLERY_BY["Full mouth rehabilitation"][0])]
    groups = ""
    for g, gn in GROUPS:
        rows = "".join(f'<li><a href="{x["slug"]}.html"><span class="tile">{ic(TX_ICON[x["slug"]])}</span><b>{esc(x["name"])}</b><span>{esc(x["summary"])}</span>{ARROW}</a></li>' for x in by_group(g))
        groups += f'<div class="tx__group"><h3>{esc(gn)}</h3><ul>{rows}</ul></div>'
    why = "".join(f'<li class="wcard"><span class="tile">{ic(k)}</span><h3>{esc(a)}</h3><p>{esc(b)}</p></li>' for (a, b), k in zip(WHY, WHY_ICON))
    leads = "".join(f"""<article class="lead-card">{media(l['img'], l['name'])}
      <div class="lead-card__body"><div><h3>{esc(l['name'])}</h3><p class="role">{esc(l['role'])}</p></div><p class="muted">{esc(l['short'])}</p><a class="more" href="about.html#{'ramesh' if 'Ramesh S' in l['name'] else 'ranjana'}">Full profile {ARROW}</a></div></article>""" for l in LEADS)
    faces = "".join(media(m["img"], "") for m in TEAM[:7])
    def initials(n): return "".join(w[0] for w in n.split()[:2]).upper()
    def rv_foot(n, c, tags):
        t = "".join(f'<li><a href="{h}">{esc(l)}</a></li>' for l, h in tags)
        return f'<figcaption><span class="rv__who"><span class="rv__av" aria-hidden="true">{initials(n)}</span><span><b>{esc(n)}</b>{esc(c)}</span></span><ul class="rv__tags" aria-label="Mentioned">{t}</ul></figcaption>'
    fq, fn, fc, ft = REVIEWS[0]
    rv_feature = f'<figure class="rv__feature">{QUOTE}<blockquote><p>{esc(fq)}</p></blockquote>{rv_foot(fn, fc, ft)}</figure>'
    rv_more = "".join(f'<figure class="rv__card"><blockquote><p>{esc(q)}</p></blockquote>{rv_foot(n, c, t)}</figure>' for q, n, c, t in REVIEWS[1:])
    s = head("Veeyes Dental Hospital | Dentist in Coimbatore & Tiruppur",
             "Multi-speciality dental hospital in Coimbatore and Tiruppur since 2004. Braces and Invisalign, implants, Teeth in an Hour, smile design, laser and pain-free dentistry.",
             "index", 0, extra_head=f'<link rel="preload" as="image" href="{VIDEO["hero"]["poster"]}">\n')
    s += header(0, "index") + jsonld()
    s += f"""
<section class="hero" aria-labelledby="hero-title">
  <div class="hero__media">{video('hero', 'hero-video')}</div>
  <div class="wrap hero__inner">
    <div class="hero__copy">
      <p class="label">Coimbatore · Tiruppur</p>
      <h1 id="hero-title">A better life starts with a <span>beautiful smile</span></h1>
      <p class="lead">A multi-speciality dental hospital where specialists in every field of dentistry work under one roof, guided by a simple idea: healthy teeth make for a healthy lifestyle.</p>
      <div class="btns"><a class="btn btn--cyan" href="appointment.html">Book an appointment</a><a class="btn btn--line-light" href="treatments.html">Explore treatments</a></div>
    </div>
    <div class="hero__foot">
      <ul class="hero__places"><li>Coimbatore · Ganapathy&nbsp; <a href="tel:{CO['phones'][0][1]}">{CO['phones'][0][0]}</a></li><li>Tiruppur · Avinashi Road&nbsp; <a href="tel:{TI['phones'][0][1]}">{TI['phones'][0][0]}</a></li></ul>
    </div>
  </div>
</section>

<section class="facts" aria-label="Veeyes at a glance"><div class="wrap"><ul>{facts}</ul></div></section>

<section class="sec"><div class="wrap split">
  <div class="photo-pair">{photo('operatory_2')}{photo('reception')}</div>
  <div class="prose">
    <h2>Exceptional oral care, held to high standards</h2>
    <p class="lead">Veeyes Dental Care is one of the leading dental hospitals in Tamil Nadu, with specialists covering every dental need in a single facility in Coimbatore and Tiruppur.</p>
    <p>We aim for dental health free from pain and complications, for people from all walks of life. Our dentists keep bringing the best of modern dentistry into everyday practice, we run dental awareness camps across both districts, and we treat overseas patients who fly in every year for their care.</p>
    <p class="muted">Patients regularly travel to us from {', '.join(AREAS[:-1])} and {AREAS[-1]}.</p>
    <p><a class="more" href="about.html">Our story {ARROW}</a></p>
  </div>
</div></section>

<section class="sec sec--mist"><div class="wrap">
  {sh("Before and after", f'<p class="muted">Results from Veeyes patients. Drag the handle on each photo to compare.</p><a class="more" href="smile-gallery.html">See all {cases_total()} cases {ARROW}</a>', "Smile Gallery")}
  <div class="ba-grid ba-grid--home">{''.join(ba_card(c, p) for c, p in pairs)}</div>
</div></section>

<section class="sec sec--navy"><div class="wrap tx">
  <div class="tx__side">
    <p class="label">Treatments</p>
    <h2>Care for every stage of your smile</h2>
    <p class="muted">Each treatment is planned by a specialist in that field, with the rest of our specialists in the same building if you need them.</p>
    {video('treat')}
    <p><a class="more" href="treatments.html">Treatments overview {ARROW}</a></p>
  </div>
  <div class="tx__groups">{groups}</div>
</div></section>

<section class="sec"><div class="wrap">
  {sh("Why patients choose us", '<p class="muted">The reasons patients give for coming back to us, and for bringing their families.</p>', "Why Veeyes")}
  <ul class="wgrid">
    <li class="wgrid__photo">{photo('operatory_wood')}<p class="wgrid__cap">A treatment room at Veeyes</p></li>
    {why}
  </ul>
</div></section>

<section class="sec sec--mist"><div class="wrap">
  {sh("Our chief dental surgeons", '<p class="muted">They lead a team of 22 dental specialists, with a resident medical officer, staff nurse and clinical assistants.</p>', "Specialists")}
  <div class="leads">{leads}</div>
  <div class="team-strip"><div class="team-strip__faces" aria-hidden="true">{faces}</div><a class="more" href="about.html#team">Meet all {len(TEAM) + len(LEADS)} specialists {ARROW}</a></div>
</div></section>

<section class="sec sec--navy"><div class="wrap">
  <div class="rv">
    <div class="rv__intro">
      <p class="label">Reviews</p>
      <h2>What our patients say</h2>
      <p class="muted">In their own words, from families treated at our Coimbatore hospital.</p>
      <p><a class="more" href="{GOOGLE_REVIEWS}" target="_blank" rel="noopener">Read more reviews on Google {ARROW}</a></p>
    </div>
    {rv_feature}
    {photo('waiting', 'rv__photo')}
    <div class="rv__more">{rv_more}</div>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  {sh("Visit us in Coimbatore or Tiruppur", '<a class="more" href="contact.html">Maps and contact details ' + ARROW + '</a>', "Locations")}
  {clinic_cards()}
</div></section>
""" + band(0) + footer(0)
    write("index.html", s)

# ------------------------------------------------------------------ treatment pages
TX_PHOTO = {"invisalign": "waiting_invisalign", "kids-family-dentistry": "kids_stars", "digital-radiography": "cbct",
            "geriatric-dentistry": "operatory_1", "teeth-management": "operatory_3"}

def items_html(items, steps=False):
    if not items: return ""
    if steps: return '<ol class="steps">' + "".join(f"<li><span>{esc(s)}</span></li>" for s in items) + "</ol>"
    if isinstance(items[0], tuple):
        return '<dl class="terms">' + "".join(f"<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>" for a, b in items) + "</dl>"
    return '<ul class="ticks">' + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"

def slugify(s): return "-".join("".join(ch if ch.isalnum() else " " for ch in s.lower()).split())

def treatment(x):
    pairs = [(c, p) for c in x.get("ba", []) for p in GALLERY_BY.get(c, [])]
    if pairs: hero_media = ba(pairs[0][1], x["name"], cls="ph__media", eager=True)
    elif x["slug"] in TX_PHOTO: hero_media = photo(TX_PHOTO[x["slug"]], "ph__media", eager=True)
    else: hero_media = video(x["video"], cls="ph__media")
    blocks, toc = "", []
    for h, paras, items in x["sections"]:
        sid = slugify(h) if h else ""
        steps = x["slug"] == "teeth-management" and h == "Root canal treatment"
        body = "".join(f"<p>{esc(p)}</p>" for p in paras) + items_html(items, steps)
        blocks += f'<section class="block">{f"<h2 id=\"{sid}\">{esc(h)}</h2>" if h else ""}{body}</section>'
        if h: toc.append((sid, h))
    if len(pairs) > 1:
        blocks += f'<section class="block block--wide"><h2 id="results">More results</h2><div class="ba-grid ba-grid--2">{"".join(ba_card(c, p) for c, p in pairs[1:5])}</div><p class="fine">Results vary from patient to patient.</p></section>'
        toc.append(("results", "More results"))
    if x.get("single"):
        src = wix(dict(SINGLES)[x["single"]], 1200)
        blocks += f'<section class="block block--wide"><h2 id="case">From our Smile Gallery</h2>{media(src, x["single"] + ", before and after", style="aspect-ratio:16/9")}<p class="fine">{esc(x["single"])}, before and after. Results vary from patient to patient.</p></section>'
        toc.append(("case", "From our Smile Gallery"))
    toc_html = ('<nav class="toc" aria-label="On this page"><h2>On this page</h2><ol>' + "".join(f'<li><a href="#{i}">{esc(h)}</a></li>' for i, h in toc) + "</ol></nav>") if len(toc) >= 3 else ""
    related = [r for r in by_group(x["group"]) if r["slug"] != x["slug"]]
    if len(related) < 3:
        related += [r for r in T if r["group"] != x["group"] and r["slug"] in ("teeth-replacement", "preventive-dentistry", "cosmetic-dentistry") and r not in related][: 3 - len(related)]
    rel = "".join(f'<li><a href="{r["slug"]}.html"><span class="tile">{ic(TX_ICON[r["slug"]])}</span><b>{esc(r["name"])}</b><span>{esc(r["summary"])}</span></a></li>' for r in related[:4])
    desc = x["lead"] if len(x["lead"]) <= 158 else x["lead"][:155].rsplit(" ", 1)[0] + "…"
    s = head(f'{x["name"]} in Coimbatore & Tiruppur | Veeyes Dental', desc, x["slug"], 0)
    s += header(0, "treatments", x["slug"]) + f"""
<section class="ph"><div class="wrap ph__grid">
  <div class="ph__copy">
    <ol class="crumbs"><li><a href="index.html">Home</a></li><li><a href="treatments.html">Treatments</a></li><li><span aria-current="page">{esc(x['name'])}</span></li></ol>
    <div class="ph__kicker"><span class="tile tile--lg">{ic(TX_ICON[x['slug']])}</span><p class="label">{esc(GROUP_NAME[x['group']])}</p></div>
    <h1>{esc(x['name'])}</h1>
    <p class="lead">{esc(x['lead'])}</p>
    <div class="btns"><a class="btn" href="appointment.html?t={x['slug']}">Book a consultation</a><a class="btn btn--line" href="https://wa.me/{CO['whatsapp']}?text={quote('Hello Veeyes Dental, I have a question about ' + x['name'].lower() + '.')}" target="_blank" rel="noopener">{icon('chat')} Ask on WhatsApp</a></div>
  </div>
  {hero_media}
</div></section>
<section class="sec sec--tight-top"><div class="wrap article">
  <div class="article__main">{blocks}</div>
  <aside class="aside">{toc_html}{book_card(0)}</aside>
</div></section>
<section class="sec sec--mist"><div class="wrap">
  {sh("Related treatments", '<a class="more" href="treatments.html">All treatments ' + ARROW + '</a>')}
  <ul class="cards">{rel}</ul>
</div></section>
""" + footer(0)
    write(x["slug"] + ".html", s)

def treatments_page():
    blurbs = {"straighten": "Braces and aligners for children and adults, and early orthodontics that guides jaw growth.",
              "replace": "Implants, crowns, veneers, fillings and full-mouth rebuilding when teeth are lost or damaged.",
              "cosmetic": "Shape, colour and gum line, planned around your face.",
              "everyday": "Check-ups, gums, root canals and extractions, for children, parents and grandparents.",
              "digital": "The imaging and digital planning behind every treatment we carry out."}
    groups = ""
    for g, gn in GROUPS:
        cards = "".join(f'<li><a href="{x["slug"]}.html"><span class="tile">{ic(TX_ICON[x["slug"]])}</span><b>{esc(x["name"])}</b><span>{esc(x["summary"])}</span></a></li>' for x in by_group(g))
        groups += f'<section class="tgroup"><div class="stack"><h2>{esc(gn)}</h2><p class="muted">{blurbs[g]}</p></div><ul class="cards">{cards}</ul></section>'
    s = head("Dental Treatments | Veeyes Dental Hospital", "Braces and Invisalign, implants, Teeth in an Hour, cosmetic and laser dentistry, root canals, gum care, and kids and family dentistry at Veeyes in Coimbatore and Tiruppur.", "treatments", 0)
    s += header(0, "treatments") + f"""
<section class="ph"><div class="wrap ph__grid">
  <div class="ph__copy">
    <ol class="crumbs"><li><a href="index.html">Home</a></li><li><span aria-current="page">Treatments</span></li></ol>
    <h1>Treatments</h1>
    <p class="lead">From laser dentistry and smile design to microscopic root canals, implant rehabilitation, 3D CBCT scanning and piezo bone surgery, every treatment is available at both our hospitals.</p>
  </div>
  {photo('operatory_4', 'ph__media', eager=True)}
</div></section>
<section class="sec sec--tight-top"><div class="wrap">{groups}</div></section>
""" + band(0) + footer(0)
    write("treatments.html", s)

# ------------------------------------------------------------------ about
def about():
    bios = ""
    for l, anchor in zip(LEADS, ("ramesh", "ranjana")):
        bios += f"""<article class="bio" id="{anchor}">{media(l['img'], l['name'])}
  <div class="prose"><div class="stack" style="gap:.5rem"><h3>{esc(l['name'])}</h3><p class="label">{esc(l['role'])}</p></div>{''.join(f'<p>{esc(b)}</p>' for b in l['bio'])}</div></article>"""
    team = "".join(f'<li>{media(m["img"], m["name"])}<b>{esc(m["name"])}</b><span>{esc(m["role"])}</span></li>' for m in TEAM)
    s = head("About Veeyes Dental Hospital | Our Story & Specialists", "From a three-chair clinic in Tiruppur in 2004 to two dental hospitals with 14 chairs. Meet Dr. Ramesh Shanmugam, Dr. Ranjana Ramesh and our team of specialists.", "about", 0)
    s += header(0, "about") + f"""
<section class="ph"><div class="wrap ph__grid">
  <div class="ph__copy">
    <ol class="crumbs"><li><a href="index.html">Home</a></li><li><span aria-current="page">About</span></li></ol>
    <p class="label">Our story</p>
    <h1>From three chairs to two hospitals</h1>
    <p class="lead">Our first practice, Sanjeevi Dental, opened in Tiruppur in 2004: three dental chairs in 550 sq. ft, founded by Prof. Dr. Ramesh Shanmugam and Dr. Narendran.</p>
  </div>
  {photo('building', 'ph__media', eager=True)}
</div></section>
<section class="sec sec--tight-top"><div class="wrap split split--start">
  <div class="prose">
    <p>When Dr. Ranjana Ramesh joined, the practice grew into the Veeyes Dental Care™ brand. Today it is a one-stop dental hospital with 14 operatory chairs across 6,500 sq. ft in Coimbatore and Tiruppur, staffed by registered dentists, dental technicians and trained clinical staff, and one of the largest dental care providers in both cities.</p>
    <p>Our chief dental surgeons believe a clinic becomes a world-class dental hospital only when it can meet every oral care need in one place. From laser dentistry and smile design to microscopic dentistry, advanced implant rehabilitation, 3D CBCT scanning and piezo bone surgery, we aim for treatment that is comfortable, affordable and pain-free, delivered by specialists working together and backed by a five-step sterilisation protocol.</p>
  </div>
  <div class="mission">
    <div><p class="label">Our mission</p><p>To provide comprehensive, personalised dental care with modern technology, helping patients keep healthy teeth and a healthy lifestyle.</p></div>
    <div><p class="label">Our vision</p><p>To be a world-class dental hospital known for compassionate, patient-centred care, led by a team of dedicated professionals.</p></div>
  </div>
</div></section>
<section class="sec sec--mist" id="specialists"><div class="wrap">
  {sh("Our chief dental surgeons", label="Leadership")}
  {bios}
</div></section>
<section class="sec" id="team"><div class="wrap">
  {sh("Our specialists", '<p class="muted">Endodontists, periodontists, pedodontists, an oral and maxillofacial surgeon, an oral medicine and radiology specialist, and general dentists.</p>', "Team")}
  <ul class="team">{team}</ul>
</div></section>
""" + band(0, pic="front_desk") + footer(0)
    write("about.html", s)

# ------------------------------------------------------------------ smile gallery
def smile_gallery():
    cats = [c for c, _ in GALLERY] + [c for c, _ in SINGLES]
    btns = '<button type="button" data-filter="all" aria-pressed="true">All</button>' + "".join(f'<button type="button" data-filter="{esc(c)}" aria-pressed="false">{esc(c)}</button>' for c in cats)
    cards = "".join(ba_card(c, p, eager=(n < 3)) for n, (c, p) in enumerate((c, p) for c, ps in GALLERY for p in ps))
    singles = "".join(f'<figure class="ba-card" data-cat="{esc(c)}">{media(wix(src, 1200), c + ", before and after", style="aspect-ratio:16/9")}<figcaption>{esc(c)}</figcaption></figure>' for c, src in SINGLES)
    s = head("Smile Gallery | Before & After | Veeyes Dental", "Before and after photos of Veeyes patients: braces, crowns, veneers, Teeth in an Hour, smile design, laser gum treatment and full mouth rehabilitation.", "smile-gallery", 0)
    s += header(0, "smile-gallery") + f"""
<section class="ph"><div class="wrap ph__grid ph__grid--solo"><div class="ph__copy">
  <ol class="crumbs"><li><a href="index.html">Home</a></li><li><span aria-current="page">Smile Gallery</span></li></ol>
  <h1>Smile Gallery</h1>
  <p class="lead">Before and after photos of Veeyes patients, from a single filling to a full mouth rehabilitation. Drag the handle on a photo to compare, or choose a treatment.</p>
</div></div></section>
<section class="sec sec--tight-top"><div class="wrap">
  <div class="filters" role="group" aria-label="Show cases for">{btns}</div>
  <p class="fine" style="margin:-1rem 0 1.25rem" aria-live="polite"><span id="gallery-count">{cases_total()} cases</span></p>
  <div class="ba-grid">{cards}{singles}</div>
  <p class="fine" style="margin-top:2rem">Results vary from patient to patient. Your dentist will explain what to expect in your case.</p>
</div></section>
""" + band(0) + footer(0)
    write("smile-gallery.html", s)

# ------------------------------------------------------------------ hospital
def hospital():
    pics = ["ot", "corridor", "operatory_1", "operatory_3"]
    fac = "".join(f'<article class="facility">{photo(k)}<div class="prose"><div class="ph__kicker"><span class="tile tile--lg">{ic(HOSPITAL_ICON[n])}</span><p class="label">{esc(sub)}</p></div><h2>{esc(h)}</h2>{"".join(f"<p>{esc(p)}</p>" for p in ps)}</div></article>' for n, ((h, sub, ps), k) in enumerate(zip(HOSPITAL, pics)))
    order = ["building", "reception", "front_desk", "waiting_room", "corridor", "operatory_2", "operatory_4", "operatory_wood", "kids_tree", "kids_stars", "cbct", "operatory_1", "operatory_3", "ot", "waiting_invisalign", "signage_night", "waiting"]
    gal = "".join(f'<figure>{media(PH[k], PH_ALT[k])}</figure>' for k in order)
    s = head("Hospital & Facilities | Veeyes Dental Hospital", "Operation theatre for dental treatment under general anaesthesia, surgical ICU, nitrous oxide sedation, five-step sterilisation and 3D CBCT imaging at Veeyes Dental Hospital.", "clinic-gallery", 0)
    s += header(0, "clinic-gallery") + f"""
<section class="ph"><div class="wrap ph__grid">
  <div class="ph__copy">
    <ol class="crumbs"><li><a href="index.html">Home</a></li><li><span aria-current="page">Hospital</span></li></ol>
    <p class="label">Hospital &amp; facilities</p>
    <h1>Hospital care for complex dental treatment</h1>
    <p class="lead">An operation theatre, a surgical ICU and sedation for patients who need more than a dental chair, with the same sterilisation protocol in every room.</p>
  </div>
  {photo('signage_night', 'ph__media', eager=True)}
</div></section>
<section class="sec sec--tight-top"><div class="wrap">{fac}</div></section>
<section class="sec sec--mist"><div class="wrap">
  {sh("Inside our hospitals", label="Photos")}
  <div class="photos">{gal}</div>
</div></section>
""" + band(0) + footer(0)
    write("clinic-gallery.html", s)

# ------------------------------------------------------------------ blog
def render_body(body):
    out = ""
    for kind, v in body:
        if kind == "p": out += f"<p>{esc(v)}</p>"
        elif kind == "h": out += f"<h2>{esc(v)}</h2>"
        elif kind == "ul": out += items_html(v)
        elif kind == "ol": out += '<ol class="steps">' + "".join(f"<li><span><b>{esc(a)}</b>{esc(b)}</span></li>" for a, b in v) + "</ol>"
    return out

def blog():
    items = "".join(f'<li><a href="post/{p["slug"]}.html">{media(p["img"], "")}<div class="stack" style="gap:.5rem"><p class="meta">{p["date"]} · {p["read"]}</p><h2>{esc(p["title"])}</h2><p class="muted">{esc(p["excerpt"])}</p></div></a></li>' for p in POSTS)
    s = head("Dental Health Blog | Veeyes Dental", "Dental health advice from Veeyes Dental: root canals, children's dental hygiene, signs you need a check-up, and how cavities form.", "blog", 0)
    s += header(0, "blog") + f"""
<section class="ph"><div class="wrap ph__grid ph__grid--solo"><div class="ph__copy">
  <ol class="crumbs"><li><a href="index.html">Home</a></li><li><span aria-current="page">Blog</span></li></ol>
  <h1>Blog</h1><p class="lead">Straightforward answers to the questions our dentists hear most often.</p>
</div></div></section>
<section class="sec sec--tight-top"><div class="wrap"><ul class="posts">{items}</ul></div></section>
""" + band(0) + footer(0)
    write("blog.html", s)
    for p in POSTS:
        others = "".join(f'<li><a href="{o["slug"]}.html"><b>{esc(o["title"])}</b><span>{o["read"]}</span></a></li>' for o in POSTS if o is not p)
        s = head(f'{p["title"]} | Veeyes Dental Blog', p["excerpt"], "post/" + p["slug"], 1, og_img=p["img"])
        s += header(1, "blog") + f"""
<section class="ph"><div class="wrap ph__grid ph__grid--solo"><div class="ph__copy">
  <ol class="crumbs"><li><a href="../index.html">Home</a></li><li><a href="../blog.html">Blog</a></li></ol>
  <h1>{esc(p['title'])}</h1><p class="muted">{p['date']} · {p['read']}</p>
</div></div></section>
<section class="sec sec--tight-top"><div class="wrap">
  {media(p['img'], '', 'post-cover', eager=True)}
  <div class="article"><div class="article__main"><div class="block">{render_body(p['body'])}</div>
    <p class="note-box">This article is general information about dental health and is not a substitute for professional advice or diagnosis. Please see your dentist about any condition or treatment.</p></div>
  <aside class="aside">{book_card(1, "Talk to a dentist")}</aside></div>
</div></section>
<section class="sec sec--mist"><div class="wrap">{sh("More from the blog", '<a class="more" href="../blog.html">All articles ' + ARROW + '</a>')}<ul class="cards">{others}</ul></div></section>
""" + footer(1)
        write(f"post/{p['slug']}.html", s)

# ------------------------------------------------------------------ appointment + contact
def appt_form():
    opts = "".join(f'<option value="{esc(x["name"])}" data-slug="{x["slug"]}">{esc(x["name"])}</option>' for x in T)
    copt = "".join(f'<option value="{c["city"]}" data-wa="{c["whatsapp"]}" data-phone="{c["phones"][0][0]}" data-tel="{c["phones"][0][1]}">{c["city"]} · {"Ganapathy" if c is CO else "Avinashi Road"}</option>' for c in CLINICS)
    return f"""<form class="form" id="appt" novalidate>
  <h2>Request an appointment</h2>
  <p class="form__note">When you send this, WhatsApp opens with your details filled in, addressed to the hospital you choose. Send the message there and we will reply to arrange a time.</p>
  <div class="form__row">
    <div class="field"><label for="a-name">Full name</label><input id="a-name" name="name" autocomplete="name" required aria-describedby="a-name-err"><span class="err" id="a-name-err" hidden>Enter your name.</span></div>
    <div class="field"><label for="a-phone">Phone or WhatsApp number</label><input id="a-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required aria-describedby="a-phone-err"><span class="err" id="a-phone-err" hidden>Enter a 10-digit phone number.</span></div>
  </div>
  <div class="form__row">
    <div class="field"><label for="a-clinic">Hospital</label><select id="a-clinic" name="clinic">{copt}</select></div>
    <div class="field"><label for="a-date">Preferred date <span>(optional)</span></label><input id="a-date" name="date" type="date"></div>
  </div>
  <div class="field"><label for="a-treat">Treatment <span>(optional)</span></label><select id="a-treat" name="treatment"><option value="">Not sure yet, or a general check-up</option>{opts}</select></div>
  <div class="field"><label for="a-msg">Anything we should know? <span>(optional)</span></label><textarea id="a-msg" name="message" placeholder="For example: pain in a lower back tooth for three days"></textarea></div>
  <div class="form__actions"><button class="btn" type="submit">{icon('chat')} Continue on WhatsApp</button></div>
  <p class="form__note" id="appt-status" role="status" hidden>WhatsApp should have opened in a new tab. If it didn't, <a href="#">open the message here</a> or call <a data-phone href="tel:{CO['phones'][0][1]}">{CO['phones'][0][0]}</a>.</p>
</form>"""

def contact():
    s = head("Contact Veeyes Dental | Coimbatore & Tiruppur", "Addresses, phone numbers, WhatsApp and directions for Veeyes Dental Hospital in Ganapathy, Coimbatore and on Avinashi Road, Tiruppur.", "contact", 0)
    s += header(0, "contact") + jsonld() + f"""
<section class="ph"><div class="wrap ph__grid ph__grid--solo"><div class="ph__copy">
  <ol class="crumbs"><li><a href="index.html">Home</a></li><li><span aria-current="page">Contact</span></li></ol>
  <h1>Contact us</h1>
  <p class="lead">Call, message us on WhatsApp or visit either hospital. If you are in pain, please call rather than wait for a reply.</p>
</div></div></section>
<section class="sec sec--tight-top"><div class="wrap">{clinic_cards(maps=True)}</div></section>
<section class="sec sec--mist" id="book"><div class="wrap split split--start">
  <div class="prose"><p class="label">Appointments</p><h2>Book a visit online</h2><p>Share a few details and choose a hospital. You can also call either hospital directly on the numbers above.</p></div>
  {appt_form()}
</div></section>
""" + footer(0)
    write("contact.html", s)

def appointment():
    s = head("Book an Appointment | Veeyes Dental", "Request a dental appointment at Veeyes Dental Hospital in Coimbatore or Tiruppur by WhatsApp or phone.", "appointment", 0)
    s += header(0, "appointment") + f"""
<section class="ph"><div class="wrap split split--start">
  <div class="stack-lg">
    <ol class="crumbs"><li><a href="index.html">Home</a></li><li><span aria-current="page">Book an appointment</span></li></ol>
    <h1 style="font-size:var(--t-h1)">Book an appointment</h1>
    <p class="lead muted">Send us your details on WhatsApp and we will arrange a time. Prefer to talk? Call either hospital.</p>
    {book_card(0, "Call a hospital", button=False)}
  </div>
  {appt_form()}
</div></section>
""" + footer(0)
    write("appointment.html", s)

def notfound():
    s = head("Page not found | Veeyes Dental", "This page doesn't exist.", "404", 0, extra_head='<base href="/">\n')
    s += header(0) + f'<section class="sec"><div class="wrap center">{LOST_SVG}<p class="label">Error 404</p><h1 style="font-size:var(--t-h1)">We couldn\'t find that page</h1><p class="muted">It may have moved when we redesigned the website.</p><div class="btns"><a class="btn" href="index.html">Go to the homepage</a><a class="btn btn--line" href="treatments.html">See treatments</a></div></div></section>' + footer(0)
    write("404.html", s)

# ------------------------------------------------------------------ redirects, sitemap, hosting config
OLD = {"copy-of-inflation-facility-1": "invisalign", "copy-of-ot": "clinic-gallery", "copy-of-surgical-icu": "clinic-gallery",
       "copy-of-inflation-facility": "clinic-gallery", "copy-of-digital-radiography": "clinic-gallery", "copy-of-services": "treatments",
       "events-page": "", "services": "treatments", "gallery": "smile-gallery", "book-online": "appointment",
       "service-page/*": "treatments", "booking-calendar/*": "appointment"}
def redirects():
    for old, new in OLD.items():
        if "*" in old: continue
        tgt = (new or "index") + ".html"
        write(old + ".html", f'<!doctype html><meta charset="utf-8"><title>Page moved</title><link rel="canonical" href="{DOMAIN}/{new}"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={tgt}"><p>This page has moved. <a href="{tgt}">Continue</a>.</p>')
    write("_redirects", "".join(f"/{o}  /{n}  301\n" for o, n in OLD.items()))
    write("vercel.json", json.dumps({"cleanUrls": True, "trailingSlash": False,
        "redirects": [{"source": "/" + o.replace("/*", "/:path*"), "destination": "/" + n, "permanent": True} for o, n in OLD.items()]}, indent=2))
    rules = "\n".join(f"RedirectMatch 301 ^/{o.replace('/*', '/.*')}(\\.html)?$ /{n}" for o, n in OLD.items())
    write(".htaccess", f"""# Apache / cPanel hosting
Options -MultiViews
ErrorDocument 404 /404.html
RewriteEngine On
# serve /about from about.html, and send /about.html to /about
RewriteCond %{{THE_REQUEST}} \\s/([^.?\\s]+)\\.html[\\s?] [NC]
RewriteRule ^ /%1 [R=301,L]
RewriteCond %{{REQUEST_FILENAME}} !-d
RewriteCond %{{REQUEST_FILENAME}}.html -f
RewriteRule ^(.+?)/?$ $1.html [L]
# old Wix addresses
{rules}
<IfModule mod_expires.c>
ExpiresActive On
ExpiresByType text/css "access plus 1 month"
ExpiresByType application/javascript "access plus 1 month"
ExpiresByType font/woff2 "access plus 1 year"
ExpiresByType image/jpeg "access plus 1 month"
ExpiresByType image/png "access plus 1 month"
ExpiresByType video/mp4 "access plus 1 month"
</IfModule>
""")

def sitemap():
    urls = ["", "about", "treatments", "smile-gallery", "clinic-gallery", "blog", "contact", "appointment"] + [x["slug"] for x in T] + ["post/" + p["slug"] for p in POSTS]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{DOMAIN}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")

if __name__ == "__main__":
    if os.path.exists(OUT): shutil.rmtree(OUT)
    shutil.copytree("static", os.path.join(OUT, "assets"))
    for f in os.listdir("extra"): shutil.copy(os.path.join("extra", f), OUT)
    os.makedirs(os.path.join(OUT, "_source"), exist_ok=True)
    for f in ("build.py", "content.py", "icons.py", "meta.json", "qa.py", "mshot.py", "serve.sh", "scrape_veeyes.py"):
        if os.path.exists(f): shutil.copy(f, os.path.join(OUT, "_source"))
    for d in ("static", "extra"): shutil.copytree(d, os.path.join(OUT, "_source", d))
    home(); treatments_page(); about(); smile_gallery(); hospital(); blog(); contact(); appointment(); notfound(); redirects(); sitemap()
    for x in T: treatment(x)
    n = sum(len(f) for _, _, f in os.walk(OUT))
    print("built", n, "files")
