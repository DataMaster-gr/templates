#!/usr/bin/env python3
"""Build the multi-page Law Firm template (Greek + English) from one source.

    python3 multipage/law/_src/build.py

Texts live in content_el.py / content_en.py. Header, footer, menus and the
language switch are generated here once, so a change (e.g. a phone number)
applies to every page. Output is plain static HTML next to this folder:
Greek pages at the site root, English pages under en/. Styles and scripts are
in ../assets/. The _src folder is not published on GitHub Pages (Jekyll skips
folders that start with "_"); don't upload it to the client's server either.
"""
import datetime
import html
import json
import pathlib

import content_el
import content_en

SRC = pathlib.Path(__file__).resolve().parent
OUT = SRC.parent
BASE_URL = "https://datamaster-gr.github.io/templates/multipage/law/"  # client's domain when live
PHONE = "+302100000000"
EMAIL = "info@nikolaou-law.example"
MAP_Q = "Akadimias%2C%20Athens"
PHOTO = "https://images.pexels.com/photos/{id}/pexels-photo-{id}.jpeg?auto=compress&amp;cs=tinysrgb&amp;w={w}"
LANGS = ("el", "en")
C = {"el": content_el.C, "en": content_en.C}

# Page key -> output folder per language ("" = site root). Greek URLs use Greek words
# in Latin letters, which helps Greek searches; English pages live under en/.
PATHS = {
    "home": ("", "en/"),
    "areas": ("tomeis/", "en/practice-areas/"),
    "area-family": ("tomeis/oikogeneiako-dikaio/", "en/practice-areas/family-law/"),
    "area-inheritance": ("tomeis/klironomiko-dikaio/", "en/practice-areas/inheritance-law/"),
    "area-realestate": ("tomeis/akinita-misthoseis/", "en/practice-areas/real-estate/"),
    "area-corporate": ("tomeis/etairiko-dikaio/", "en/practice-areas/corporate-law/"),
    "area-employment": ("tomeis/ergatiko-dikaio/", "en/practice-areas/employment-law/"),
    "area-debt": ("tomeis/diekdikisi-apaitiseon/", "en/practice-areas/debt-recovery/"),
    "team": ("omada/", "en/team/"),
    "fees": ("amoives/", "en/fees/"),
    "insights": ("arthra/", "en/insights/"),
    "art-divorce": ("arthra/synainetiko-diazygio/", "en/insights/uncontested-divorce/"),
    "art-inheritance": ("arthra/apodochi-apopoiisi-klironomias/", "en/insights/accepting-renouncing-inheritance/"),
    "art-property": ("arthra/elegchos-akinitou/", "en/insights/property-title-check/"),
    "contact": ("epikoinonia/", "en/contact/"),
}
NAV = ["areas", "team", "fees", "insights", "contact"]

SVG = '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{}</svg>'
ICONS = {
    "family": '<circle cx="8" cy="7" r="2.5"/><circle cx="16" cy="7" r="2.5"/><path d="M3 20c.4-3.6 2.4-6 5-6s4.6 2.4 5 6M11 20c.4-3.6 2.4-6 5-6s4.6 2.4 5 6"/>',
    "inheritance": '<path d="M7 3h8l4 4v14H7z"/><path d="M15 3v4h4M10 12h6M10 16h4"/><path d="M4 7v14"/>',
    "realestate": '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-5h4v5"/>',
    "corporate": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 13h18"/>',
    "employment": '<circle cx="12" cy="7" r="3"/><path d="M5 21c.6-4 3.3-7 7-7s6.4 3 7 7"/><path d="M8.5 5.5h7"/>',
    "debt": '<ellipse cx="9" cy="7" rx="6" ry="2.5"/><path d="M3 7v4c0 1.4 2.7 2.5 6 2.5s6-1.1 6-2.5V7"/><path d="M9 16.5c0 1.4 2.7 2.5 6 2.5s6-1.1 6-2.5v-4c0-1.4-2.7-2.5-6-2.5"/>',
    "phone": '<path d="M5 3h3l2 5-2.5 1.5a11 11 0 0 0 5 5L14 12l5 2v3a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/>',
    "cal": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "scales": '<path d="M12 3v18M7 21h10M5 7h14M12 5l-7 2M12 5l7 2"/><path d="M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "medal": '<circle cx="12" cy="9" r="6"/><path d="M8.5 14 7 21l5-3 5 3-1.5-7"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/>',
    "lock": '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9h8M8 12h5"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.5 2.5L16 9.5"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "doc": '<path d="M14 3H6v18h12V7z"/><path d="M14 3v4h4M9 12h6M9 16h4"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
}
MONTHS = {
    "el": ["Ιανουαρίου", "Φεβρουαρίου", "Μαρτίου", "Απριλίου", "Μαΐου", "Ιουνίου", "Ιουλίου",
           "Αυγούστου", "Σεπτεμβρίου", "Οκτωβρίου", "Νοεμβρίου", "Δεκεμβρίου"],
    "en": ["January", "February", "March", "April", "May", "June", "July", "August",
           "September", "October", "November", "December"],
}


