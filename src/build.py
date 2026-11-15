#!/usr/bin/env python3
"""Static site generator. Run: python3 src/build.py  ->  writes ./public"""
import json, html, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from process import PROCESS, scene, SAMPLE_REPORT, SAMPLE_GANTT
from content import PEST, ISO, OTHER, EXTRA, MORE_FAQS, VALUES, SECTORS, CITY_PAGES, PEST_STEPS, ISO_STEPS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public")
C = json.load(open(os.path.join(ROOT, "src", "config.json"), encoding="utf-8"))
E = html.escape
CITIES = C["cities"]
city = " and ".join(CITIES)
BASE = C["base_url"].rstrip("/")
PAGES = []  # (url path) for sitemap


def fmt(s):
    lic = C["proof"]["pest_licence"]
    return s.replace("{city}", city).replace("{pest_licence_line}", (" Our qualification: " + lic + ".") if lic else "")


def write(path, content):
    full = os.path.join(OUT, path.strip("/"), "index.html") if not path.endswith(".html") else os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


def business_ld():
    o = {"@context": "https://schema.org", "@type": "LocalBusiness", "@id": BASE + "/#business", "name": C["brand"],
         "url": BASE + "/", "telephone": C["phone"], "email": C["email"],
         "areaServed": [{"@type": "City", "name": x} for x in CITIES] + [{"@type": "Country", "name": C["country"]}],
         "address": {"@type": "PostalAddress", "addressLocality": CITIES[0], "addressCountry": "SA"}}
    if C["street_address"]:
        o["address"]["streetAddress"] = C["street_address"]
    return o


def gtm_head():
    g = C["gtm_id"]
    if not g:
        return ""
    return ("<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});"
            "var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;"
            "j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})"
            "(window,document,'script','dataLayer','%s');</script>" % g)


def gtm_body():
    g = C["gtm_id"]
    return ('<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=%s" height="0" width="0" '
            'style="display:none;visibility:hidden"></iframe></noscript>' % g) if g else ""


# ---------- icons and illustrations ----------
def _svg(inner):
    return '<svg viewBox="0 0 24 24" aria-hidden="true">' + inner + "</svg>"


ICON = {
    "termite": _svg('<circle cx="12" cy="5" r="2"/><ellipse cx="12" cy="10.5" rx="2" ry="2.8"/><ellipse cx="12" cy="17.2" rx="3.2" ry="4"/><path d="M11 3.4 9 1.5M13 3.4l2-1.9M10 9.5 6 8M14 9.5 18 8M10 11l-4.5 1M14 11l4.5 1M10 12.5 6.5 16M14 12.5l3.5 3.5"/>'),
    "rodent": _svg('<circle cx="12" cy="14.5" r="5.6"/><circle cx="6.3" cy="7.8" r="3.1"/><circle cx="17.7" cy="7.8" r="3.1"/><circle cx="10" cy="13.4" r=".8" class="fill"/><circle cx="14" cy="13.4" r=".8" class="fill"/><path d="M11.2 16.2h1.6M8.6 16.6l-3.4.6M15.4 16.6l3.4.6"/>'),
    "roach": _svg('<ellipse cx="12" cy="14.5" rx="4" ry="6.3"/><path d="M9.6 9.4a2.4 2.4 0 0 1 4.8 0M12 9.6v11M10.6 7.2C9.6 4.4 7.2 3.2 5 3.6M13.4 7.2c1-2.8 3.4-4 5.6-3.6M8.2 12.4 5 11M15.8 12.4 19 11M8 15.4H4.6M16 15.4h3.4M8.7 18.6 6.2 21M15.3 18.6l2.5 2.4"/>'),
    "bed": _svg('<path d="M3 19V7M3 14.5h18V19M21 14.5V13a3 3 0 0 0-3-3h-7v4.5M3 19v1.5M21 19v1.5"/><circle cx="7" cy="11.4" r="1.7"/>'),
    "fume": _svg('<path d="M3 20.5V9.5l9-5 9 5v11M2 20.5h20M8 20.5v-5h8v5"/><path d="M9 12.3a1.6 1.6 0 0 1 3-.7 1.6 1.6 0 0 1 3 .7"/>'),
    "building": _svg('<path d="M4 21V4.5h10V21M14 10h6v11M2.5 21h19M7 8h1.2M10 8h1.2M7 12h1.2M10 12h1.2M7 16h1.2M10 16h1.2M17 14h.2M17 17.5h.2"/>'),
    "shield": _svg('<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>'),
    "wa": _svg('<path d="M12 3a9 9 0 0 0-7.8 13.5L3 21l4.7-1.2A9 9 0 1 0 12 3z"/>'),
    "mosquito": _svg('<ellipse cx="7" cy="9" rx="4.2" ry="2" transform="rotate(-25 7 9)"/><ellipse cx="17" cy="9" rx="4.2" ry="2" transform="rotate(25 17 9)"/><path d="M12 8v9M12 17l-1.2 4M12 17l1.2 4M12 8V4l-1.6-2M9 12l-4 2M15 12l4 2"/>'),
    "bird": _svg('<path d="M3 15c3-1 4-4 7-5 3-1 6 0 7 3l4-1-2 4c-1 3-4 5-8 5-5 0-8-2-8-6z"/><path d="M10 10c0-3 2-5 5-5 2 0 3 1 3 3"/><circle cx="16" cy="12" r=".8" class="fill"/>'),
    "snake": _svg('<path d="M18 4c-4 0-5 3-3 5s1 5-3 6-6 3-4 6"/><path d="M18 4l3 1-3 1"/><circle cx="17" cy="4.6" r=".6" class="fill"/>'),
    "people": _svg('<circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0 1 12 0"/><circle cx="17" cy="9" r="2.4"/><path d="M16 20a5 5 0 0 1 6 0"/>'),
    "grid": _svg('<rect x="4" y="4" width="7" height="7" rx="1"/><rect x="13" y="4" width="7" height="7" rx="1"/><rect x="4" y="13" width="7" height="7" rx="1"/><rect x="13" y="13" width="7" height="7" rx="1"/>'),
    "phone": _svg('<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>'),
}
PEST_ICON = {"termite-control": "termite", "rodent-control": "rodent", "cockroach-control": "roach",
             "bed-bug-treatment": "bed", "fumigation": "fume", "commercial-ipm": "building",
             "mosquito-control": "mosquito", "bird-control": "bird", "wildlife-control": "snake"}
