#!/usr/bin/env python3
"""Static site generator. Run: python3 src/build.py  ->  writes ./public"""
import json, html, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import PEST, ISO, OTHER

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public")
C = json.load(open(os.path.join(ROOT, "src", "config.json"), encoding="utf-8"))
E = html.escape
city = C["primary_city"]
BASE = C["base_url"].rstrip("/")
PAGES = []  # (url path) for sitemap


def fmt(s):
    return s.replace("{city}", city)


def write(path, content):
    full = os.path.join(OUT, path.strip("/"), "index.html") if not path.endswith(".html") else os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


def business_ld():
    o = {"@context": "https://schema.org", "@type": "LocalBusiness", "@id": BASE + "/#business", "name": C["brand"],
         "url": BASE + "/", "telephone": C["phone"], "email": C["email"],
         "areaServed": [{"@type": "Country", "name": C["country"]}],
         "address": {"@type": "PostalAddress", "addressLocality": city, "addressCountry": "SA"}}
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


ICON = {
 "bug": '<svg viewBox="0 0 24 24" aria-hidden="true"><ellipse cx="12" cy="14" rx="5" ry="6"/><circle cx="12" cy="6.5" r="2.5"/><path d="M7 11 4 9M17 11l3-2M7 15H4M17 15h3M8 19l-3 2M16 19l3 2M12 8v12"/></svg>',
 "shield": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="m8.5 12 2.5 2.5 4.5-5"/></svg>',
 "doc": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5M9 13h7M9 17h5"/></svg>',
}


def ic(kind):
    return '<span class="ic">' + ICON[kind] + '</span>'


WA = "https://wa.me/" + C["whatsapp"]


def wa_link(text):
    return WA + "?text=" + text.replace(" ", "%20")


def header():
    return f"""<header class="site"><div class="wrap">
<a class="brand" href="/">{E(C['brand'])}</a>
<nav class="main" aria-label="Main"><a href="/pest-control/">Pest Control</a><a href="/iso-consultancy/">ISO Consultancy</a><a href="/facility-services/">Other Services</a><a href="/about/">About</a><a href="/contact/">Contact</a></nav>
<a class="btn btn-call" href="tel:{C['phone']}">Call {E(C['phone_display'])}</a>
</div></header>"""


def footer():
    pest = "".join(f'<li><a href="/pest-control/{s}/">{E(fmt(PEST[s]["service"]))}</a></li>' for s in PEST["hub"]["children"])
    iso = "".join(f'<li><a href="/iso-consultancy/{s}/">{E(ISO[s]["service"])}</a></li>' for s in ISO["hub"]["children"])
    addr = E(C["street_address"] or C["address_note"])
    return f"""<footer class="site"><div class="wrap"><div class="cols">
<div><h4>{E(C['brand'])}</h4><p>{addr}</p><p><a href="tel:{C['phone']}">{E(C['phone_display'])}</a><br><a href="mailto:{C['email']}">{E(C['email'])}</a></p></div>
<div><h4>Pest Control</h4><ul>{pest}</ul></div>
<div><h4>ISO Consultancy</h4><ul>{iso}</ul></div>
<div><h4>Company</h4><ul><li><a href="/facility-services/">Other services</a></li><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li><li><a href="/privacy/">Privacy</a></li></ul></div>
</div><p style="margin-top:24px">&copy; 2026 {E(C['brand'])}</p></div></footer>
<div class="sticky"><a class="btn btn-call" href="tel:{C['phone']}">Call</a><a class="btn btn-wa" href="{WA}">WhatsApp</a></div>"""