def e(s):
    return html.escape(s, quote=True)


def ic(name):
    return SVG.format(ICONS[name])


def path(key, lang):
    return PATHS[key][LANGS.index(lang)]


def rel(frm, to):
    """Relative link from one page folder to another page folder (or a file)."""
    return "../" * frm.count("/") + to if (to or frm) else "./"


def link(frm, key, lang):
    return rel(frm, path(key, lang)) or "./"


def date(iso, lang):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {MONTHS[lang][d.month - 1]} {d.year}"


def area(lang, key):
    return next(a for a in C[lang]["areas"] if a["key"] == key)


def member(lang, key):
    return next(m for m in C[lang]["team"] if m["key"] == key)


def article(lang, key):
    return next(a for a in C[lang]["articles"] if a["key"] == key)


# ---------------------------------------------------------------- page shell

def head(lang, key, title, desc, jsonld=None):
    cur = path(key, lang)
    alts = "".join(f'\n    <link rel="alternate" hreflang="{l}" href="{BASE_URL}{path(key, l)}">' for l in LANGS)
    ld = ""
    for block in (jsonld or []):
        ld += '\n    <script type="application/ld+json">' + json.dumps(block, ensure_ascii=False) + "</script>"
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Generated by _src/build.py: edit the content files there and rebuild, don't edit this file. -->
    <title>{e(title)}</title>
    <meta name="description" content="{e(desc)}">
    <meta name="theme-color" content="#1C1B1F">
    <link rel="canonical" href="{BASE_URL}{cur}">{alts}
    <link rel="alternate" hreflang="x-default" href="{BASE_URL}{path(key, 'el')}">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{e(title)}">
    <meta property="og:description" content="{e(desc)}">
    <meta property="og:url" content="{BASE_URL}{cur}">
    <meta property="og:image" content="{PHOTO.format(id='6077091', w=1200)}">
    <meta property="og:locale" content="{'el_GR' if lang == 'el' else 'en_GB'}">
    <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%231C1B1F'/%3E%3Ctext x='16' y='22' text-anchor='middle' font-family='Georgia,serif' font-size='17' fill='%23D9B98A'%3EN%3C/text%3E%3C/svg%3E">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@500;600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{rel(cur, 'assets/site.css')}">{ld}
</head>
<body>
"""


def header(lang, key):
    t = C[lang]["ui"]
    cur = path(key, lang)
    active = key if key in NAV else ("areas" if key.startswith("area") else "insights" if key.startswith("art") else "")
    nav = "".join(
        f'<a href="{link(cur, k, lang)}"{" aria-current=\"page\"" if k == active else ""}>{e(t["nav"][k])}</a>' for k in NAV)
    langs = "".join(
        f'<a href="{rel(cur, path(key, l))}" hreflang="{l}" lang="{l}" data-set-lang="{l}"{" aria-current=\"true\"" if l == lang else ""}>{"ΕΛ" if l == "el" else "EN"}</a>'
        for l in LANGS)
    sub = "".join(f'<li class="sub"><a href="{link(cur, "area-" + a["key"], lang)}">{e(a["title"])}</a></li>' for a in C[lang]["areas"])
    mitems = ""
    for k in NAV:
        mitems += f'<li><a href="{link(cur, k, lang)}"{" aria-current=\"page\"" if k == active else ""}>{e(t["nav"][k])}</a></li>'
        if k == "areas":
            mitems += sub
    return f"""
<div class="ribbon">{e(t['ribbon'])} <a href="{rel(cur, '../')}">{e(t['ribbon_link'])}</a></div>