ISO_ICON = {"training": "people", "other-standards": "grid"}


def ic(kind):
    return '<span class="ic">' + ICON[kind] + "</span>"


def seal(num):
    return f'<span class="seal" aria-hidden="true"><small>ISO</small><b>{num}</b></span>'


def card_icon(family, slug):
    if family == "pest":
        return ic(PEST_ICON[slug])
    return ic(ISO_ICON[slug]) if slug in ISO_ICON else seal(slug.replace("iso-", ""))


def illus_pest():
    bug = '<ellipse rx="6" ry="4"/><path d="M-4-4l-3-4M0-4v-5M4-4l3-4M-4 4l-3 4M0 4v5M4 4l3 4"/>'
    return f'''<svg class="illus" viewBox="0 0 360 280" role="img" aria-label="A building inside a monitored protection perimeter">
<ellipse class="ring faint" cx="180" cy="152" rx="158" ry="112"/>
<ellipse class="ring draw" pathLength="1" cx="180" cy="152" rx="124" ry="86"/>
<path class="ln" d="M96 204h168"/>
<path class="house" d="M122 204v-62l58-46 58 46v62z"/>
<path class="ln" d="M110 148l70-56 70 56"/>
<rect class="ln" x="168" y="164" width="24" height="40" rx="2"/><rect class="ln" x="136" y="154" width="20" height="20" rx="2"/><rect class="ln" x="204" y="154" width="20" height="20" rx="2"/>
<circle class="node" cx="56" cy="152" r="6"/><circle class="node n2" cx="304" cy="152" r="6"/><circle class="node n3" cx="180" cy="238" r="6"/>
<g class="bug" transform="translate(26 62)">{bug}</g><g class="bug" transform="translate(334 236) rotate(140)">{bug}</g><g class="bug" transform="translate(326 54) rotate(40)">{bug}</g>
<g transform="translate(180 50)"><g class="pop"><path class="badge" d="M0-24l19 7v14c0 13-8.5 21-19 25-10.5-4-19-12-19-25v-14z"/><path class="badge-ck" d="M-8 0l6 6 10-12"/></g></g>
</svg>'''


def illus_ipm():
    return '''<svg class="illus ipm" viewBox="0 0 360 280" role="img" aria-label="The IPM cycle: assess, prevent, control">
<g class="ipm-ring"><path class="ar a1" d="M180 40a100 100 0 0 1 86.600 50"/><path class="ar a2" d="M266.600 190a100 100 0 0 1-173.200 0"/><path class="ar a3" d="M93.400 90A100 100 0 0 1 180 40"/>
<path class="fl1" d="m272 84 8 20-21-3z"/><path class="fl2" d="m88 206-8-20 21 3z"/><path class="fl3" d="m96 78 20-9-4 21z"/></g>
<circle class="core" cx="180" cy="140" r="52"/><text class="cn" x="180" y="136" text-anchor="middle">IPM</text><text class="cs" x="180" y="156" text-anchor="middle">integrated pest management</text>
<text class="lb" x="340" y="52" text-anchor="end">PREVENT</text><text class="lb" x="180" y="266" text-anchor="middle">CONTROL</text><text class="lb" x="20" y="52" text-anchor="start">ASSESS</text>
</svg>'''


def illus_iso(label="MANAGEMENT SYSTEM"):
    rows = ["Gap analysis", "Documentation", "Internal audit", "Certification audit"]
    r = ""
    for i, t in enumerate(rows):
        y = 96 + i * 34
        r += (f'<rect class="box" x="92" y="{y}" width="18" height="18" rx="4"/>'
              f'<path class="tick draw d{i}" pathLength="1" d="M96 {y+9}l4 4 7-8"/>'
              f'<text class="row" x="122" y="{y+13}">{t}</text>')
    return f'''<svg class="illus" viewBox="0 0 360 280" role="img" aria-label="An audit checklist being completed, with a certification seal">
<rect class="doc-shadow" x="84" y="30" width="204" height="238" rx="10"/>
<rect class="doc" x="72" y="18" width="204" height="238" rx="10"/>
<text class="mono" x="92" y="52">{E(label)}</text>
<rect class="rule" x="92" y="64" width="120" height="5" rx="2.5"/><rect class="rule" x="92" y="76" width="76" height="5" rx="2.5"/>
{r}
<g transform="translate(262 222)"><g class="pop"><path class="ribbon" d="M-14 20l-7 26 13-8zM14 20l7 26-13-8z"/><circle class="seal-c" r="32"/><circle class="seal-r" r="24"/><path class="seal-ck" d="M-10 0l7 7 13-15"/></g></g>
</svg>'''