def form(service, dark=False):
    opts = ["Pest Control", "Termite Control", "Rodent Control", "Cockroach / Insect Control", "Bed Bug Treatment", "Fumigation",
            "Commercial IPM Programme", "ISO Consultancy", "ISO 9001", "ISO 22000", "ISO 45001", "ISO 14001", "ISO 27001", "Other"]
    if service not in opts:
        opts.insert(0, service)
    o = "".join(f'<option{" selected" if x == service else ""}>{E(x)}</option>' for x in opts)
    return f"""<form class="lead" data-wa="{C['whatsapp']}" data-endpoint="{E(C['form_endpoint'])}">
<label for="n">Name</label><input id="n" name="name" required autocomplete="name">
<label for="p">Phone / WhatsApp</label><input id="p" name="phone" type="tel" required autocomplete="tel">
<label for="s">Service</label><select id="s" name="service">{o}</select>
<label for="c">City</label><input id="c" name="city" value="{E(city)}">
<label for="m">Details (optional)</label><textarea id="m" name="message" rows="2"></textarea>
<button class="btn btn-wa" type="submit">Send via WhatsApp</button>
<p class="small">Opens WhatsApp with your details filled in. We reply during business hours.</p></form>"""


def trust(family="pest"):
    p = C["proof"]
    items = []
    if p["iso9001_certificate"]:
        items.append("ISO 9001 certified: " + p["iso9001_certificate"])
    if p["pest_licence"]:
        items.append("Licence: " + p["pest_licence"])
    if p["years_in_service"]:
        items.append(p["years_in_service"] + " years in service")
    items += (["Free site inspection", "Written service records"] if family == "pest" else ["Free consultation", "Gap analysis and audit preparation"]) + [f"Serving {city} and Saudi Arabia"]
    return '<div class="trust">' + "".join(f"<span>✓ {E(i)}</span>" for i in items) + "</div>"


def page(path, title, desc, body, extra_ld=None, crumbs=None, noindex=False):
    url = BASE + path
    ldo = [business_ld()] if path == "/" else []
    if crumbs:
        ldo.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u} for i, (n, u) in enumerate(crumbs)]})
    ldo += extra_ld or []
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">{robots}
<meta property="og:type" content="website"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}">
<script>document.documentElement.className="js"</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
{''.join(ld(o) for o in ldo)}
{gtm_head()}</head><body class="{"fam-pest" if path.startswith("/pest-control") else "fam-iso" if path.startswith("/iso-consultancy") else "fam-home"}">{gtm_body()}
{header()}
{body}
{footer()}
<script src="/assets/site.js" defer></script></body></html>"""
    write(path, doc)
    if not noindex:
        PAGES.append(path)


def crumbs_html(items):
    return '<div class="wrap crumbs">' + " › ".join(f'<a href="{u}">{E(n)}</a>' if u else E(n) for n, u in items) + "</div>"


def service_page(path, d, parent, family):
    h1, title, desc = fmt(d["h1"]), fmt(d["title"]), fmt(d["desc"])
    cr = [("Home", "/")]
    if parent:
        cr.append((parent[0], parent[1]))
    cr.append((h1, path))
    ticks = "".join(f"<li>{E(fmt(b))}</li>" for b in d["bullets"])
    steps = "".join(f"<li><b>{E(a)}</b>{E(b)}</li>" for a, b in d["steps"])
    faq = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in d["faqs"])
    related = ""
    if "children" in d:
        base = "/" + d["slug"] + "/"
        src = PEST if family == "pest" else ISO
        cards = "".join(f'<a class="card" href="{base}{c}/">{ic("bug" if family == "pest" else "doc")}<h3>{E(fmt(src[c]["h1"]))}</h3><p>{E(fmt(src[c]["lead"]))}</p></a>' for c in d["children"])
        related = f'<section class="alt"><div class="wrap"><h2 class="s">Our {E(d["service"])} services</h2><div class="cards">{cards}</div></div></section>'
    elif parent:
        related = f'<section class="alt"><div class="wrap"><p>See all <a href="{parent[1]}">{E(parent[0])}</a> services.</p></div></section>'
    notice = ""
    if family == "iso":
        notice = '<div class="notice">We are ISO consultants. Certificates are issued by an accredited certification body of your choice; we prepare you for its audit.</div>'
    cta_text = wa_link("Hello, I need " + d["service"])
    body = f"""{crumbs_html(cr)}