<header class="site-header">
    <div class="wrap">
        <a class="brand" href="{link(cur, 'home', lang)}">
            <span class="brand-mark" aria-hidden="true">N</span>
            <span><span class="brand-name">{e(t['brand'])}</span><span class="brand-sub">{e(t['brand_sub'])}</span></span>
        </a>
        <nav class="nav" aria-label="{e(t['nav_label'])}">{nav}</nav>
        <div class="head-actions">
            <a class="head-phone" href="tel:{PHONE}">{ic('phone')}{e(t['phone_display'])}</a>
            <div class="lang-switch" role="group" aria-label="{e(t['lang_label'])}">{langs}</div>
            <a class="btn btn-ox btn-sm" href="{link(cur, 'contact', lang)}">{e(t['cta'])}</a>
            <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mnav" aria-label="{e(t['menu'])}">{ic('menu')}</button>
        </div>
    </div>
    <nav class="mnav" id="mnav" aria-label="{e(t['nav_label'])}"><ul>{mitems}</ul></nav>
</header>
"""


def footer(lang, key):
    t = C[lang]["ui"]
    cur = path(key, lang)
    priv = rel(cur, "privacy.html") + ("?lang=en" if lang == "en" else "")
    areas = "".join(f'<li><a href="{link(cur, "area-" + a["key"], lang)}">{e(a["title"])}</a></li>' for a in C[lang]["areas"])
    office = "".join(f'<li><a href="{link(cur, k, lang)}">{e(t["nav"][k])}</a></li>' for k in ("team", "fees", "insights"))
    return f"""
<footer>
    <div class="wrap">
        <div class="cols">
            <div>
                <h3>{e(t['f_office'])}</h3>
                <p>{e(t['brand'])}</p>
                <p>{e(t['address'])}</p>
                <ul>{office}</ul>
            </div>
            <div><h3>{e(t['f_areas'])}</h3><ul>{areas}</ul></div>
            <div>
                <h3>{e(t['f_contact'])}</h3>
                <p><a href="tel:{PHONE}">{e(t['phone_display'])}</a></p>
                <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
                <p>{e(t['hours'])}</p>
            </div>
        </div>
        <div class="row">
            <span>&copy; 2026 {e(t['rights'])}</span>
            <span><a href="{priv}">{e(t['privacy'])}</a> · <a href="{priv}#cookies" data-cc="show-preferencesModal">{e(t['cookies'])}</a></span>
            <span>{e(t['demo_by'])} <a href="https://www.datamaster.gr">Data Master</a></span>
        </div>
        <div>{e(t['legal'])}</div>
    </div>
</footer>

<nav class="mbar" aria-label="Quick actions">
    <a href="tel:{PHONE}">{ic('phone')}<span>{e(t['call'])}</span></a>
    <a class="main" href="{link(cur, 'contact', lang)}">{ic('cal')}<span>{e(t['meeting'])}</span></a>
    <a href="mailto:{EMAIL}">{ic('mail')}<span>{e(t['email'])}</span></a>
</nav>