# ---------- shared chrome ----------
WA = "https://wa.me/" + C["whatsapp"]


def wa_link(text):
    return WA + "?text=" + text.replace(" ", "%20")


def btn_wa(href, label="WhatsApp us"):
    return f'<a class="btn btn-wa" href="{href}">{ICON["wa"]}{label}</a>'


def btn_call(label=None):
    return f'<a class="btn btn-call" href="tel:{C["phone"]}">{ICON["phone"]}{label or "Call " + E(C["phone_display"])}</a>'


def header():
    return f"""<header class="site"><div class="wrap">
<a class="brand" href="/"><img src="/assets/logo.png" width="154" height="40" alt="{E(C['brand'])}"></a>
<nav class="main" aria-label="Main"><a href="/pest-control/">Pest Control</a><a href="/iso-consultancy/">ISO Consultancy</a><a href="/how-it-works/">How It Works</a><a href="/facility-services/">Other Services</a><a href="/about/">About</a><a href="/contact/">Contact</a></nav>
<a class="btn btn-ghost" href="tel:{C['phone']}">{ICON['phone']}{E(C['phone_display'])}</a>
</div></header>"""


def footer():
    pest = "".join(f'<li><a href="/pest-control/{s}/">{E(fmt(PEST[s]["service"]))}</a></li>' for s in PEST["hub"]["children"])
    iso = "".join(f'<li><a href="/iso-consultancy/{s}/">{E(ISO[s]["service"])}</a></li>' for s in ISO["hub"]["children"])
    addr = E(C["street_address"] or C["address_note"])
    areas = "".join(f'<li><a href="/{h}/{x.lower()}/">{l} in {E(x)}</a></li>' for h, l in (("pest-control", "Pest control"), ("iso-consultancy", "ISO consultants")) for x in CITIES)
    return f"""<footer class="site"><div class="wrap"><div class="cols">
<div><p class="flogo"><img src="/assets/logo.png" width="190" height="50" alt="{E(C['brand'])}" loading="lazy"></p><p>{addr}</p><p><a href="tel:{C['phone']}">{E(C['phone_display'])}</a><br><a href="mailto:{C['email']}">{E(C['email'])}</a></p></div>
<div><h4>Pest Control</h4><ul>{pest}</ul></div>
<div><h4>ISO Consultancy</h4><ul>{iso}</ul></div>
<div><h4>Areas</h4><ul>{areas}</ul></div>
<div><h4>Company</h4><ul><li><a href="/how-it-works/">How it works</a></li><li><a href="/facility-services/">Other services</a></li><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li><li><a href="/privacy/">Privacy</a></li></ul></div>
</div><p class="copy">&copy; 2026 {E(C['brand'])}</p></div></footer>
<div class="sticky"><a class="btn btn-call" href="tel:{C['phone']}">{ICON['phone']}Call</a><a class="btn btn-wa" href="{WA}">{ICON['wa']}WhatsApp</a></div>"""


def form(service, sel_city=None):
    opts = ["Pest Control", "Termite Control", "Rodent Control", "Cockroach / Insect Control", "Bed Bug Treatment", "Fumigation",
            "Commercial IPM Programme", "Mosquito / Dengue Control", "Bird Control", "Snake / Lizard / Stray Animal Control",
            "ISO Consultancy", "ISO 9001", "ISO 22000", "ISO 45001", "ISO 14001", "ISO 27001", "Other ISO Standards", "ISO Training", "Other"]
    if service not in opts:
        opts.insert(0, service)
    o = "".join(f'<option{" selected" if x == service else ""}>{E(x)}</option>' for x in opts)
    copts = "".join(f'<option{" selected" if x == sel_city else ""}>{E(x)}</option>' for x in CITIES + ["Other city"])
    return f"""<form class="lead" data-wa="{C['whatsapp']}" data-endpoint="{E(C['form_endpoint'])}">
<label for="n">Name</label><input id="n" name="name" required autocomplete="name">
<label for="p">Phone / WhatsApp</label><input id="p" name="phone" type="tel" required autocomplete="tel">
<label for="s">Service</label><select id="s" name="service">{o}</select>
<label for="c">City</label><select id="c" name="city">{copts}</select>
<label for="m">Details (optional)</label><textarea id="m" name="message" rows="2"></textarea>
<button class="btn btn-wa" type="submit">{ICON['wa']}Send via WhatsApp</button>
<p class="small">Opens WhatsApp with your details filled in. We reply during business hours.</p></form>"""


def trust(family="pest"):
    p = C["proof"]
    items = []
    if p["iso9001_certificate"]:
        items.append("ISO 9001 certified: " + p["iso9001_certificate"])
    if p["pest_licence"] and family != "iso":
        items.append("Licence: " + p["pest_licence"])
    if p["years_in_service"]:
        items.append(p["years_in_service"] + " years in service")
    if family == "pest":
        items += ["Free site inspection", "Written service records"]
    elif family == "iso":
        items += ["Free consultation", "Gap analysis and audit preparation"]
    else:
        items += ["Free site inspection", "Free ISO consultation"]
    items.append(f"Serving {city}")
    return '<ul class="trust">' + "".join(f"<li>{E(i)}</li>" for i in items) + "</ul>"


FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500&family=IBM+Plex+Sans:wght@400;500;600;700'
         '&family=IBM+Plex+Sans+Condensed:wght@600;700&display=swap" rel="stylesheet">')


def page(path, title, desc, body, extra_ld=None, crumbs=None, noindex=False):
    url = BASE + path
    fam = "t-pest" if path.startswith("/pest-control") else "t-iso" if path.startswith("/iso-consultancy") else "t-home"
    ldo = [business_ld()] if path == "/" else []
    if crumbs:
        ldo.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u} for i, (n, u) in enumerate(crumbs)]})
    ldo += extra_ld or []
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}"><link rel="icon" type="image/png" href="/assets/favicon.png">{robots}
<meta property="og:type" content="website"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}">
<script>document.documentElement.className="js"</script>
{FONTS}
<link rel="stylesheet" href="/assets/style.css">
{''.join(ld(o) for o in ldo)}
{gtm_head()}</head><body class="{fam}">{gtm_body()}
{header()}
<main>{body}</main>
{footer()}
<script src="/assets/site.js" defer></script></body></html>"""
    write(path, doc)
    if not noindex:
        PAGES.append(path)


def crumbs_html(items):
    return '<nav class="crumbs" aria-label="Breadcrumb">' + " <span>/</span> ".join(
        f'<a href="{u}">{E(n)}</a>' if i < len(items) - 1 else f"<b>{E(n)}</b>" for i, (n, u) in enumerate(items)) + "</nav>"


def simple_hero(cr, h1, lead):
    return f'<div class="hero slim"><div class="wrap">{crumbs_html(cr)}<h1>{E(h1)}</h1><p class="lead">{E(lead)}</p></div></div>'


def render_blocks(blocks):
    """Render in-depth content blocks; returns (html, [(id, title)])."""
    out, toc = "", []
    for i, b in enumerate(blocks):
        kind, bid = b[0], b[1]
        alt = ' class="alt"' if i % 2 == 0 else ""
        if kind == "callout":
            out += f'<section class="tight" id="{bid}"><div class="wrap narrow"><div class="callout"><h3>{E(fmt(b[2]))}</h3><p>{E(fmt(b[3]))}</p></div></div></section>'
            continue
        kicker, title = b[2], fmt(b[3])
        toc.append((bid, title))
        head = f'<p class="kicker">{E(kicker)}</p><h2 class="s">{E(title)}</h2>'
        if kind == "table":
            intro, headers, rows, note = b[4], b[5], b[6], b[7]
            th = "".join(f"<th>{E(h)}</th>" for h in headers)
            tr = "".join("<tr>" + "".join(
                (f'<th scope="row" data-l="{E(headers[j])}">{E(c)}</th>' if j == 0 else f'<td data-l="{E(headers[j])}">{E(c)}</td>')
                for j, c in enumerate(r)) + "</tr>" for r in rows)
            body = (f'<p class="sub">{E(fmt(intro))}</p>' if intro else "") + f'<div class="tbl"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
            if note:
                body += f'<p class="note">{E(note)}</p>'
            out += f'<section{alt} id="{bid}"><div class="wrap">{head}{body}</div></section>'
        elif kind == "list":
            intro, items = b[4], b[5]
            li = "".join(f"<li>{E(x)}</li>" for x in items)
            out += f'<section{alt} id="{bid}"><div class="wrap narrow">{head}<p class="sub">{E(fmt(intro))}</p><ul class="ticks one">{li}</ul></div></section>'
        elif kind == "cards":
            intro, items = b[4], b[5]
            cards = "".join(f'<div class="card plain"><h3>{E(h)}</h3><p>{E(t)}</p></div>' for h, t in items)
            out += f'<section{alt} id="{bid}"><div class="wrap">{head}' + (f'<p class="sub">{E(intro)}</p>' if intro else "") + f'<div class="cards wide">{cards}</div></div></section>'
        elif kind == "prose":
            ps = "".join(f"<p>{E(x)}</p>" for x in b[4])
            out += f'<section{alt} id="{bid}"><div class="wrap narrow prose">{head}{ps}</div></section>'
    return out, toc


def wyg(st):
    return ('<div class="wyg"><div><h4>What we do</h4><p>' + E(st["we"]) + '</p></div><div><h4>What you do</h4><p>' + E(st["you"]) +
            '</p></div><div class="gets"><h4>What you get</h4><p>' + E(st["get"]) + '</p></div></div>')


def process_widget(family):
    steps = PROCESS[family]
    btns = "".join(
        f'<button type="button" class="pstep{" active" if i == 0 else ""}" role="tab" id="t-{family}-{i}" aria-controls="p-{family}-{i}" aria-selected="{"true" if i == 0 else "false"}" data-i="{i}">'
        f'<span class="pn">{i+1:02d}</span><span class="pt"><b>{E(st["title"])}</b><small>{E(st["short"])}</small></span><span class="pbar"></span></button>'
        for i, st in enumerate(steps))
    panels = "".join(
        f'<div class="ppanel{" active" if i == 0 else ""}" role="tabpanel" id="p-{family}-{i}" aria-labelledby="t-{family}-{i}">'
        f'<div class="pscene">{scene(st["icon"])}<span class="pcount">Step {i+1} of {len(steps)}</span></div>'
        f'<div class="pbody"><span class="chip">{E(st["time"])}</span><h3>{E(st["title"])}</h3>{wyg(st)}</div></div>'
        for i, st in enumerate(steps))
    what = "a pest control job" if family == "pest" else "an ISO project"
    return (f'<section class="alt" id="process"><div class="wrap"><p class="kicker">Process</p><h2 class="s">How {what} works, step by step</h2>'
            f'<p class="sub">Pick a step to see what we do, what we need from you, and what you receive. Durations are typical and are confirmed in your quotation.</p>'
            f'<div class="pw"><div class="plist" role="tablist" aria-label="Process steps">{btns}</div><div class="ppanels">{panels}</div></div>'
            f'<p class="more-link"><a href="/{"pest-control" if family == "pest" else "iso-consultancy"}/how-it-works/">See the full process, with a sample {"service report" if family == "pest" else "project plan"} &rarr;</a></p></div></section>')


def lane(family):
    steps = PROCESS[family]
    name, path = ("Pest control", "/pest-control/how-it-works/") if family == "pest" else ("ISO consultancy", "/iso-consultancy/how-it-works/")
    li = "".join(f'<li style="--d:{i*90}ms"><span class="ln-n">{i+1}</span><b>{E(st["title"])}</b></li>' for i, st in enumerate(steps))
    return f'<div class="lane t-{family}"><h3>{name}</h3><ol class="lane-steps">{li}</ol><a class="more" href="{path}">See how it works</a></div>'


def sample_report():
    rows = "".join(f"<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>" for k, v in SAMPLE_REPORT)
    return ('<div class="paper"><span class="stamp-s">Sample</span><p class="kicker">Service report</p><h3>What you receive after every visit</h3>'
            f'<dl>{rows}</dl><p class="small">This is an illustration. Your report is filled in with the real details of your visit.</p></div>')


def sample_gantt():
    wk = 24
    rows = ""
    for i, (label, a, b, who) in enumerate(SAMPLE_GANTT):
        left, width = (a - 1) / wk * 100, (b - a + 1) / wk * 100
        rows += (f'<div class="g-row"><span class="g-l">{E(label)}</span><span class="g-t"><i class="g-b {who}" style="left:{left:.2f}%;width:{width:.2f}%;--d:{i*140}ms"></i></span></div>')
    scale = "".join(f"<span>{w}</span>" for w in (1, 4, 8, 12, 16, 20, 24))
    return ('<div class="gantt"><p class="kicker">Illustrative plan</p><h3>A typical five-month ISO project</h3>'
            f'<div class="g-scale"><span class="g-l">Week</span><span class="g-t g-ticks">{scale}</span></div>{rows}'
            '<div class="g-key"><span><i class="g-b us"></i>Our work with your team</span><span><i class="g-b you"></i>Your management</span>'
            '<span><i class="g-b cb"></i>Certification body (its own schedule)</span></div>'
            '<p class="small">Your plan is dated after the gap analysis. The certification body sets the dates of its own audits.</p></div>')


def process_page(family):
    steps = PROCESS[family]
    hub = "pest-control" if family == "pest" else "iso-consultancy"
    path = f"/{hub}/how-it-works/"
    nm = "Pest control" if family == "pest" else "ISO consultancy"
    h1 = f"How our {nm.lower()} works" if family == "pest" else "How ISO certification works with us"
    cr = [("Home", "/"), (nm, f"/{hub}/"), ("How it works", path)]
    tl = "".join(
        f'<article class="tl" id="step-{st["id"]}"><span class="tl-m">{i+1}</span><div class="tl-in"><div class="tl-sc">{scene(st["icon"])}</div>'
        f'<div><span class="chip">{E(st["time"])}</span><h2>{E(st["title"])}</h2>{wyg(st)}</div></div></article>' for i, st in enumerate(steps))
    extra = sample_report() if family == "pest" else sample_gantt()
    lead = ("From the first call to the follow-up visit: what happens, who does what, and what you get at each step." if family == "pest"
            else "From the first meeting to the certificate and beyond: what happens, who does what, and who decides at each step.")
    nav = "".join(f'<a href="#step-{st["id"]}">{i+1}. {E(st["title"])}</a>' for i, st in enumerate(steps))
    cta = "Book a free inspection" if family == "pest" else "Book a free consultation"
    cl = wa_link("Hello, I would like to book " + ("an inspection" if family == "pest" else "an ISO consultation"))
    body = (f'<div class="hero slim t-{family}"><div class="wrap">{crumbs_html(cr)}<h1>{E(h1)}</h1><p class="lead">{E(lead)}</p>'
            f'<div class="cta">{btn_wa(cl)}{btn_call()}</div></div></div>'
            f'<nav class="onpage" aria-label="Steps"><div class="wrap"><b>Steps</b>{nav}</div></nav>'
            f'<section><div class="wrap"><div class="tlwrap"><div class="tlrail" aria-hidden="true"><i></i></div>{tl}</div></div></section>'
            f'<section class="alt"><div class="wrap narrow">{extra}</div></section>'
            f'<div class="cta-band"><div class="wrap"><h2>{cta}</h2><p>Tell us about your site and we will contact you.</p><div class="cta">{btn_wa(cl)}{btn_call("Call now")}</div></div></div>')
    page(path, f"How {nm} Works | Step by Step Process | Omnexa Solutions",
         ("How our pest control works in Riyadh and Jeddah: inspection, written plan, treatment, service report and follow-up." if family == "pest"
          else "How ISO certification works: gap analysis, documentation, training, internal audit, certification audit and renewal."), body, crumbs=cr)


def process_hub():
    cr = [("Home", "/"), ("How it works", "/how-it-works/")]
    cols = ""
    for fam, nm, path, desc in (("pest", "Pest control", "/pest-control/how-it-works/", "Inspection first, a written plan, treatment, a report after every visit, and follow-up."),
                                ("iso", "ISO consultancy", "/iso-consultancy/how-it-works/", "Gap analysis, documentation, training, internal audit, then the certification audit by an accredited body.")):
        cols += f'<a class="door t-{fam}" href="{path}"><div class="door-txt"><p class="kicker">{nm}</p><h2>{len(PROCESS[fam])} steps from first contact to result</h2><p>{desc}</p><span class="more">See the full process</span></div></a>'
    body = (f'<div class="hero slim"><div class="wrap">{crumbs_html(cr)}<h1>How we work</h1><p class="lead">Both services follow a clear process, with written records at every stage.</p></div></div>'
            f'<section><div class="wrap doors flat">{cols}</div></section>')
    page("/how-it-works/", "How We Work | Pest Control and ISO Process | Omnexa Solutions", "How our pest control and ISO consultancy processes work, step by step.", body, crumbs=cr)


def service_page(path, d, parent, family, slug=None):
    h1, title, desc = fmt(d["h1"]), fmt(d["title"]), fmt(d["desc"])
    data = PEST if family == "pest" else ISO
    hub = data["hub"]
    hub_path = "/" + hub["slug"] + "/"
    cr = [("Home", "/")]
    if parent:
        cr.append((parent[0], parent[1]))
    cr.append((h1, path))
    ticks = "".join(f"<li>{E(fmt(b))}</li>" for b in d["bullets"])
    steps = "".join(f"<li><b>{E(a)}</b><span>{E(b)}</span></li>" for a, b in d["steps"])
    key = (family, slug or "hub")
    faqs = list(d["faqs"]) + MORE_FAQS.get(key, [])
    faq = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in faqs)
    extra, toc = render_blocks(EXTRA.get(key, []))
    onpage = ""
    if toc:
        links = "".join(f'<a href="#{i}">{E(t)}</a>' for i, t in toc) + '<a href="#process">How it works</a><a href="#faq">FAQ</a>'
        onpage = f'<nav class="onpage" aria-label="On this page"><div class="wrap"><b>On this page</b>{links}</div></nav>'
    noun = "inspection" if family == "pest" else "consultation"
    if slug is None:  # hub
        cards = "".join(f'<a class="card" href="{hub_path}{c}/">{card_icon(family, c)}<h3>{E(fmt(data[c]["h1"]))}</h3><p>{E(fmt(data[c]["lead"]))}</p><span class="more">Learn more</span></a>'
                        for c in hub["children"])
        ktitle = "Pest control services" if family == "pest" else "ISO standards we support"
        areas = "".join(f'<a href="{hub_path}{x.lower()}/">{E(CITY_PAGES[(family, x.lower())]["h1"])}</a>' for x in CITIES)
        related = f'<section class="alt"><div class="wrap"><p class="kicker">Services</p><h2 class="s">{ktitle}</h2><div class="cards">{cards}</div><p class="kicker" style="margin-top:36px">Areas we serve</p><div class="chips">{areas}</div></div></section>'
        eyebrow = ("Pest control" if family == "pest" else "ISO consultancy") + " · " + (city if family == "pest" else "Saudi Arabia")
        label = "MANAGEMENT SYSTEM"
    else:
        sib = "".join(f'<a href="{hub_path}{c}/">{E(fmt(data[c]["service"]))}</a>' for c in hub["children"] if c != slug)
        related = f'<section class="alt tight"><div class="wrap"><p class="kicker">Related services</p><div class="chips">{sib}<a class="all" href="{hub_path}">All {E(parent[0].lower())} services</a></div></div></section>'
        eyebrow = parent[0] + (" · " + d["city"] if d.get("city") else "")
        label = d["service"].upper()
    notice = ""
    if family == "iso":
        notice = '<div class="notice">We are ISO consultants. Certificates are issued by an accredited certification body of your choice; we prepare you for its audit.</div>'
    art = illus_ipm() if slug == "commercial-ipm" else (illus_pest() if family == "pest" else illus_iso(label))
    if slug is None or d.get("city"):
        proc = process_widget(family)
    else:
        proc = (f'<section class="alt" id="process"><div class="wrap"><p class="kicker">Process</p><h2 class="s">How it works</h2><ol class="steps">{steps}</ol>'
                f'<p class="more-link"><a href="/{hub["slug"]}/how-it-works/">See the full process &rarr;</a></p></div></section>')
    cta = wa_link("Hello, I need " + d["service"])
    body = f"""<div class="hero"><div class="wrap">{crumbs_html(cr)}<div class="grid"><div>