<div class="hero"><div class="hero-bg" aria-hidden="true"><i></i><i></i><i></i></div><div class="wrap grid"><div><h1>{E(h1)}</h1><p class="lead">{E(fmt(d['lead']))}</p>
<div class="cta"><a class="btn btn-wa" href="{cta_text}">WhatsApp us</a><a class="btn btn-call" href="tel:{C['phone']}">Call {E(C['phone_display'])}</a></div>{trust(family)}</div>
<div class="card"><h2>Request a free {'inspection' if family=='pest' else 'consultation'}</h2>{form(d['service'])}</div></div></div>
<section><div class="wrap"><h2 class="s">{E(h1)}: what we do</h2><p class="sub">{E(fmt(d['intro']))}</p><ul class="ticks">{ticks}</ul>{notice}</div></section>
<section class="alt"><div class="wrap"><h2 class="s">How it works</h2><ol class="steps">{steps}</ol></div></section>
{related}
<section><div class="wrap"><h2 class="s">Frequently asked questions</h2>{faq}</div></section>
<div class="cta-band"><h2>{'Book your free inspection' if family=='pest' else 'Book your free consultation'}</h2><p>Tell us about your site and we will contact you.</p>
<div class="cta"><a class="btn btn-wa" href="{cta_text}">WhatsApp us</a><a class="btn btn-call" href="tel:{C['phone']}">Call now</a></div></div>"""
    svc = {"@context": "https://schema.org", "@type": "Service", "name": h1, "serviceType": d["service"],
           "provider": {"@type": "LocalBusiness", "@id": BASE + "/#business", "name": C["brand"], "telephone": C["phone"]},
           "areaServed": {"@type": "Country", "name": C["country"]}, "url": BASE + path, "description": desc}
    fq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faqs"]]}
    page(path, title, desc, body, [svc, fq], cr)


def build():
    # service pages
    for fam, data, name in (("pest", PEST, "Pest Control"), ("iso", ISO, "ISO Consultancy")):
        hub = data["hub"]
        hp = "/" + hub["slug"] + "/"
        service_page(hp, hub, None, fam)
        for k in hub["children"]:
            service_page(hp + k + "/", {**data[k], "slug": hub["slug"]}, (name, hp), fam)

    # home
    pest_cards = "".join(f'<a class="card f-pest" href="/pest-control/{s}/">{ic("bug")}<h3>{E(fmt(PEST[s]["service"]))}</h3></a>' for s in PEST["hub"]["children"])
    iso_cards = "".join(f'<a class="card f-iso" href="/iso-consultancy/{s}/">{ic("doc")}<h3>{E(ISO[s]["service"])}</h3></a>' for s in ISO["hub"]["children"])
    home = f"""<div class="hero"><div class="hero-bg" aria-hidden="true"><i></i><i></i><i></i></div><div class="wrap"><span class="eyebrow">Saudi Arabia</span><h1>Pest Control and <em>ISO Consultancy</em> in Saudi Arabia</h1>
<p class="lead">Inspection-led pest management and practical ISO implementation, from one company. Free site inspection and free ISO consultation.</p>
<div class="cta"><a class="btn btn-wa" href="{wa_link('Hello, I would like to enquire')}">WhatsApp us</a><a class="btn btn-call" href="tel:{C['phone']}">Call {E(C['phone_display'])}</a></div>{trust()}</div></div>
<section><div class="wrap"><div class="cards">
<a class="card feature f-pest" href="/pest-control/">{ic("bug")}<h3>Pest Control in {E(city)}</h3><p>Termites, rodents, cockroaches, bed bugs, fumigation and commercial IPM programmes.</p><p><b>View pest control →</b></p></a>
<a class="card feature f-iso" href="/iso-consultancy/">{ic("shield")}<h3>ISO Consultancy</h3><p>ISO 9001, 22000, 45001, 14001 and 27001: gap analysis, documentation and certification preparation.</p><p><b>View ISO consultancy →</b></p></a></div></div></section>
<section class="alt"><div class="wrap"><h2 class="s">Pest control services</h2><div class="cards">{pest_cards}</div></div></section>
<section><div class="wrap"><h2 class="s">ISO standards we support</h2><div class="cards">{iso_cards}</div></div></section>
<section class="alt"><div class="wrap"><h2 class="s">Why food, hospitality and industrial clients use both</h2>
<p class="sub">Food-safety audits look at both your management system and your pest control records. Working with one company for both makes audits simpler.</p>
<div class="cta"><a class="btn btn-primary" href="/contact/">Talk to us</a></div></div></section>
<div class="cta-band"><h2>Tell us what you need</h2><p>We respond with next steps.</p><div class="cta"><a class="btn btn-wa" href="{WA}">WhatsApp us</a><a class="btn btn-call" href="tel:{C['phone']}">Call now</a></div></div>"""
    page("/", "Pest Control & ISO Consultancy in Saudi Arabia | Omnexa Solutions",
         "Pest control and ISO consultancy in Saudi Arabia. Free site inspection and free ISO consultation. Termites, rodents, ISO 9001, 22000, 45001.", home)

    # other services
    cards = "".join(f'<div class="card"><h3>{E(a)}</h3><p>{E(b)}</p></div>' for a, b in OTHER)
    body = f"""{crumbs_html([('Home','/'),('Other services','/facility-services/')])}<div class="hero"><div class="hero-bg" aria-hidden="true"><i></i><i></i><i></i></div><div class="wrap"><h1>Facility and Technical Services</h1><p class="lead">We also provide these services. Contact us for a quotation.</p></div></div>