<script src="{rel(cur, 'assets/site.js')}" defer></script>
"""


def page(lang, key, title, desc, body, jsonld=None, extra_scripts=""):
    return head(lang, key, title, desc, jsonld) + header(lang, key) + "\n<main>\n" + body + "\n</main>\n" + footer(lang, key) + extra_scripts + "</body>\n</html>\n"


def crumbs_ld(lang, trail):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": name, "item": BASE_URL + path(k, lang)} for i, (k, name) in enumerate(trail)]}


def page_hero(lang, key, trail, eyebrow, h1, lead, meta=""):
    cur = path(key, lang)
    items = "".join(f'<li><a href="{link(cur, k, lang)}">{e(n)}</a></li>' for k, n in trail[:-1])
    items += f'<li aria-current="page">{e(trail[-1][1])}</li>'
    return f"""
    <section class="page-hero">
        <div class="wrap">
            <ol class="crumbs" aria-label="Breadcrumb">{items}</ol>
            <p class="eyebrow">{e(eyebrow)}</p>
            <h1>{e(h1)}</h1>
            {f'<p class="lead">{e(lead)}</p>' if lead else ''}{meta}
        </div>
    </section>"""


def cta_band(lang, key, area_key=None):
    t = C[lang]["ui"]
    cur = path(key, lang)
    href = link(cur, "contact", lang) + (f"?area={area_key}" if area_key else "")
    return f"""
    <section class="cta-band">
        <div class="wrap">
            <div><h2>{e(t['cta_title'])}</h2><p>{e(t['cta_text'])}</p></div>
            <div class="btns">
                <a class="btn btn-gold" href="{href}">{ic('cal')}{e(t['cta'])}</a>
                <a class="btn btn-line" href="tel:{PHONE}">{ic('phone')}{e(t['phone_display'])}</a>
            </div>
        </div>
    </section>"""


def faq(items, title=None):
    qs = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in items)
    h = f'<h2>{e(title)}</h2>' if title else ""
    return f'{h}<div class="faq">{qs}</div>'


def area_cards(lang, key):
    t = C[lang]["ui"]
    cur = path(key, lang)
    return "".join(
        f'<a class="area" href="{link(cur, "area-" + a["key"], lang)}">{ic(a["icon"])}<h3>{e(a["title"])}</h3><p>{e(a["card"])}</p><span class="go">{e(t["more"])}{ic("arrow")}</span></a>'
        for a in C[lang]["areas"])


def post_cards(lang, key):
    t = C[lang]["ui"]
    cur = path(key, lang)
    out = ""
    for a in C[lang]["articles"]:
        out += (f'<a class="post reveal" href="{link(cur, "art-" + a["key"], lang)}"><span class="cat">{e(area(lang, a["area"])["title"])}</span>'
                f'<h3>{e(a["title"])}</h3><span class="date">{date(a["date"], lang)}</span><p>{e(a["summary"])}</p>'
                f'<span class="more"><span>{e(t["read"])}</span>{ic("arrow")}</span></a>')
    return out


def photo(m, w):
    return PHOTO.format(id=m["photo"], w=w)


# ---------------------------------------------------------------- pages

def build_home(lang):
    c, t, key = C[lang], C[lang]["ui"], "home"
    h = c["home"]
    cur = path(key, lang)
    trust_ic = ["scales", "medal", "globe"]
    trust = "".join(f'<li>{ic(trust_ic[i])}<span>{e(x)}</span></li>' for i, x in enumerate(h["trust"]))
    steps = "".join(f'<li class="reveal"><h3>{e(a)}</h3><p>{e(b)}</p></li>' for a, b in h["steps"])
    ap_ic = ["lock", "chat", "check", "globe"]
    ap = "".join(f'<div class="feat">{ic(ap_ic[i])}<h3>{e(a)}</h3><p>{e(b)}</p></div>' for i, (a, b) in enumerate(h["ap"]))
    team = ""
    for m in c["team"]:
        team += (f'<article class="member reveal"><img src="{photo(m, 700)}" alt="" width="700" height="467" loading="lazy" style="object-position: {m["pos"]}">'
                 f'<div><h3>{e(m["name"])}</h3><p class="r">{e(m["role"])}</p><p class="b">{e(m["short"])}</p></div></article>')
    ld = {"@context": "https://schema.org", "@type": "LegalService", "name": t["brand"], "url": BASE_URL + cur,
          "image": PHOTO.format(id="6077091", w=1200).replace("&amp;", "&"), "telephone": PHONE, "email": EMAIL,
          "address": {"@type": "PostalAddress", "streetAddress": "Akadimias St", "addressLocality": "Athens", "addressRegion": "Attica", "addressCountry": "GR"},
          "areaServed": "GR", "knowsLanguage": ["el", "en"],
          "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "18:00"}]}
    body = f"""
    <section class="hero">
        <img class="hero-bg" src="{PHOTO.format(id='6077091', w=1600)}" alt="" width="1600" height="1066" fetchpriority="high">
        <div class="wrap">
            <p class="eyebrow">{e(h['eyebrow'])}</p>
            <h1>{e(h['h1'])}</h1>
            <p class="lead">{e(h['lead'])}</p>
            <div class="hero-cta">
                <a class="btn btn-gold" href="{link(cur, 'contact', lang)}">{ic('cal')}<span>{e(t['cta'])}</span></a>
                <a class="btn btn-line" href="tel:{PHONE}">{ic('phone')}<span>{e(t['phone_display'])}</span></a>
            </div>
            <ul class="trust">{trust}</ul>
        </div>
    </section>

    <section class="block">
        <div class="wrap">
            <div class="head">
                <p class="eyebrow">{e(h['areas_eyebrow'])}</p>
                <h2>{e(h['areas_title'])}</h2>
                <p class="lead">{e(h['areas_lead'])}</p>
            </div>
            <div class="grid-3">{area_cards(lang, key)}</div>
        </div>
    </section>

    <section class="block stone">
        <div class="wrap">
            <div class="head"><p class="eyebrow">{e(h['steps_eyebrow'])}</p><h2>{e(h['steps_title'])}</h2></div>
            <ol class="steps">{steps}</ol>
        </div>
    </section>

    <section class="block">
        <div class="wrap split">
            <img class="photo reveal" src="{PHOTO.format(id='7876154', w=1000)}" alt="" width="1000" height="667" loading="lazy">
            <div>
                <p class="eyebrow">{e(h['ap_eyebrow'])}</p>
                <h2>{e(h['ap_title'])}</h2>
                <div class="grid-2">{ap}</div>
            </div>
        </div>
    </section>

    <section class="block stone">
        <div class="wrap">
            <div class="head"><p class="eyebrow">{e(h['team_eyebrow'])}</p><h2>{e(h['team_title'])}</h2></div>
            <div class="team">{team}</div>
            <p style="margin-top:34px"><a class="btn btn-ox" href="{link(cur, 'team', lang)}">{e(h['team_link'])}{ic('arrow')}</a></p>
        </div>
    </section>

    <section class="block">
        <div class="wrap">
            <div class="head"><p class="eyebrow">{e(h['ins_eyebrow'])}</p><h2>{e(h['ins_title'])}</h2></div>
            <div class="posts">{post_cards(lang, key)}</div>
            <p style="margin-top:34px"><a class="btn btn-ox" href="{link(cur, 'insights', lang)}">{e(h['ins_link'])}{ic('arrow')}</a></p>
        </div>
    </section>
{cta_band(lang, key)}"""
    return page(lang, key, h["title"], h["desc"], body, [ld])


def build_areas(lang):
    c, t, key = C[lang], C[lang]["ui"], "areas"
    p = c["areas_page"]
    cur = path(key, lang)
    trail = [("home", t["home"]), (key, t["nav"]["areas"])]
    body = page_hero(lang, key, trail, p["eyebrow"], p["h1"], p["lead"]) + f"""
    <section class="block">
        <div class="wrap">
            <div class="grid-3">{area_cards(lang, key)}</div>
            <div class="side-card" style="margin-top:48px; max-width:760px">
                <h3>{e(p['other_title'])}</h3>
                <p>{e(p['other_text'])}</p>
                <a class="btn btn-ox" href="{link(cur, 'contact', lang)}?area=other" style="width:auto">{e(t['cta'])}</a>
            </div>
        </div>
    </section>
{cta_band(lang, key)}"""
    return page(lang, key, p["title"], p["desc"], body, [crumbs_ld(lang, trail)])


def side(lang, key, a):
    t = C[lang]["ui"]
    cur = path(key, lang)
    m = member(lang, a["lawyer"])
    others = "".join(f'<li><a href="{link(cur, "area-" + o["key"], lang)}">{e(o["title"])}</a></li>' for o in C[lang]["areas"] if o["key"] != a["key"])
    return f"""
            <aside class="side">
                <div class="side-card dark">
                    <h3>{e(t['side_title'])}</h3>
                    <p>{e(t['side_text'])}</p>
                    <a class="btn btn-gold" href="{link(cur, 'contact', lang)}?area={a['key']}">{ic('cal')}{e(t['cta'])}</a>
                    <a class="btn btn-line" href="tel:{PHONE}">{ic('phone')}{e(t['phone_display'])}</a>
                </div>
                <div class="side-card">
                    <p style="margin:0 0 12px">{e(t['side_lawyer'])}</p>
                    <a class="side-person" href="{link(cur, 'team', lang)}#{m['key']}" style="text-decoration:none;color:inherit">
                        <img src="{photo(m, 200)}" alt="" width="64" height="64" loading="lazy" style="object-position: {m['pos']}">
                        <span><strong>{e(m['name'])}</strong><span>{e(m['role'])}</span></span>
                    </a>
                </div>
                <div class="side-card">
                    <p style="margin:0">{e(t['side_other'])}</p>
                    <ul class="side-links">{others}</ul>
                </div>
            </aside>"""


def build_area(lang, a):
    c, t = C[lang], C[lang]["ui"]
    key = "area-" + a["key"]
    cur = path(key, lang)
    trail = [("home", t["home"]), ("areas", t["nav"]["areas"]), (key, a["title"])]
    handle = "".join(f"<li>{ic('check')}<span>{e(x)}</span></li>" for x in a["handle"])
    bring = "".join(f"<li>{ic('doc')}<span>{e(x)}</span></li>" for x in a["bring"])
    rel_art = ""
    if a.get("article"):
        ar = article(lang, a["article"])
        rel_art = (f'<h2>{e(t["related_title"])}</h2><p><a href="{link(cur, "art-" + ar["key"], lang)}"><strong>{e(ar["title"])}</strong></a><br>'
                   f'<span style="color:var(--muted)">{e(ar["summary"])}</span></p>')
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in a["faq"]]}
    body = page_hero(lang, key, trail, t["nav"]["areas"].upper(), a["title"], a["card"]) + f"""
    <section class="block">
        <div class="wrap layout">
            <div class="prose">
                <p style="font-size:18px">{e(a['intro'])}</p>
                <h2>{e(t['handle_title'])}</h2>
                <ul class="checklist">{handle}</ul>
                <h2>{e(t['bring_title'])}</h2>
                <ul class="checklist">{bring}</ul>
                <h2>{e(t['faq_title'])}</h2>
                {faq(a['faq'])}
                {rel_art}
            </div>{side(lang, key, a)}
        </div>
    </section>
{cta_band(lang, key, a['key'])}"""
    title = f"{a['title']} | {t['brand']}"
    return page(lang, key, title, a["card"], body, [crumbs_ld(lang, trail), faq_ld])


def build_team(lang):
    c, t, key = C[lang], C[lang]["ui"], "team"
    p = c["team_page"]
    cur = path(key, lang)
    trail = [("home", t["home"]), (key, t["nav"]["team"])]
    bios = ""
    for m in c["team"]:
        areas = ", ".join(f'<a href="{link(cur, "area-" + k, lang)}">{e(area(lang, k)["title"])}</a>' for k in m["areas"])
        paras = "".join(f'<p class="b" style="color:var(--muted)">{e(x)}</p>' for x in m["bio"])
        bios += f"""
            <article class="bio" id="{m['key']}">
                <img src="{photo(m, 800)}" alt="{e(m['name'])}" width="800" height="1000" loading="lazy" style="object-position: {m['pos']}">
                <div>
                    <h2>{e(m['name'])}</h2>
                    <p class="r">{e(m['role'])}</p>
                    {paras}
                    <dl>
                        <dt>{e(p['l_edu'])}</dt><dd>{e(m['edu'])}</dd>
                        <dt>{e(p['l_areas'])}</dt><dd>{areas}</dd>
                        <dt>{e(p['l_langs'])}</dt><dd>{e(m['langs'])}</dd>
                        <dt>{e(p['l_bar'])}</dt><dd>{e(m['bar'])}</dd>
                    </dl>
                </div>
            </article>"""
    body = page_hero(lang, key, trail, p["eyebrow"], p["h1"], p["lead"]) + f"""
    <section class="block">
        <div class="wrap">{bios}
        </div>
    </section>
{cta_band(lang, key)}"""
    return page(lang, key, p["title"], p["desc"], body, [crumbs_ld(lang, trail)])


def build_fees(lang):
    c, t, key = C[lang], C[lang]["ui"], "fees"
    p = c["fees_page"]
    trail = [("home", t["home"]), (key, t["nav"]["fees"])]
    m_ic = ["doc", "scales", "corporate"]
    models = "".join(f'<li>{ic(m_ic[i])}<h3>{e(a)}</h3><p>{e(b)}</p></li>' for i, (a, b) in enumerate(p["models"]))
    affects = "".join(f"<li>{ic('check')}<span>{e(x)}</span></li>" for x in p["affects"])
    includes = "".join(f"<li>{ic('doc')}<span>{e(x)}</span></li>" for x in p["includes"])
    body = page_hero(lang, key, trail, p["eyebrow"], p["h1"], p["lead"]) + f"""
    <section class="block">
        <div class="wrap fees">
            <div>
                <h2>{e(p['models_title'])}</h2>
                <ul class="fee-list">{models}</ul>
            </div>
            <img class="reveal" src="{PHOTO.format(id='7504780', w=900)}" alt="" width="900" height="1350" loading="lazy">
        </div>
    </section>
    <section class="block stone">
        <div class="wrap split" style="align-items:start">
            <div class="prose"><h2>{e(p['affects_title'])}</h2><ul class="checklist">{affects}</ul></div>
            <div class="prose"><h2>{e(p['includes_title'])}</h2><ul class="checklist">{includes}</ul></div>
        </div>
    </section>
    <section class="block">
        <div class="wrap">
            <div class="head center"><h2>{e(t['faq_title'])}</h2></div>
            {faq(p['faq'])}
        </div>
    </section>
{cta_band(lang, key)}"""
    return page(lang, key, p["title"], p["desc"], body, [crumbs_ld(lang, trail)])


def build_insights(lang):
    c, t, key = C[lang], C[lang]["ui"], "insights"
    p = c["ins_page"]
    trail = [("home", t["home"]), (key, t["nav"]["insights"])]
    body = page_hero(lang, key, trail, p["eyebrow"], p["h1"], p["lead"]) + f"""
    <section class="block">
        <div class="wrap"><div class="posts">{post_cards(lang, key)}</div></div>
    </section>
{cta_band(lang, key)}"""
    return page(lang, key, p["title"], p["desc"], body, [crumbs_ld(lang, trail)])


def build_article(lang, a):
    c, t = C[lang], C[lang]["ui"]
    key = "art-" + a["key"]
    cur = path(key, lang)
    m = member(lang, a["author"])
    ar = area(lang, a["area"])
    trail = [("home", t["home"]), ("insights", t["nav"]["insights"]), (key, a["title"])]
    meta = (f'<div class="meta"><span>{e(t["by"])} <a href="{link(cur, "team", lang)}#{m["key"]}" style="color:#fff">{e(m["name"])}</a></span>'
            f'<span>{date(a["date"], lang)}</span><span>{a["mins"]} {e(t["min"])}</span></div>')
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "datePublished": a["date"],
          "inLanguage": lang, "author": {"@type": "Person", "name": m["name"]},
          "publisher": {"@type": "LegalService", "name": t["brand"]}, "mainEntityOfPage": BASE_URL + cur}
    body = page_hero(lang, key, trail, ar["title"].upper(), a["title"], a["summary"], meta) + f"""
    <section class="block">
        <div class="wrap layout">
            <article class="prose">{a['body']}
                <p class="note">{e(t['art_note'])}</p>
            </article>{side(lang, key, ar)}
        </div>
    </section>
{cta_band(lang, key, ar['key'])}"""
    return page(lang, key, f"{a['title']} | {t['brand']}", a["summary"], body, [crumbs_ld(lang, trail), ld])


def build_contact(lang):
    c, t, key = C[lang], C[lang]["ui"], "contact"
    p = c["contact_page"]
    f = p["fm"]
    cur = path(key, lang)
    priv = rel(cur, "privacy.html") + ("?lang=en" if lang == "en" else "")
    trail = [("home", t["home"]), (key, t["nav"]["contact"])]
    opts = "".join(f'<option value="{a["key"]}">{e(a["title"])}</option>' for a in c["areas"])
    body = page_hero(lang, key, trail, p["eyebrow"], p["h1"], p["lead"]) + f"""
    <section class="block contact-sec" style="padding-top:0">
        <div class="wrap">
            <div class="contact">
                <div class="form-card" id="formCard">
                    <form id="leadForm" action="{rel(cur, 'dm-contact/contact.php')}" method="post" data-dm-contact data-sent-target="#formCard" novalidate>
                        <div class="fields">
                            <div class="field full"><label for="f-name">{e(f['name'])}</label><input id="f-name" type="text" name="name" autocomplete="name" required></div>
                            <div class="field"><label for="f-phone">{e(f['phone'])}</label><input id="f-phone" type="tel" name="phone" autocomplete="tel" required></div>
                            <div class="field"><label for="f-email">{e(f['email'])}</label><input id="f-email" type="email" name="email" autocomplete="email"></div>
                            <div class="field full">
                                <label for="f-area">{e(f['area'])}</label>
                                <select id="f-area" name="area"><option value="">{e(f['choose'])}</option>{opts}<option value="other">{e(f['other'])}</option></select>
                            </div>
                            <fieldset class="field full">
                                <legend class="legend">{e(f['meet'])}</legend>
                                <div class="seg">
                                    <label><input type="radio" name="meeting" value="office" checked><span>{e(f['m1'])}</span></label>
                                    <label><input type="radio" name="meeting" value="video"><span>{e(f['m2'])}</span></label>
                                    <label><input type="radio" name="meeting" value="phone"><span>{e(f['m3'])}</span></label>
                                </div>
                            </fieldset>
                            <div class="field full"><label for="f-msg">{e(f['msg'])}</label><textarea id="f-msg" name="message" maxlength="400" placeholder="{e(f['msg_ph'])}"></textarea></div>
                            <label class="check field full"><input type="checkbox" name="consent" required><span>{e(f['consent'])}</span></label>
                        </div>
                        <button class="btn btn-ox" type="submit">{ic('cal')}<span>{e(f['submit'])}</span></button>
                        <p class="form-note">{ic('lock')}<span>{e(f['note'])} {e(f['see'])} <a href="{priv}">{e(t['privacy'])}</a>.</span></p>
                    </form>
                    <div class="form-ok" role="status" aria-live="polite">
                        {ic('check')}
                        <h3>{e(f['ok_t'])}</h3>
                        <p>{e(f['ok_d'])}</p>
                    </div>
                </div>

                <div class="info">
                    <div class="info-row">{ic('pin')}<div><h3>{e(p['i_addr'])}</h3><p>{e(t['address'])}</p><small>{e(t['address_note'])}</small><p><a href="https://www.google.com/maps/dir/?api=1&amp;destination=Akadimias%2C+Athens" target="_blank" rel="noopener">{e(p['i_dir'])}</a></p></div></div>
                    <div class="info-row">{ic('mail')}<div><h3>{e(p['i_phone'])}</h3><p><a href="tel:{PHONE}">{e(t['phone_display'])}</a></p><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div></div>
                    <div class="info-row">{ic('clock')}<div><h3>{e(p['i_hours'])}</h3>
                        <table class="hours">
                            <tr><td>{e(p['h_wd'])}</td><td>09:00–18:00</td></tr>
                            <tr><td>{e(p['h_sat'])}</td><td>{e(p['h_sat_v'])}</td></tr>
                        </table>
                    </div></div>
                </div>
            </div>
            <div class="map">
                <iframe src="https://maps.google.com/maps?q={MAP_Q}&amp;z=15&amp;output=embed" title="{e(p['map_title'])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
            </div>
        </div>
    </section>
    <section class="block">
        <div class="wrap">
            <div class="head center"><h2>{e(t['faq_title'])}</h2></div>
            {faq(p['faq'])}
        </div>
    </section>"""
    form_js = f'<script src="{rel(cur, "dm-contact/contact-form.js")}" defer></script>\n'
    return page(lang, key, p["title"], p["desc"], body, [crumbs_ld(lang, trail)], form_js)


# ---------------------------------------------------------------- write

def write(key, lang, html_text):
    out = OUT / path(key, lang) / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_text, encoding="utf-8")
    return out


def sitemap():
    today = datetime.date.today().isoformat()
    urls = ""
    for key in PATHS:
        for lang in LANGS:
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{BASE_URL}{path(key, l)}"/>' for l in LANGS)
            urls += f"  <url><loc>{BASE_URL}{path(key, lang)}</loc><lastmod>{today}</lastmod>{alts}</url>\n"
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + urls + "</urlset>\n", encoding="utf-8")


def main():
    n = 0
    for lang in LANGS:
        write("home", lang, build_home(lang))
        write("areas", lang, build_areas(lang))
        for a in C[lang]["areas"]:
            write("area-" + a["key"], lang, build_area(lang, a))
        write("team", lang, build_team(lang))
        write("fees", lang, build_fees(lang))
        write("insights", lang, build_insights(lang))
        for a in C[lang]["articles"]:
            write("art-" + a["key"], lang, build_article(lang, a))
        write("contact", lang, build_contact(lang))
        n += len(PATHS)
    sitemap()
    print(f"built {n} pages + sitemap.xml in {OUT.relative_to(OUT.parent.parent)}")


if __name__ == "__main__":
    main()