<p class="eyebrow">{E(eyebrow)}</p><h1>{E(h1)}</h1><p class="lead">{E(fmt(d['lead']))}</p>
<div class="cta">{btn_wa(cta)}{btn_call()}</div>{trust(family)}</div>
<div class="card formcard"><h2>Request a free {noun}</h2>{form(d['service'], d.get('city'))}</div></div></div></div>
{onpage}
<section><div class="wrap two"><div><p class="kicker">What's included</p><h2 class="s">{E(d['service'])}: what we do</h2><p class="sub">{E(fmt(d['intro']))}</p><ul class="ticks">{ticks}</ul>{notice}</div>
<div class="art">{art}</div></div></section>
{extra}
{proc}
{related}
<section id="faq"><div class="wrap narrow"><p class="kicker">FAQ</p><h2 class="s">Frequently asked questions</h2>{faq}</div></section>
<div class="cta-band"><div class="wrap"><h2>Book your free {noun}</h2><p>Tell us about your site and we will contact you.</p>
<div class="cta">{btn_wa(cta)}{btn_call("Call now")}</div></div></div>"""
    svc = {"@context": "https://schema.org", "@type": "Service", "name": h1, "serviceType": d["service"],
           "provider": {"@type": "LocalBusiness", "@id": BASE + "/#business", "name": C["brand"], "telephone": C["phone"]},
           "areaServed": {"@type": "Country", "name": C["country"]}, "url": BASE + path, "description": desc}
    fq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    page(path, title, desc, body, [svc, fq], cr)


def build():
    for fam, data, name in (("pest", PEST, "Pest Control"), ("iso", ISO, "ISO Consultancy")):
        hub = data["hub"]
        hp = "/" + hub["slug"] + "/"
        service_page(hp, hub, None, fam)
        for k in hub["children"]:
            service_page(hp + k + "/", data[k], (name, hp), fam, slug=k)
        for x in CITIES:
            d = dict(CITY_PAGES[(fam, x.lower())], steps=PEST_STEPS if fam == "pest" else ISO_STEPS)
            service_page(hp + x.lower() + "/", d, (name, hp), fam, slug=x.lower())

    # home
    pest_cards = "".join(f'<a class="card" href="/pest-control/{s}/">{card_icon("pest", s)}<h3>{E(fmt(PEST[s]["service"]))}</h3><span class="more">Learn more</span></a>' for s in PEST["hub"]["children"])
    iso_cards = "".join(f'<a class="card" href="/iso-consultancy/{s}/">{card_icon("iso", s)}<h3>{E(ISO[s]["service"])}</h3><span class="more">Learn more</span></a>' for s in ISO["hub"]["children"])
    home = f"""<div class="hero home"><div class="wrap"><p class="eyebrow">{E(" · ".join(CITIES))}</p>