<section><div class="wrap"><div class="cards">{cards}</div><div class="cta" style="margin-top:20px"><a class="btn btn-wa" href="{WA}">WhatsApp us</a></div></div></section>"""
    page("/facility-services/", "Facility & Technical Services | Omnexa Solutions", "HVAC, electrical, plumbing and construction services from Omnexa Solutions in Saudi Arabia.", body,
         crumbs=[("Home", "/"), ("Other services", "/facility-services/")])

    # about
    body = f"""{crumbs_html([('Home','/'),('About','/about/')])}<section><div class="wrap"><h1>About {E(C['brand'])}</h1>
<p class="sub">{E(C['brand'])} provides pest control and ISO consultancy in Saudi Arabia, with additional facility services. Our office is at {E(C['street_address'] or C['address_note'])}.</p>
<!-- TODO: add verified company facts, licences, certificate details, team and client list. Nothing is shown here until provided. --></div></section>"""
    page("/about/", "About Omnexa Solutions", "About Omnexa Solutions: pest control and ISO consultancy in Saudi Arabia.", body, crumbs=[("Home", "/"), ("About", "/about/")])

    # contact
    body = f"""{crumbs_html([('Home','/'),('Contact','/contact/')])}<section><div class="wrap" style="display:grid;gap:24px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr))">
<div><h1>Contact us</h1><p><a href="tel:{C['phone']}">{E(C['phone_display'])}</a></p><p><a href="{WA}">WhatsApp</a></p><p><a href="mailto:{C['email']}">{E(C['email'])}</a></p><p>{E(C['street_address'] or C['address_note'])}</p></div>
<div class="card"><h2>Send an enquiry</h2>{form('Other')}</div></div></section>"""
    page("/contact/", "Contact Omnexa Solutions", "Contact Omnexa Solutions by phone, WhatsApp or email for pest control and ISO consultancy.", body, crumbs=[("Home", "/"), ("Contact", "/contact/")])

    # privacy
    body = f"""<section><div class="wrap"><h1>Privacy</h1><p class="sub">When you submit the enquiry form, your name, phone number and message are sent to us through WhatsApp{' and our form service' if C['form_endpoint'] else ''} so we can reply. We use analytics to measure site use. Contact {E(C['email'])} to ask us to delete your data.</p></div></section>"""
    page("/privacy/", "Privacy | Omnexa Solutions", "Privacy information for Omnexa Solutions.", body)

    # 404
    write("/404.html", """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found</title><meta name="robots" content="noindex"><link rel="stylesheet" href="/assets/style.css"></head><body><section><div class="wrap"><h1>Page not found</h1><p><a href="/">Back to home</a></p></div></section></body></html>""")

    urls = "".join(f"<url><loc>{BASE}{p}</loc></url>" for p in PAGES)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    print(len(PAGES), "pages built")


build()