<h1>Pest Control and ISO Consultancy in Saudi Arabia</h1>
<p class="lead">Inspection-led pest management and practical ISO implementation, from one company.</p>
<div class="cta">{btn_wa(wa_link('Hello, I would like to enquire'))}{btn_call()}</div>{trust('home')}</div></div>
<div class="wrap doors">
<a class="door t-pest" href="/pest-control/"><div class="art">{illus_pest()}</div><div class="door-txt"><p class="kicker">For homes and facilities</p><h2>Pest Control in {E(city)}</h2><p>Termites, rodents, cockroaches, bed bugs, fumigation and scheduled IPM programmes.</p><span class="more">Book a free inspection</span></div></a>
<a class="door t-iso" href="/iso-consultancy/"><div class="art">{illus_iso('ISO 9001 · 22000 · 45001')}</div><div class="door-txt"><p class="kicker">For companies seeking certification</p><h2>ISO Consultancy</h2><p>Gap analysis, documentation, internal audit and certification preparation.</p><span class="more">Book a free consultation</span></div></a>
</div>
<section class="t-pest"><div class="wrap"><p class="kicker">Pest control</p><h2 class="s">Pest control services</h2><div class="cards">{pest_cards}</div></div></section>
<section class="alt t-iso"><div class="wrap"><p class="kicker">ISO consultancy</p><h2 class="s">ISO standards we support</h2><div class="cards">{iso_cards}</div></div></section>
<section id="how"><div class="wrap"><p class="kicker">How we work</p><h2 class="s">Clear steps, written records</h2><p class="sub">Every job follows the same path: we inspect or assess first, agree the plan in writing, do the work, and give you the paperwork.</p><div class="lanes">{lane("pest")}{lane("iso")}</div></div></section>
<section class="alt"><div class="wrap narrow"><p class="kicker">One provider</p><h2 class="s">Why food, hospitality and industrial clients use both</h2>
<p class="sub">Food-safety audits look at both your management system and your pest control records. Working with one company for both makes audits simpler.</p>
<a class="btn btn-call" href="/contact/">Talk to us</a></div></section>
<div class="cta-band"><div class="wrap"><h2>Tell us what you need</h2><p>We respond with next steps.</p><div class="cta">{btn_wa(WA)}{btn_call("Call now")}</div></div></div>"""
    page("/", "Pest Control & ISO Consultancy in Saudi Arabia | Omnexa Solutions",
         "Pest control and ISO consultancy in Saudi Arabia. Free site inspection and free ISO consultation. Termites, rodents, ISO 9001, 22000, 45001.", home)

    process_page("pest")
    process_page("iso")
    process_hub()

    # other services
    cr = [("Home", "/"), ("Other services", "/facility-services/")]
    cards = "".join(f'<div class="card plain"><h3>{E(a)}</h3><p>{E(b)}</p><ul class="mini">' + "".join(f"<li>{E(x)}</li>" for x in c) + "</ul></div>" for a, b, c in OTHER)
    body = f"""{simple_hero(cr, 'Facility and Technical Services', 'We also provide these services. Contact us for a quotation.')}
<section><div class="wrap"><div class="cards wide">{cards}</div><div class="cta" style="margin-top:28px">{btn_wa(WA)}{btn_call()}</div></div></section>"""
    page("/facility-services/", "Facility & Technical Services | Omnexa Solutions", "HVAC, construction, safety signage and equipment, and IT services from Omnexa Solutions in Saudi Arabia.", body, crumbs=cr)

    # about
    cr = [("Home", "/"), ("About", "/about/")]
    vals = "".join(f'<div class="card plain"><h3>{E(t)}</h3><p>{E(d)}</p></div>' for t, d in VALUES)
    sec = "".join(f"<li>{E(x)}</li>" for x in SECTORS)
    body = f"""{simple_hero(cr, 'About ' + C['brand'], 'Pest management, ISO consultancy and training, and facility services for businesses in Saudi Arabia.')}
<section><div class="wrap two"><div><p class="kicker">Who we are</p><h2 class="s">One company for pest control and ISO</h2>
<p class="sub">{E(C['brand'])} provides Integrated Pest Management (pesticide and non-pesticide), ISO consultancy and training, and facility services including air-conditioning, construction and IT. Our office is at {E(C['street_address'] or C['address_note'])}.</p>
<p class="sub">We also advise and train in environment, health and safety, quality management, Integrated Pest Management and food safety management.</p></div>
<div class="art"><img class="about-logo" src="/assets/logo.png" width="360" height="94" alt="{E(C['brand'])}" loading="lazy"></div></div></section>
<section class="alt"><div class="wrap"><div class="cards wide"><div class="card plain"><h3>Our mission</h3><p>To give clients dependable service, and to make sure our staff, products and equipment meet the standards our clients set.</p></div>
<div class="card plain"><h3>Our vision</h3><p>To be the pest management and facility services provider that clients choose for reliability and value.</p></div></div></div></section>
<section><div class="wrap"><p class="kicker">What we stand for</p><h2 class="s">Our values</h2><div class="cards wide">{vals}</div></div></section>
<section class="alt"><div class="wrap"><p class="kicker">Where we work</p><h2 class="s">Sectors we serve</h2><p class="sub">Our pest control and consultancy cover public health and food safety across these kinds of sites.</p><ul class="ticks">{sec}</ul></div></section>
<!-- TODO: add verified company facts, licences, certificate details, team and client list. Nothing is shown here until provided. -->
<div class="cta-band"><div class="wrap"><h2>Talk to us</h2><p>Free site inspection and free ISO consultation.</p><div class="cta">{btn_wa(WA)}{btn_call("Call now")}</div></div></div>"""
    page("/about/", "About Omnexa Solutions", "About Omnexa Solutions: pest management, ISO consultancy and training, and facility services in Saudi Arabia.", body, crumbs=cr)

    # contact
    cr = [("Home", "/"), ("Contact", "/contact/")]
    body = f"""{simple_hero(cr, 'Contact us', 'Phone and WhatsApp are the fastest ways to reach us.')}
<section><div class="wrap two"><div class="contact"><p><b>Phone</b><a href="tel:{C['phone']}">{E(C['phone_display'])}</a></p><p><b>WhatsApp</b><a href="{WA}">Chat on WhatsApp</a></p><p><b>Email</b><a href="mailto:{C['email']}">{E(C['email'])}</a></p><p><b>Office</b>{E(C['street_address'] or C['address_note'])}</p></div>
<div class="card formcard"><h2>Send an enquiry</h2>{form('Other')}</div></div></section>"""
    page("/contact/", "Contact Omnexa Solutions", "Contact Omnexa Solutions by phone, WhatsApp or email for pest control and ISO consultancy.", body, crumbs=cr)

    # privacy
    body = f"""{simple_hero([('Home','/'),('Privacy','/privacy/')], 'Privacy', 'How we handle enquiry details.')}
<section><div class="wrap narrow"><p class="sub">When you submit the enquiry form, your name, phone number and message are sent to us through WhatsApp{' and our form service' if C['form_endpoint'] else ''} so we can reply. We use analytics to measure site use. Contact {E(C['email'])} to ask us to delete your data.</p></div></section>"""
    page("/privacy/", "Privacy | Omnexa Solutions", "Privacy information for Omnexa Solutions.", body)

    write("/404.html", f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found</title><meta name="robots" content="noindex">{FONTS}<link rel="stylesheet" href="/assets/style.css"></head><body class="t-home">{header()}<main><div class="hero slim"><div class="wrap"><h1>Page not found</h1><p class="lead"><a href="/">Back to home</a></p></div></div></main></body></html>""")

    urls = "".join(f"<url><loc>{BASE}{p}</loc></url>" for p in PAGES)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    print(len(PAGES), "pages built")


build()
