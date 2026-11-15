#!/usr/bin/env python3
"""Static site generator. Run: python3 src/build.py  ->  writes ./public"""
import json, html, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import re
from urllib.parse import quote
from process import scene
import content as CONTENT_EN
import process as PROCESS_EN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public")
C = json.load(open(os.path.join(ROOT, "src", "config.json"), encoding="utf-8"))
E = html.escape
CITIES = C["cities"]
city = " and ".join(CITIES)
BASE = C["base_url"].rstrip("/")
PAGES = []  # (url path) for sitemap


LANG = "en"
CITY_AR = {"Riyadh": "الرياض", "Jeddah": "جدة"}


def T(en, ar):
    return ar if LANG == "ar" else en


def cname(x):
    return CITY_AR.get(x, x) if LANG == "ar" else x


def city_all():
    return " و".join(CITY_AR[x] for x in CITIES) if LANG == "ar" else " and ".join(CITIES)


def P(path):
    """Public path for the current language."""
    if LANG == "ar":
        return "/ar" + path if path != "/" else "/ar/"
    return path


def ltr(x):
    return f'<bdi dir="ltr">{x}</bdi>'


def use(lang):
    """Select the content for a language and expose it as module globals."""
    global LANG, PEST, ISO, OTHER, EXTRA, MORE_FAQS, VALUES, CITY_PAGES, PEST_STEPS, ISO_STEPS, PROCESS, SAMPLE_REPORT, SAMPLE_GANTT, IMG
    LANG = lang
    m = CONTENT_EN
    pm = PROCESS_EN
    if lang == "ar":
        import content_ar as m
        pm = m
    PEST, ISO, OTHER, EXTRA, MORE_FAQS, VALUES = m.PEST, m.ISO, m.OTHER, m.EXTRA, m.MORE_FAQS, m.VALUES
    CITY_PAGES, PEST_STEPS, ISO_STEPS = m.CITY_PAGES, m.PEST_STEPS, m.ISO_STEPS
    PROCESS, SAMPLE_REPORT, SAMPLE_GANTT = pm.PROCESS, pm.SAMPLE_REPORT, pm.SAMPLE_GANTT
    IMG = IMG_AR if lang == "ar" else IMG_EN


def brand():
    return C["brand_ar"] if LANG == "ar" else C["brand"]


def legal_name():
    return (C.get("legal_name_ar") if LANG == "ar" else C.get("legal_name")) or brand()


def fmt(s):
    lic = C["proof"]["pest_licence"]
    return s.replace("{city}", city_all()).replace("{pest_licence_line}", ((" Our qualification: " + lic + ".") if LANG == "en" else (" مؤهلنا: " + lic + ".")) if lic else "")


def loc(h):
    """Point internal links at the Arabic copy of the site."""
    if LANG != "ar":
        return h
    h = re.sub(r'href="/(?!ar/|assets/|__en__/)', 'href="/ar/', h)
    return h.replace('href="/__en__/', 'href="/')


def write(path, content):
    full = os.path.join(OUT, path.strip("/"), "index.html") if not path.endswith(".html") else os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


def business_ld():
    o = {"@context": "https://schema.org", "@type": "LocalBusiness", "@id": BASE + "/#business", "name": brand(),
         "url": BASE + P("/"), "telephone": C["phone"], "email": C["email"],
         "areaServed": [{"@type": "City", "name": cname(x)} for x in CITIES] + [{"@type": "Country", "name": T(C["country"], "المملكة العربية السعودية")}],
         "address": {"@type": "PostalAddress", "addressLocality": cname(CITIES[0]), "postalCode": C.get("postal_code", ""), "addressCountry": "SA"}}
    o["location"] = [{"@type": "Place", "name": T(f["label"], f["label_ar"]), "address": {"@type": "PostalAddress", "streetAddress": T(f["address"].replace(", Saudi Arabia", ""), f["address_ar"]), "addressLocality": cname(f["city"]), "addressCountry": "SA"}} for f in C.get("offices", [])]
    if C.get("legal_name"):
        o["legalName"] = legal_name()
    if C["proof"].get("vat_number"):
        o["vatID"] = C["proof"]["vat_number"]
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
    "cap": _svg('<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11.5V16c0 1.5 3 3 6 3s6-1.5 6-3v-4.5M22 9v6"/>'),
    "phone": _svg('<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>'),
}
PEST_ICON = {"termite-control": "termite", "rodent-control": "rodent", "cockroach-control": "roach",
             "bed-bug-treatment": "bed", "fumigation": "fume", "commercial-ipm": "building",
             "mosquito-control": "mosquito", "bird-control": "bird", "wildlife-control": "snake"}
ISO_ICON = {"training": "people", "other-standards": "grid", "iso-9001-training": "cap", "iso-14001-training": "cap", "iso-45001-training": "cap", "iso-22000-training": "cap", "iso-27001-training": "cap"}


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
    sub = T("integrated pest management", "الإدارة المتكاملة للآفات")
    if LANG == "en":
        labels = ("ASSESS", "PREVENT", "CONTROL")
    else:
        labels = ("التقييم", "الوقاية", "المكافحة")
    aria = T("The IPM cycle: assess, prevent, control", "دورة الإدارة المتكاملة للآفات: التقييم والوقاية والمكافحة")
    # the arcs run left (assess) -> right (prevent) -> bottom (control); Arabic reads the same cycle right-to-left
    left, right, bottom = (labels[0], labels[1], labels[2]) if LANG == "en" else (labels[1], labels[0], labels[2])
    return f'''<svg class="illus ipm" viewBox="0 0 360 280" role="img" aria-label="{aria}">
<g class="ipm-ring"><path class="ar a1" d="M180 40a100 100 0 0 1 86.6 50"/><path class="ar a2" d="M266.6 190a100 100 0 0 1-173.2 0"/><path class="ar a3" d="M93.4 90A100 100 0 0 1 180 40"/>
<path class="fl1" d="m272 84 8 20-21-3z"/><path class="fl2" d="m88 206-8-20 21 3z"/><path class="fl3" d="m96 78 20-9-4 21z"/></g>
<circle class="core" cx="180" cy="140" r="52"/><text class="cn" x="180" y="136" text-anchor="middle">IPM</text><text class="cs" x="180" y="156" text-anchor="middle">{sub}</text>
<text class="lb" x="340" y="52" text-anchor="end">{right}</text><text class="lb" x="180" y="266" text-anchor="middle">{bottom}</text><text class="lb" x="20" y="52" text-anchor="start">{left}</text>
</svg>'''


def illus_iso(label=None):
    label = label or T("MANAGEMENT SYSTEM", "نظام الإدارة")
    rows = [T("Gap analysis", "تحليل الفجوات"), T("Documentation", "التوثيق"), T("Internal audit", "التدقيق الداخلي"), T("Certification audit", "تدقيق منح الشهادة")]
    aria = T("An audit checklist being completed, with a certification seal", "قائمة تدقيق يجري استكمالها مع ختم شهادة")
    r = ""
    if LANG == "en":
        for i, t in enumerate(rows):
            y = 96 + i * 34
            r += (f'<rect class="box" x="92" y="{y}" width="18" height="18" rx="4"/><path class="tick draw d{i}" pathLength="1" d="M96 {y+9}l4 4 7-8"/>'
                  f'<text class="row" x="122" y="{y+13}">{t}</text>')
        head = (f'<text class="mono" x="92" y="52">{E(label)}</text><rect class="rule" x="92" y="64" width="120" height="5" rx="2.5"/><rect class="rule" x="92" y="76" width="76" height="5" rx="2.5"/>')
        seal = "262 222"
    else:
        for i, t in enumerate(rows):
            y = 96 + i * 34
            r += (f'<rect class="box" x="238" y="{y}" width="18" height="18" rx="4"/><path class="tick draw d{i}" pathLength="1" d="M242 {y+9}l4 4 7-8"/>'
                  f'<text class="row" x="228" y="{y+13}" text-anchor="end">{t}</text>')
        head = (f'<text class="mono ar" x="256" y="52" text-anchor="end">{E(label)}</text><rect class="rule" x="136" y="64" width="120" height="5" rx="2.5"/><rect class="rule" x="180" y="76" width="76" height="5" rx="2.5"/>')
        seal = "98 222"
    return f'''<svg class="illus" viewBox="0 0 360 280" role="img" aria-label="{aria}">
<rect class="doc-shadow" x="{84 if LANG == 'en' else 72}" y="30" width="204" height="238" rx="10"/>
<rect class="doc" x="{72 if LANG == 'en' else 84}" y="18" width="204" height="238" rx="10"/>
{head}
{r}
<g transform="translate({seal})"><g class="pop"><path class="ribbon" d="M-14 20l-7 26 13-8zM14 20l7 26-13-8z"/><circle class="seal-c" r="32"/><circle class="seal-r" r="24"/><path class="seal-ck" d="M-10 0l7 7 13-15"/></g></g>
</svg>'''


# ---------- shared chrome ----------
WA = "https://wa.me/" + C["whatsapp"]


def wa_link(text):
    return WA + "?text=" + quote(text)


def btn_wa(href, label=None):
    return f'<a class="btn btn-wa" href="{href}">{ICON["wa"]}{label or T("WhatsApp us", "تواصل عبر واتساب")}</a>'


def btn_call(label=None):
    return f'<a class="btn btn-call" href="tel:{C["phone"]}">{ICON["phone"]}{label or (T("Call ", "اتصل ") + ltr(E(C["phone_display"])))}</a>'


CURPATH = "/"


def header():
    other = ("/__en__" + CURPATH) if LANG == "ar" else ("/ar" + CURPATH if CURPATH != "/" else "/ar/")
    sw = T("العربية", "English")
    swl = T("ar", "en")
    return f"""<header class="site"><div class="wrap">
<a class="brand" href="/"><img src="/assets/logo.png" width="154" height="40" alt="{E(brand())}"></a>
<button class="menu-btn" type="button" aria-label="{T('Menu', 'القائمة')}" aria-expanded="false" aria-controls="mnav"><span class="mb-i"></span></button>
<nav class="main" id="mnav" aria-label="{T('Main', 'القائمة الرئيسية')}"><a href="/pest-control/">{T('Pest Control', 'مكافحة الحشرات')}</a><a href="/iso-consultancy/">{T('ISO Consultancy', 'استشارات الأيزو')}</a><a href="/how-it-works/">{T('How It Works', 'آلية العمل')}</a><a href="/facility-services/">{T('Other Services', 'خدمات أخرى')}</a><a href="/about/">{T('About', 'من نحن')}</a><a href="/contact/">{T('Contact', 'اتصل بنا')}</a>
<div class="menu-extra"><a class="btn btn-call" href="tel:{C['phone']}">{ICON['phone']}{T('Call', 'اتصل')}</a><a class="btn btn-wa" href="{WA}">{ICON['wa']}{T('WhatsApp', 'واتساب')}</a></div></nav>
<a class="lang" href="{other}" hreflang="{swl}" lang="{swl}">{sw}</a>
<a class="btn btn-ghost" href="tel:{C['phone']}">{ICON['phone']}{ltr(E(C['phone_display']))}</a>
</div></header>"""


def office_label(o):
    return o["label_ar"] if LANG == "ar" else o["label"]


def office_addr(o):
    return o["address_ar"] if LANG == "ar" else o["address"]


def offices_html():
    return "".join(f'<p><b>{E(office_label(o))}</b><br>{E(office_addr(o))}</p>' for o in C.get("offices", [])) or f'<p>{E(C["address_note"])}</p>'


def office_for(city):
    for o in C.get("offices", []):
        if o["city"] == city:
            return office_addr(o)
    return ""


IMG_EN = {
    "field-fogging": ("Technician fogging a residential area", 246, 242), "field-warehouse": ("Technician treating a warehouse", 171, 169),
    "field-termite": ("Termite treatment by drilling and injection", 150, 148), "field-bait-station": ("Rodent bait station being checked", 141, 138),
    "field-aircon": ("Technician servicing an air conditioner", 165, 164),
    "sector-government": ("Government building", 297, 187), "sector-mall": ("Shopping mall", 296, 187), "sector-hotel": ("Hotel", 296, 186),
    "sector-hospital": ("Hospital", 297, 187), "sector-bank": ("Bank building", 297, 186), "sector-restaurant": ("Restaurant", 297, 187),
    "sector-food-industry": ("Food production line", 297, 186),
}
IMG_AR = {
    "field-fogging": ("فني يقوم بالرش الضبابي لمكافحة الحشرات في منطقة سكنية", 246, 242), "field-warehouse": ("فني يعالج مستودعاً", 171, 169),
    "field-termite": ("معالجة النمل الأبيض بالحفر والحقن", 150, 148), "field-bait-station": ("فحص محطة طعوم للقوارض", 141, 138),
    "field-aircon": ("فني يصيّن مكيّف هواء", 165, 164),
    "sector-government": ("مبنى حكومي", 297, 187), "sector-mall": ("مركز تسوق", 296, 187), "sector-hotel": ("فندق", 296, 186),
    "sector-hospital": ("مستشفى", 297, 187), "sector-bank": ("مبنى بنك", 297, 186), "sector-restaurant": ("مطعم", 297, 187),
    "sector-food-industry": ("خط إنتاج غذائي", 297, 186),
}


def img(name, cls=""):
    alt, w, h = IMG[name]
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="/assets/img/{name}.webp" width="{w}" height="{h}" alt="{E(alt)}" loading="lazy">'


def field_strip():
    items = [("field-fogging", T("Fogging", "الرش الضبابي")), ("field-warehouse", T("Warehouse treatment", "معالجة المستودعات")),
             ("field-termite", T("Termite treatment", "معالجة النمل الأبيض")), ("field-bait-station", T("Rodent monitoring", "مراقبة القوارض"))]
    fig = "".join(f'<figure>{img(n, "round")}<figcaption>{E(t)}</figcaption></figure>' for n, t in items)
    return f'<section><div class="wrap"><p class="kicker">{T("In the field", "في الميدان")}</p><h2 class="s">{T("Trained teams, proper equipment", "فرق مدرّبة ومعدات مناسبة")}</h2><div class="field">{fig}</div></div></section>'


def sector_grid():
    items = [("sector-government", T("Government", "الجهات الحكومية")), ("sector-mall", T("Shopping malls", "مراكز التسوق")), ("sector-hotel", T("Hotels", "الفنادق")),
             ("sector-hospital", T("Hospitals", "المستشفيات")), ("sector-bank", T("Banks and offices", "البنوك والمكاتب")), ("sector-restaurant", T("Restaurants", "المطاعم")),
             ("sector-food-industry", T("Food industries", "الصناعات الغذائية"))]
    fig = "".join(f'<figure>{img(n, "sec")}<figcaption>{E(t)}</figcaption></figure>' for n, t in items)
    return f'<div class="sgrid">{fig}</div>'


def legal_line():
    p = C["proof"]
    bits = [E(legal_name())]
    if p.get("commercial_registration"):
        bits.append(T("CR ", "السجل التجاري ") + ltr(p["commercial_registration"]))
    if p.get("vat_number"):
        bits.append(T("VAT ", "الرقم الضريبي ") + ltr(p["vat_number"]))
    return " &middot; ".join(bits)


def company_box():
    p = C["proof"]
    rows = [(T("Legal name", "الاسم النظامي"), E(legal_name())), (T("Company type", "نوع الشركة"), E(T(C.get("legal_form", ""), C.get("legal_form_ar", ""))))]
    if p.get("commercial_registration"):
        rows.append((T("Commercial registration (CR)", "السجل التجاري"), ltr(p["commercial_registration"])))
    if p.get("vat_number"):
        rows.append((T("VAT registration number", "رقم التسجيل في ضريبة القيمة المضافة"), ltr(p["vat_number"])))
    rows.append((T("Registered address", "العنوان المسجّل"), E(T(C["address_note"], C["address_note_ar"]))))
    dl = "".join(f"<div><dt>{E(k)}</dt><dd>{v}</dd></div>" for k, v in rows if v)
    return f'<div class="paper company"><p class="kicker">{T("Company details", "بيانات الشركة")}</p><h3>{T("Registered in the Kingdom of Saudi Arabia", "مسجّلة في المملكة العربية السعودية")}</h3><dl>{dl}</dl></div>'


def footer():
    pest = "".join(f'<li><a href="/pest-control/{s}/">{E(fmt(PEST[s]["service"]))}</a></li>' for s in PEST["hub"]["children"])
    iso = "".join(f'<li><a href="/iso-consultancy/{s}/">{E(ISO[s]["service"])}</a></li>' for s in ISO["hub"]["children"])
    pl, il = T("Pest control", "مكافحة الحشرات"), T("ISO consultants", "استشارات الأيزو")
    areas = "".join(f'<li><a href="/{h}/{x.lower()}/">{l} {T("in", "في")} {E(cname(x))}</a></li>' for h, l in (("pest-control", pl), ("iso-consultancy", il)) for x in CITIES)
    return f"""<footer class="site"><div class="wrap"><div class="cols">
<div><p class="flogo"><img src="/assets/logo.png" width="190" height="50" alt="{E(brand())}" loading="lazy"></p>{offices_html()}<p><a href="tel:{C['phone']}">{ltr(E(C['phone_display']))}</a><br><a href="mailto:{C['email']}">{E(C['email'])}</a></p></div>
<div><h4>{pl}</h4><ul>{pest}</ul></div>
<div><h4>{T('ISO Consultancy', 'استشارات الأيزو')}</h4><ul>{iso}</ul></div>
<div><h4>{T('Areas', 'المناطق')}</h4><ul>{areas}</ul></div>
<div><h4>{T('Company', 'الشركة')}</h4><ul><li><a href="/how-it-works/">{T('How it works', 'آلية العمل')}</a></li><li><a href="/facility-services/">{T('Other services', 'خدمات أخرى')}</a></li><li><a href="/about/">{T('About', 'من نحن')}</a></li><li><a href="/contact/">{T('Contact', 'اتصل بنا')}</a></li><li><a href="/privacy/">{T('Privacy', 'الخصوصية')}</a></li></ul></div>
</div><p class="legal">{legal_line()}</p><p class="copy">&copy; 2026 {E(legal_name())}</p></div></footer>
<div class="sticky"><a class="btn btn-call" href="tel:{C['phone']}">{ICON['phone']}{T('Call', 'اتصل')}</a><a class="btn btn-wa" href="{WA}">{ICON['wa']}{T('WhatsApp', 'واتساب')}</a></div>"""


FORM_OPTS_EN = ["Pest Control", "Termite Control", "Rodent Control", "Cockroach / Insect Control", "Bed Bug Treatment", "Fumigation",
                "Commercial IPM Programme", "Mosquito / Dengue Control", "Bird Control", "Snake / Lizard / Stray Animal Control",
                "ISO Consultancy", "ISO 9001", "ISO 22000", "ISO 45001", "ISO 14001", "ISO 27001", "Other ISO Standards", "ISO Training", "ISO 9001 Training", "ISO 14001 Training", "ISO 45001 Training", "ISO 22000 and HACCP Training", "ISO 27001 Training", "Other"]
FORM_OPTS_AR = ["مكافحة الحشرات", "مكافحة النمل الأبيض", "مكافحة القوارض", "مكافحة الصراصير والحشرات", "مكافحة بق الفراش", "التبخير",
                "برنامج مكافحة تجاري متكامل", "مكافحة البعوض وحمى الضنك", "مكافحة الطيور", "مكافحة الثعابين والسحالي والحيوانات الضالة",
                "استشارات الأيزو", "ISO 9001", "ISO 22000", "ISO 45001", "ISO 14001", "ISO 27001", "معايير أيزو أخرى", "التدريب على الأيزو", "التدريب على ISO 9001", "التدريب على ISO 14001", "التدريب على ISO 45001", "التدريب على ISO 22000 وهاسب", "التدريب على ISO 27001", "أخرى"]


def form(service, sel_city=None):
    opts = list(FORM_OPTS_AR if LANG == "ar" else FORM_OPTS_EN)
    if service not in opts:
        opts.insert(0, service)
    o = "".join(f'<option{" selected" if x == service else ""}>{E(x)}</option>' for x in opts)
    copts = "".join(f'<option value="{E(cname(x))}"{" selected" if x == sel_city else ""}>{E(cname(x))}</option>' for x in CITIES) + f'<option>{T("Other city", "مدينة أخرى")}</option>'
    return f"""<form class="lead" data-wa="{C['whatsapp']}" data-endpoint="{E(C['form_endpoint'])}">
<label for="n">{T('Name', 'الاسم')}</label><input id="n" name="name" required autocomplete="name">
<label for="p">{T('Phone / WhatsApp', 'رقم الجوال / واتساب')}</label><input id="p" name="phone" type="tel" required autocomplete="tel" dir="ltr">
<label for="s">{T('Service', 'الخدمة')}</label><select id="s" name="service">{o}</select>
<label for="c">{T('City', 'المدينة')}</label><select id="c" name="city">{copts}</select>
<label for="m">{T('Details (optional)', 'تفاصيل (اختياري)')}</label><textarea id="m" name="message" rows="2"></textarea>
<button class="btn btn-wa" type="submit">{ICON['wa']}{T('Send via WhatsApp', 'إرسال عبر واتساب')}</button>
<p class="small">{T('Opens WhatsApp with your details filled in. We reply during business hours.', 'يفتح واتساب وتفاصيلك مكتوبة مسبقاً. نردّ خلال ساعات العمل.')}</p></form>"""


def trust(family="pest", override=None):
    p = C["proof"]
    items = []
    if override:
        return '<ul class="trust">' + "".join(f"<li>{E(i)}</li>" for i in override) + "</ul>"
    if p["iso9001_certificate"]:
        items.append(T("ISO 9001 certified: ", "حاصلة على ISO 9001: ") + p["iso9001_certificate"])
    if p["pest_licence"] and family != "iso":
        items.append(T("Licence: ", "الترخيص: ") + p["pest_licence"])
    if family == "pest":
        items += [T("Free site inspection", "فحص مجاني للموقع"), T("Written service records", "تقارير خدمة مكتوبة")]
    elif family == "iso":
        items += [T("Free consultation", "استشارة مجانية"), T("Gap analysis and audit preparation", "تحليل الفجوات والتحضير للتدقيق")]
    else:
        items += [T("Free site inspection", "فحص مجاني للموقع"), T("Free ISO consultation", "استشارة أيزو مجانية")]
    items.append(T(f"Serving {city_all()}", f"نخدم {city_all()}"))
    return '<ul class="trust">' + "".join(f"<li>{E(i)}</li>" for i in items) + "</ul>"


FONTS_EN = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500&family=IBM+Plex+Sans:wght@400;600;700'
            '&family=IBM+Plex+Sans+Condensed:wght@700&display=swap" rel="stylesheet">')
FONTS_AR = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500&family=IBM+Plex+Sans+Arabic:wght@400;600;700'
            '&family=IBM+Plex+Sans:wght@400;600&display=swap" rel="stylesheet">')


def page(path, title, desc, body, extra_ld=None, crumbs=None, noindex=False):
    global CURPATH
    CURPATH = path
    url = BASE + P(path)
    fam = "t-pest" if path.startswith("/pest-control") else "t-iso" if path.startswith("/iso-consultancy") else "t-home"
    ldo = [business_ld()] if path == "/" else []
    if crumbs:
        ldo.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + P(u)} for i, (n, u) in enumerate(crumbs)]})
    ldo += extra_ld or []
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    alts = ""
    if not noindex:
        alts = (f'<link rel="alternate" hreflang="en" href="{BASE}{path}"><link rel="alternate" hreflang="ar" href="{BASE}{"/ar" + path if path != "/" else "/ar/"}">'
                f'<link rel="alternate" hreflang="x-default" href="{BASE}{path}">')
    htmlattr = 'lang="ar" dir="rtl"' if LANG == "ar" else 'lang="en"'
    locale = "ar_SA" if LANG == "ar" else "en_US"
    doc = f"""<!doctype html>
<html {htmlattr}><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#ffffff">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">{alts}<link rel="icon" type="image/png" href="/assets/favicon.png"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">{robots}
<meta property="og:type" content="website"><meta property="og:locale" content="{locale}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/assets/og.png"><meta property="og:site_name" content="{E(brand())}"><meta name="twitter:card" content="summary_large_image">
<script>document.documentElement.className="js"</script>
{FONTS_AR if LANG == "ar" else FONTS_EN}
<link rel="stylesheet" href="/assets/style.css">
{''.join(ld(o) for o in ldo)}
{gtm_head()}</head><body class="{fam}">{gtm_body()}
{loc(header())}
<main>{loc(body)}</main>
{loc(footer())}
<script src="/assets/site.js" defer></script></body></html>"""
    write(P(path), doc)
    if not noindex and LANG == "en":
        PAGES.append(path)


def crumbs_html(items):
    return '<nav class="crumbs" aria-label="Breadcrumb">' + " <span>/</span> ".join(
        f'<a href="{u}">{E(n)}</a>' if i < len(items) - 1 else f"<b>{E(n)}</b>" for i, (n, u) in enumerate(items)) + "</nav>"


def HOME():
    return T("Home", "الرئيسية")


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
        head = f'<p class="kicker">{E(kicker)}</p><h2 class="s fold-h">{E(title)}</h2>'
        if kind == "table":
            intro, headers, rows, note = b[4], b[5], b[6], b[7]
            th = "".join(f"<th>{E(h)}</th>" for h in headers)
            tr = "".join("<tr>" + "".join(
                (f'<th scope="row" data-l="{E(headers[j])}">{E(c)}</th>' if j == 0 else f'<td data-l="{E(headers[j])}">{E(c)}</td>')
                for j, c in enumerate(r)) + "</tr>" for r in rows)
            body = (f'<p class="sub">{E(fmt(intro))}</p>' if intro else "") + f'<div class="tbl"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
            if note:
                body += f'<p class="note">{E(note)}</p>'
            out += f'<section{alt} id="{bid}" data-fold><div class="wrap">{head}<div class="fold-b">{body}</div></div></section>'
        elif kind == "list":
            intro, items = b[4], b[5]
            li = "".join(f"<li>{E(x)}</li>" for x in items)
            out += f'<section{alt} id="{bid}" data-fold><div class="wrap narrow">{head}<div class="fold-b"><p class="sub">{E(fmt(intro))}</p><ul class="ticks one">{li}</ul></div></div></section>'
        elif kind == "cards":
            intro, items = b[4], b[5]
            cards = "".join(f'<div class="card plain"><h3>{E(h)}</h3><p>{E(t)}</p></div>' for h, t in items)
            out += f'<section{alt} id="{bid}" data-fold><div class="wrap">{head}<div class="fold-b">' + (f'<p class="sub">{E(intro)}</p>' if intro else "") + f'<div class="cards wide">{cards}</div></div></div></section>'
        elif kind == "prose":
            ps = "".join(f"<p>{E(x)}</p>" for x in b[4])
            out += f'<section{alt} id="{bid}" data-fold><div class="wrap narrow prose">{head}<div class="fold-b">{ps}</div></div></section>'
    return out, toc


def wyg(st):
    return (f'<div class="wyg"><div><h4>{T("What we do", "ما نقوم به")}</h4><p>' + E(st["we"]) + f'</p></div><div><h4>{T("What you do", "ما عليك القيام به")}</h4><p>' + E(st["you"]) +
            f'</p></div><div class="gets"><h4>{T("What you get", "ما تحصل عليه")}</h4><p>' + E(st["get"]) + '</p></div></div>')


def process_widget(family):
    steps = PROCESS[family]
    btns = "".join(
        f'<button type="button" class="pstep{" active" if i == 0 else ""}" role="tab" id="t-{family}-{i}" aria-controls="p-{family}-{i}" aria-selected="{"true" if i == 0 else "false"}" data-i="{i}">'
        f'<span class="pn">{i+1:02d}</span><span class="pt"><b>{E(st["title"])}</b><small>{E(st["short"])}</small></span><span class="pbar"></span></button>'
        for i, st in enumerate(steps))
    panels = "".join(
        f'<div class="ppanel{" active" if i == 0 else ""}" role="tabpanel" id="p-{family}-{i}" aria-labelledby="t-{family}-{i}">'
        f'<div class="pscene">{scene(st["icon"], LANG)}<span class="pcount">{T(f"Step {i+1} of {len(steps)}", f"الخطوة {i+1} من {len(steps)}")}</span></div>'
        f'<div class="pbody"><span class="chip">{E(st["time"])}</span><h3>{E(st["title"])}</h3>{wyg(st)}</div></div>'
        for i, st in enumerate(steps))
    heading = (T("How a pest control job works, step by step", "كيف تتم أعمال مكافحة الحشرات خطوة بخطوة") if family == "pest"
               else T("How an ISO project works, step by step", "كيف يسير مشروع الأيزو خطوة بخطوة"))
    link = (T("See the full process, with a sample service report", "اطّلع على العملية كاملة، مع نموذج لتقرير الخدمة") if family == "pest"
            else T("See the full process, with a sample project plan", "اطّلع على العملية كاملة، مع نموذج لخطة المشروع"))
    sub = T("Pick a step to see what we do, what we need from you, and what you receive. Durations are typical and are confirmed in your quotation.",
            "اختر خطوة لترى ما نقوم به وما نحتاجه منك وما ستتسلّمه. المدد تقريبية ويؤكدها عرض السعر.")
    return (f'<section class="alt" id="process"><div class="wrap"><p class="kicker">{T("Process", "آلية العمل")}</p><h2 class="s">{heading}</h2>'
            f'<p class="sub">{sub}</p>'
            f'<div class="pw"><div class="plist" role="tablist" aria-label="{T("Process steps", "خطوات العمل")}">{btns}</div><div class="ppanels">{panels}</div></div>'
            f'<p class="more-link"><a href="/{"pest-control" if family == "pest" else "iso-consultancy"}/how-it-works/">{link} &{"l" if LANG == "ar" else "r"}arr;</a></p></div></section>')


def lane(family):
    steps = PROCESS[family]
    name, path = ((T("Pest control", "مكافحة الحشرات"), "/pest-control/how-it-works/") if family == "pest" else (T("ISO consultancy", "استشارات الأيزو"), "/iso-consultancy/how-it-works/"))
    li = "".join(f'<li style="--d:{i*90}ms"><span class="ln-n">{i+1}</span><b>{E(st["title"])}</b></li>' for i, st in enumerate(steps))
    return f'<div class="lane t-{family}"><h3>{name}</h3><ol class="lane-steps">{li}</ol><a class="more" href="{path}">{T("See how it works", "اطّلع على آلية العمل")}</a></div>'


def sample_report():
    rows = "".join(f"<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>" for k, v in SAMPLE_REPORT)
    return (f'<div class="paper"><span class="stamp-s">{T("Sample", "نموذج")}</span><p class="kicker">{T("Service report", "تقرير الخدمة")}</p><h3>{T("What you receive after every visit", "ما تتسلّمه بعد كل زيارة")}</h3>'
            f'<dl>{rows}</dl><p class="small">{T("This is an illustration. Your report is filled in with the real details of your visit.", "هذا نموذج توضيحي. يُعبّأ تقريرك بالتفاصيل الفعلية لزيارتك.")}</p></div>')


def sample_gantt():
    wk = 24
    rows = ""
    side = "right" if LANG == "ar" else "left"
    for i, (label, a, b, who) in enumerate(SAMPLE_GANTT):
        pos, width = (a - 1) / wk * 100, (b - a + 1) / wk * 100
        rows += (f'<div class="g-row"><span class="g-l">{E(label)}</span><span class="g-t"><i class="g-b {who}" style="{side}:{pos:.2f}%;width:{width:.2f}%;--d:{i*140}ms"></i></span></div>')
    scale = "".join(f"<span>{w}</span>" for w in (1, 4, 8, 12, 16, 20, 24))
    return (f'<div class="gantt"><p class="kicker">{T("Illustrative plan", "خطة توضيحية")}</p><h3>{T("A typical five-month ISO project", "مشروع أيزو نموذجي مدته خمسة أشهر")}</h3>'
            f'<div class="g-scale"><span class="g-l">{T("Week", "الأسبوع")}</span><span class="g-t g-ticks">{scale}</span></div>{rows}'
            f'<div class="g-key"><span><i class="g-b us"></i>{T("Our work with your team", "عملنا مع فريقك")}</span><span><i class="g-b you"></i>{T("Your management", "إدارتكم")}</span>'
            f'<span><i class="g-b cb"></i>{T("Certification body (its own schedule)", "جهة منح الشهادات (وفق جدولها الخاص)")}</span></div>'
            f'<p class="small">{T("Your plan is dated after the gap analysis. The certification body sets the dates of its own audits.", "تُحدَّد تواريخ خطتك بعد تحليل الفجوات. وتحدد جهة منح الشهادات مواعيد تدقيقاتها بنفسها.")}</p></div>')


def process_page(family):
    steps = PROCESS[family]
    hub = "pest-control" if family == "pest" else "iso-consultancy"
    path = f"/{hub}/how-it-works/"
    nm = T("Pest control", "مكافحة الحشرات") if family == "pest" else T("ISO consultancy", "استشارات الأيزو")
    if family == "pest":
        h1 = T("How our pest control works", "كيف تتم أعمال المكافحة لدينا")
        lead = T("From the first call to the follow-up visit: what happens, who does what, and what you get at each step.",
                 "من الاتصال الأول حتى زيارة المتابعة: ماذا يحدث، ومن يقوم بماذا، وما الذي تحصل عليه في كل خطوة.")
        title = T("How Pest Control Works | Step by Step Process | Omnexa Solutions", "كيف تتم مكافحة الحشرات؟ خطوات العمل بالتفصيل | " + brand())
        desc = T("How our pest control works in Riyadh and Jeddah: inspection, written plan, treatment, service report and follow-up.",
                 "كيف تتم أعمال مكافحة الحشرات لدينا في الرياض وجدة: الفحص، والخطة المكتوبة، والمعالجة، وتقرير الخدمة، والمتابعة.")
    else:
        h1 = T("How ISO certification works with us", "كيف تتم رحلة الحصول على شهادة الأيزو معنا")
        lead = T("From the first meeting to the certificate and beyond: what happens, who does what, and who decides at each step.",
                 "من الاجتماع الأول إلى الشهادة وما بعدها: ماذا يحدث، ومن يقوم بماذا، ومن يتخذ القرار في كل خطوة.")
        title = T("How ISO Certification Works | Step by Step Process | Omnexa Solutions", "كيف تتم شهادة الأيزو؟ خطوات العمل بالتفصيل | " + brand())
        desc = T("How ISO certification works: gap analysis, documentation, training, internal audit, certification audit and renewal.",
                 "كيف تتم شهادة الأيزو: تحليل الفجوات، والتوثيق، والتدريب، والتدقيق الداخلي، وتدقيق منح الشهادة، والتجديد.")
    cr = [(HOME(), "/"), (nm, f"/{hub}/"), (T("How it works", "آلية العمل"), path)]
    tl = "".join(
        f'<article class="tl" id="step-{st["id"]}"><span class="tl-m">{i+1}</span><div class="tl-in"><div class="tl-sc">{scene(st["icon"], LANG)}</div>'
        f'<div><span class="chip">{E(st["time"])}</span><h2>{E(st["title"])}</h2>{wyg(st)}</div></div></article>' for i, st in enumerate(steps))
    extra = sample_report() if family == "pest" else sample_gantt()
    nav = "".join(f'<a href="#step-{st["id"]}">{i+1}. {E(st["title"])}</a>' for i, st in enumerate(steps))
    cta = T("Book a free inspection", "احجز فحصاً مجانياً") if family == "pest" else T("Book a free consultation", "احجز استشارة مجانية")
    cl = wa_link(T("Hello, I would like to book " + ("an inspection" if family == "pest" else "an ISO consultation"), "السلام عليكم، أرغب في حجز " + ("فحص" if family == "pest" else "استشارة أيزو")))
    body = (f'<div class="hero slim t-{family}"><div class="wrap">{crumbs_html(cr)}<h1>{E(h1)}</h1><p class="lead">{E(lead)}</p>'
            f'<div class="cta">{btn_wa(cl)}{btn_call()}</div></div></div>'
            f'<nav class="onpage" aria-label="{T("Steps", "الخطوات")}"><div class="wrap"><b>{T("Steps", "الخطوات")}</b>{nav}</div></nav>'
            f'<section><div class="wrap"><div class="tlwrap"><div class="tlrail" aria-hidden="true"><i></i></div>{tl}</div></div></section>'
            f'<section class="alt"><div class="wrap narrow">{extra}</div></section>'
            f'<div class="cta-band"><div class="wrap"><h2>{cta}</h2><p>{T("Tell us about your site and we will contact you.", "أخبرنا عن موقعك وسنتواصل معك.")}</p><div class="cta">{btn_wa(cl)}{btn_call(T("Call now", "اتصل الآن"))}</div></div></div>')
    page(path, title, desc, body, crumbs=cr)


def process_hub():
    cr = [(HOME(), "/"), (T("How it works", "آلية العمل"), "/how-it-works/")]
    cols = ""
    for fam, nm, path, desc in (("pest", T("Pest control", "مكافحة الحشرات"), "/pest-control/how-it-works/",
                                 T("Inspection first, a written plan, treatment, a report after every visit, and follow-up.", "الفحص أولاً، ثم خطة مكتوبة، ثم المعالجة، وتقرير بعد كل زيارة، ثم المتابعة.")),
                                ("iso", T("ISO consultancy", "استشارات الأيزو"), "/iso-consultancy/how-it-works/",
                                 T("Gap analysis, documentation, training, internal audit, then the certification audit by an accredited body.", "تحليل الفجوات، والتوثيق، والتدريب، والتدقيق الداخلي، ثم تدقيق منح الشهادة من جهة معتمدة."))):
        n = len(PROCESS[fam])
        cols += f'<a class="door t-{fam}" href="{path}"><div class="door-txt"><p class="kicker">{nm}</p><h2>{T(f"{n} steps from first contact to result", f"{n} خطوات من أول تواصل حتى النتيجة")}</h2><p>{desc}</p><span class="more">{T("See the full process", "اطّلع على العملية كاملة")}</span></div></a>'
    body = (f'<div class="hero slim"><div class="wrap">{crumbs_html(cr)}<h1>{T("How we work", "كيف نعمل")}</h1><p class="lead">{T("Pest control and ISO consultancy each follow a clear process, with written records at every stage.", "تتبع مكافحة الحشرات واستشارات الأيزو كلٌّ منهما عملية واضحة، مع سجلات مكتوبة في كل مرحلة.")}</p></div></div>'
            f'<section><div class="wrap doors flat">{cols}</div></section>')
    page("/how-it-works/", T("How We Work | Pest Control and ISO Process | Omnexa Solutions", "كيف نعمل | خطوات مكافحة الحشرات واستشارات الأيزو | " + brand()),
         T("How our pest control and ISO consultancy processes work, step by step.", "كيف تتم أعمال مكافحة الحشرات واستشارات الأيزو لدينا، خطوة بخطوة."), body, crumbs=cr)


def service_page(path, d, parent, family, slug=None):
    h1, title, desc = fmt(d["h1"]), fmt(d["title"]), fmt(d["desc"])
    data = PEST if family == "pest" else ISO
    hub = data["hub"]
    hub_path = "/" + hub["slug"] + "/"
    cr = [(HOME(), "/")]
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
        links = "".join(f'<a href="#{i}">{E(t)}</a>' for i, t in toc) + f'<a href="#process">{T("How it works", "آلية العمل")}</a><a href="#faq">{T("FAQ", "الأسئلة الشائعة")}</a>'
        onpage = f'<nav class="onpage" aria-label="{T("On this page", "في هذه الصفحة")}"><div class="wrap"><b>{T("On this page", "في هذه الصفحة")}</b>{links}</div></nav>'
    noun = T("inspection", "فحص") if family == "pest" else T("consultation", "استشارة")
    quote = d.get("cta") == "quote"
    if slug is None:  # hub
        cards = "".join(f'<a class="card" href="{hub_path}{c}/">{card_icon(family, c)}<h3>{E(fmt(data[c]["h1"]))}</h3><p>{E(fmt(data[c]["lead"]))}</p><span class="more">{T("Learn more", "اعرف المزيد")}</span></a>'
                        for c in hub["children"])
        ktitle = T("Pest control services", "خدمات مكافحة الحشرات") if family == "pest" else T("ISO standards we support", "معايير الأيزو التي ندعمها")
        areas = "".join(f'<a href="{hub_path}{x.lower()}/">{E(CITY_PAGES[(family, x.lower())]["h1"])}</a>' for x in CITIES)
        related = f'<section class="alt"><div class="wrap"><p class="kicker">{T("Services", "الخدمات")}</p><h2 class="s">{ktitle}</h2><div class="cards">{cards}</div><p class="kicker" style="margin-top:36px">{T("Areas we serve", "المناطق التي نخدمها")}</p><div class="chips">{areas}</div></div></section>'
        eyebrow = (T("Pest control", "مكافحة الحشرات") if family == "pest" else T("ISO consultancy", "استشارات الأيزو")) + " · " + (city_all() if family == "pest" else T("Saudi Arabia", "المملكة العربية السعودية"))
        label = None
    else:
        sib = "".join(f'<a href="{hub_path}{c}/">{E(fmt(data[c]["service"]))}</a>' for c in hub["children"] if c != slug)
        allw = T(f"All {parent[0].lower()} services", f"جميع خدمات {parent[0]}")
        related = f'<section class="alt tight"><div class="wrap"><p class="kicker">{T("Related services", "خدمات ذات صلة")}</p><div class="chips">{sib}<a class="all" href="{hub_path}">{allw}</a></div></div></section>'
        eyebrow = parent[0] + (" · " + cname(d["city"]) if d.get("city") else "")
        label = d["service"].upper() if LANG == "en" else d["service"]
    notice = ""
    if family == "iso" and not d.get("no_notice"):
        notice = f'<div class="notice">{T("We are ISO consultants. Certificates are issued by an accredited certification body of your choice; we prepare you for its audit.", "نحن مستشارون في الأيزو. تُصدر الشهادة جهة منح شهادات معتمدة من اختيارك، ونحن نجهّزك لتدقيقها.")}</div>'
    art = illus_ipm() if slug == "commercial-ipm" else (illus_pest() if family == "pest" else illus_iso(label))
    if d.get("art") == "train":
        art = scene("train", LANG)
    if slug is None or d.get("city"):
        proc = process_widget(family)
    else:
        arrow = "&larr;" if LANG == "ar" else "&rarr;"
        plink = f'<p class="more-link"><a href="/{hub["slug"]}/how-it-works/">{T("See the full process", "اطّلع على العملية كاملة")} {arrow}</a></p>' if d.get("plink", True) else ""
        proc = (f'<section class="alt" id="process"><div class="wrap"><p class="kicker">{T("Process", "آلية العمل")}</p><h2 class="s">{T("How it works", "كيف نعمل")}</h2><ol class="steps">{steps}</ol>{plink}</div></section>')
    if quote:
        cta = wa_link(T("Hello, I would like a quote for " + d["service"], "السلام عليكم، أرغب في الحصول على عرض سعر لـ " + d["service"]))
    else:
        cta = wa_link(T("Hello, I need " + d["service"], "السلام عليكم، أحتاج إلى خدمة: " + d["service"]))
    office_note = (f'<p class="office-note">{T("Our " + d["city"] + " office: ", "مكتبنا في " + cname(d["city"]) + ": ")}{E(office_for(d["city"]))}</p>' if d.get("city") and office_for(d.get("city")) else "")
    gallery = field_strip() if (family == "pest" and (slug is None or d.get("city"))) else ""
    if slug == "commercial-ipm":
        gallery = f'<section><div class="wrap"><p class="kicker">{T("Where we work", "أين نعمل")}</p><h2 class="s">{T("Sites we protect", "مواقع نحميها")}</h2>{sector_grid()}</div></section>'
    if family == "iso" and slug is None and C.get("certification_partner"):
        gallery = (f'<section class="tight"><div class="wrap narrow"><div class="callout"><h3>{T("Our certification partner", "شريكنا في منح الشهادات")}</h3><p>'
                   + T(f'We work with {E(C["certification_partner"])} as a certification partner. You are free to choose any accredited certification body, and we prepare you for its audit whichever you choose. We do not take part in the audit or influence the certification decision.',
                       f'نعمل مع {E(C["certification_partner"])} كشريك في منح الشهادات. أنت حرّ في اختيار أي جهة منح شهادات معتمدة، ونجهّزك لتدقيقها أياً كانت. نحن لا نشارك في التدقيق ولا نؤثر في قرار منح الشهادة.')
                   + '</p></div></div></section>')
    body = f"""<div class="hero"><div class="wrap">{crumbs_html(cr)}<div class="grid"><div>
<p class="eyebrow">{E(eyebrow)}</p><h1>{E(h1)}</h1><p class="lead">{E(fmt(d['lead']))}</p>
<div class="cta">{btn_wa(cta)}{btn_call()}</div>{trust(family, d.get("trust"))}{office_note}</div>
<div class="card formcard"><h2>{T("Request a quote", "اطلب عرض سعر") if quote else T("Request a free " + noun, "اطلب " + noun + " مجانية" if family != "pest" else "اطلب فحصاً مجانياً")}</h2>{form(d['service'], d.get('city'))}</div></div></div></div>
{onpage}
<section><div class="wrap two"><div><p class="kicker">{d.get("inc_kicker") or T("What's included", "ما تشمله الخدمة")}</p><h2 class="s">{d.get("inc_title") or (E(d['service']) + T(": what we do", ": ماذا نقدّم"))}</h2><p class="sub">{E(fmt(d['intro']))}</p><ul class="ticks">{ticks}</ul>{notice}</div>
<div class="art">{art}</div></div></section>
{extra}
{gallery}
{proc}
{related}
<section id="faq"><div class="wrap narrow"><p class="kicker">{T("FAQ", "الأسئلة الشائعة")}</p><h2 class="s">{T("Frequently asked questions", "الأسئلة الأكثر شيوعاً")}</h2>{faq}</div></section>
<div class="cta-band"><div class="wrap"><h2>{T("Request a quote for your team", "اطلب عرض سعر لفريقك") if quote else T("Book your free " + noun, "احجز فحصك المجاني" if family == "pest" else "احجز استشارتك المجانية")}</h2><p>{T("Tell us the course, the number of people and your preferred dates. We will send you a written quote.", "أخبرنا بالدورة وعدد المشاركين والمواعيد المفضلة وسنرسل لك عرض سعر مكتوباً.") if quote else T("Tell us about your site and we will contact you.", "أخبرنا عن موقعك وسنتواصل معك.")}</p>
<div class="cta">{btn_wa(cta)}{btn_call(T("Call now", "اتصل الآن"))}</div></div></div>"""
    svc = {"@context": "https://schema.org", "@type": "Service", "name": h1, "serviceType": d["service"],
           "provider": {"@type": "LocalBusiness", "@id": BASE + "/#business", "name": brand(), "telephone": C["phone"]},
           "areaServed": {"@type": "Country", "name": T(C["country"], "المملكة العربية السعودية")}, "url": BASE + P(path), "description": desc, "inLanguage": LANG}
    crs = ({"@context": "https://schema.org", "@type": "Course", "name": h1, "description": desc, "inLanguage": LANG,
            "provider": {"@type": "Organization", "name": brand(), "url": BASE + P("/")}} if quote else None)
    fq = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": LANG, "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    page(path, title, desc, body, [svc, fq] + ([crs] if crs else []), cr)


def build_site():
    names = (T("Pest Control", "مكافحة الحشرات"), T("ISO Consultancy", "استشارات الأيزو"))
    for (fam, data), name in zip((("pest", PEST), ("iso", ISO)), names):
        hub = data["hub"]
        hp = "/" + hub["slug"] + "/"
        service_page(hp, hub, None, fam)
        for k in hub["children"]:
            service_page(hp + k + "/", data[k], (name, hp), fam, slug=k)
        for x in CITIES:
            d = dict(CITY_PAGES[(fam, x.lower())], steps=PEST_STEPS if fam == "pest" else ISO_STEPS)
            service_page(hp + x.lower() + "/", d, (name, hp), fam, slug=x.lower())

    # home
    more = T("Learn more", "اعرف المزيد")
    pest_cards = "".join(f'<a class="card" href="/pest-control/{s}/">{card_icon("pest", s)}<h3>{E(fmt(PEST[s]["service"]))}</h3><span class="more">{more}</span></a>' for s in PEST["hub"]["children"])
    iso_cards = "".join(f'<a class="card" href="/iso-consultancy/{s}/">{card_icon("iso", s)}<h3>{E(ISO[s]["service"])}</h3><span class="more">{more}</span></a>' for s in ISO["hub"]["children"])
    home = f"""<div class="hero home"><div class="wrap"><p class="eyebrow">{E(" · ".join(cname(x) for x in CITIES))}</p>
<h1>{T("Pest Control and ISO Consultancy in Saudi Arabia", "مكافحة الحشرات واستشارات الأيزو في المملكة العربية السعودية")}</h1>
<p class="lead">{T("Inspection-led pest control and practical ISO consultancy for homes and businesses in Riyadh and Jeddah.", "مكافحة حشرات تبدأ بالفحص، واستشارات أيزو عملية، للمنازل والشركات في الرياض وجدة.")}</p>
<div class="cta">{btn_wa(wa_link(T('Hello, I would like to enquire', 'السلام عليكم، أودّ الاستفسار')))}{btn_call()}</div>{trust('home')}</div></div>
<div class="wrap doors">
<a class="door t-pest" href="/pest-control/"><div class="art">{illus_pest()}</div><div class="door-txt"><p class="kicker">{T("For homes and facilities", "للمنازل والمنشآت")}</p><h2>{T("Pest Control in " + city_all(), "مكافحة الحشرات في " + city_all())}</h2><p>{T("Termites, rodents, cockroaches, bed bugs, fumigation and scheduled IPM programmes.", "النمل الأبيض والقوارض والصراصير وبق الفراش والتبخير وبرامج المكافحة المتكاملة المجدولة.")}</p><span class="more">{T("Book a free inspection", "احجز فحصاً مجانياً")}</span></div></a>
<a class="door t-iso" href="/iso-consultancy/"><div class="art">{illus_iso(T('ISO 9001 · 22000 · 45001', 'ISO 9001 · 22000 · 45001'))}</div><div class="door-txt"><p class="kicker">{T("For companies seeking certification", "للشركات الراغبة في الحصول على شهادة")}</p><h2>{T("ISO Consultancy", "استشارات الأيزو")}</h2><p>{T("Gap analysis, documentation, internal audit and certification preparation.", "تحليل الفجوات والتوثيق والتدقيق الداخلي والتحضير للحصول على الشهادة.")}</p><span class="more">{T("Book a free consultation", "احجز استشارة مجانية")}</span></div></a>
</div>
<section class="t-pest"><div class="wrap"><p class="kicker">{T("Pest control", "مكافحة الحشرات")}</p><h2 class="s">{T("Pest control services", "خدمات مكافحة الحشرات")}</h2><div class="cards">{pest_cards}</div></div></section>
<section class="alt t-iso"><div class="wrap"><p class="kicker">{T("ISO consultancy", "استشارات الأيزو")}</p><h2 class="s">{T("ISO standards we support", "معايير الأيزو التي ندعمها")}</h2><div class="cards">{iso_cards}</div></div></section>
<section id="how"><div class="wrap"><p class="kicker">{T("How we work", "كيف نعمل")}</p><h2 class="s">{T("Clear steps, written records", "خطوات واضحة وسجلات مكتوبة")}</h2><p class="sub">{T("Each service has its own clear path. Pest control starts with an inspection; ISO consultancy starts with a gap analysis. Both end with written records you can show an auditor or a client.", "لكل خدمة مسارها الواضح. تبدأ مكافحة الحشرات بالفحص، وتبدأ استشارات الأيزو بتحليل الفجوات. وتنتهي كلتاهما بسجلات مكتوبة يمكنك عرضها على مدقق أو عميل.")}</p><div class="lanes">{lane("pest")}{lane("iso")}</div></div></section>
{field_strip()}
<section class="alt"><div class="wrap"><p class="kicker">{T("Who we work with", "عملاؤنا")}</p><h2 class="s">{T("Different customers, different needs", "عملاء مختلفون واحتياجات مختلفة")}</h2>
<div class="cards wide"><div class="card plain t-pest"><h3>{T("Pest control customers", "عملاء مكافحة الحشرات")}</h3><p>{T("Homeowners and villa residents, restaurants and cafes, hotels and serviced apartments, hospitals and clinics, warehouses and food facilities.", "ملاك المنازل وسكان الفلل، والمطاعم والمقاهي، والفنادق والشقق المخدومة، والمستشفيات والعيادات، والمستودعات والمنشآت الغذائية.")}</p><a class="more" href="/pest-control/">{T("See pest control", "تعرّف على مكافحة الحشرات")}</a></div>
<div class="card plain t-iso"><h3>{T("ISO consultancy clients", "عملاء استشارات الأيزو")}</h3><p>{T("Contractors, food manufacturers, factories, logistics companies and IT firms that need a certificate for a tender, a customer or their own growth.", "المقاولون ومصنّعو الأغذية والمصانع وشركات اللوجستيات وشركات تقنية المعلومات التي تحتاج إلى شهادة لمناقصة أو لعميل أو لنمو أعمالها.")}</p><a class="more" href="/iso-consultancy/">{T("See ISO consultancy", "تعرّف على استشارات الأيزو")}</a></div></div></div></section>
<div class="cta-band"><div class="wrap"><h2>{T("Tell us what you need", "أخبرنا بما تحتاجه")}</h2><p>{T("We respond with next steps.", "نردّ عليك بالخطوات التالية.")}</p><div class="cta">{btn_wa(WA)}{btn_call(T("Call now", "اتصل الآن"))}</div></div></div>"""
    page("/", T("Pest Control & ISO Consultancy in Saudi Arabia | Omnexa Solutions", "مكافحة الحشرات واستشارات الأيزو في السعودية | " + brand()),
         T("Pest control and ISO consultancy in Saudi Arabia. Free site inspection and free ISO consultation. Termites, rodents, ISO 9001, 22000, 45001.",
           "مكافحة حشرات واستشارات أيزو في الرياض وجدة. فحص مجاني للموقع واستشارة أيزو مجانية. النمل الأبيض والقوارض وISO 9001 و22000 و45001."), home)

    process_page("pest")
    process_page("iso")
    process_hub()

    # other services
    cr = [(HOME(), "/"), (T("Other services", "خدمات أخرى"), "/facility-services/")]
    cards = "".join(f'<div class="card plain"><h3>{E(a)}</h3><p>{E(b)}</p><ul class="mini">' + "".join(f"<li>{E(x)}</li>" for x in c) + "</ul>" + (img("field-aircon", "inl") if i == 0 else "") + "</div>" for i, (a, b, c) in enumerate(OTHER))
    body = f"""{simple_hero(cr, T('Facility and Technical Services', 'الخدمات الفنية وخدمات المرافق'), T('We also provide these services. Contact us for a quotation.', 'نقدم أيضاً هذه الخدمات. تواصل معنا للحصول على عرض سعر.'))}
<section><div class="wrap"><div class="cards wide">{cards}</div><div class="cta" style="margin-top:28px">{btn_wa(WA)}{btn_call()}</div></div></section>"""
    page("/facility-services/", T("Facility & Technical Services | Omnexa Solutions", "الخدمات الفنية وخدمات المرافق | " + brand()),
         T("HVAC, construction, safety signage and equipment, and IT services from Omnexa Solutions in Saudi Arabia.", "التكييف والإنشاءات ولوحات ومعدات السلامة وخدمات تقنية المعلومات من أومنكسا سوليوشنز في المملكة العربية السعودية."), body, crumbs=cr)

    # about
    cr = [(HOME(), "/"), (T("About", "من نحن"), "/about/")]
    vals = "".join(f'<div class="card plain"><h3>{E(t)}</h3><p>{E(d)}</p></div>' for t, d in VALUES)
    body = f"""{simple_hero(cr, T('About ' + brand(), 'عن ' + brand()), T('Pest management, ISO consultancy and training, and facility services for businesses in Saudi Arabia.', 'إدارة الآفات واستشارات الأيزو والتدريب وخدمات المرافق للشركات في المملكة العربية السعودية.'))}
<section><div class="wrap two"><div><p class="kicker">{T("Who we are", "من نحن")}</p><h2 class="s">{T("What we do", "ماذا نقدّم")}</h2>
<p class="sub"><b>{T("Pest management.", "إدارة الآفات.")}</b> {T("Integrated Pest Management, with pesticide and non-pesticide methods, for homes, food sites, hotels, hospitals and warehouses.", "الإدارة المتكاملة للآفات بالطرق الكيميائية وغير الكيميائية، للمنازل والمنشآت الغذائية والفنادق والمستشفيات والمستودعات.")}</p><p class="sub"><b>{T("ISO consultancy and training.", "استشارات الأيزو والتدريب.")}</b> {T("Gap analysis, documentation, internal audit and training for ISO standards and food-safety schemes.", "تحليل الفجوات والتوثيق والتدقيق الداخلي والتدريب على معايير الأيزو وأنظمة سلامة الغذاء.")}</p><p class="sub"><b>{T("Facility services.", "خدمات المرافق.")}</b> {T("Air-conditioning, construction, safety signage and equipment, and IT.", "التكييف والإنشاءات ولوحات ومعدات السلامة وتقنية المعلومات.")}</p><p class="sub">{T("Our offices are in Riyadh (Al Olaya) and Jeddah (Al Handawiya).", "يقع مكتبانا في الرياض (العليا) وجدة (الهنداوية).")}</p>
</div>
<div class="art"><img class="about-logo" src="/assets/logo.png" width="360" height="94" alt="{E(brand())}" loading="lazy"></div></div></section>
<section class="alt"><div class="wrap"><div class="cards wide"><div class="card plain"><h3>{T("Our mission", "رسالتنا")}</h3><p>{T("To give clients dependable service, and to make sure our staff, products and equipment meet the standards our clients set.", "تقديم خدمة يعتمد عليها عملاؤنا، والتأكد من أن موظفينا ومنتجاتنا ومعداتنا تلبي المعايير التي يضعها عملاؤنا.")}</p></div>
<div class="card plain"><h3>{T("Our vision", "رؤيتنا")}</h3><p>{T("To be the pest management and facility services provider that clients choose for reliability and value.", "أن نكون مزوّد إدارة الآفات وخدمات المرافق الذي يختاره العملاء لموثوقيته وقيمته.")}</p></div></div></div></section>
<section><div class="wrap"><p class="kicker">{T("What we stand for", "ما نؤمن به")}</p><h2 class="s">{T("Our values", "قيمنا")}</h2><div class="cards wide">{vals}</div></div></section>
<section><div class="wrap narrow">{company_box()}</div></section>
<section class="alt"><div class="wrap"><p class="kicker">{T("Where we work", "أين نعمل")}</p><h2 class="s">{T("Sectors we serve", "القطاعات التي نخدمها")}</h2><p class="sub">{T("Our pest control and consultancy cover public health and food safety across these kinds of sites.", "تغطي أعمال المكافحة والاستشارات لدينا الصحة العامة وسلامة الغذاء في هذه الأنواع من المواقع.")}</p>{sector_grid()}</div></section>
<div class="cta-band"><div class="wrap"><h2>{T("Talk to us", "تحدّث إلينا")}</h2><p>{T("Free site inspection and free ISO consultation.", "فحص مجاني للموقع واستشارة أيزو مجانية.")}</p><div class="cta">{btn_wa(WA)}{btn_call(T("Call now", "اتصل الآن"))}</div></div></div>"""
    page("/about/", T("About Omnexa Solutions", "عن " + brand()), T("About Omnexa Solutions: pest management, ISO consultancy and training, and facility services in Saudi Arabia.", "عن أومنكسا سوليوشنز: إدارة الآفات واستشارات الأيزو والتدريب وخدمات المرافق في المملكة العربية السعودية."), body, crumbs=cr)

    # contact
    cr = [(HOME(), "/"), (T("Contact", "اتصل بنا"), "/contact/")]
    offs = "".join(f'<p><b>{E(office_label(o))}</b>{E(office_addr(o))}</p>' for o in C.get("offices", []))
    body = f"""{simple_hero(cr, T('Contact us', 'اتصل بنا'), T('Phone and WhatsApp are the fastest ways to reach us.', 'الهاتف وواتساب هما أسرع وسيلة للوصول إلينا.'))}
<section><div class="wrap two"><div class="contact"><p><b>{T("Phone", "الهاتف")}</b><a href="tel:{C['phone']}">{ltr(E(C['phone_display']))}</a></p><p><b>{T("WhatsApp", "واتساب")}</b><a href="{WA}">{T("Chat on WhatsApp", "تحدّث معنا عبر واتساب")}</a></p><p><b>{T("Email", "البريد الإلكتروني")}</b><a href="mailto:{C['email']}">{E(C['email'])}</a></p>{offs}<p><b>{T("Registered company", "الشركة المسجّلة")}</b>{legal_line()}</p></div>
<div class="card formcard"><h2>{T("Send an enquiry", "أرسل استفساراً")}</h2>{form(T('Other', 'أخرى'))}</div></div></section>"""
    page("/contact/", T("Contact Omnexa Solutions", "اتصل بنا | " + brand()), T("Contact Omnexa Solutions by phone, WhatsApp or email for pest control and ISO consultancy.", "تواصل مع أومنكسا سوليوشنز عبر الهاتف أو واتساب أو البريد الإلكتروني لخدمات مكافحة الحشرات واستشارات الأيزو."), body, crumbs=cr)

    # privacy
    fs = T(" and our form service", " وعبر خدمة النماذج لدينا") if C["form_endpoint"] else ""
    body = f"""{simple_hero([(HOME(),'/'),(T('Privacy','الخصوصية'),'/privacy/')], T('Privacy', 'الخصوصية'), T('How we handle enquiry details.', 'كيف نتعامل مع بيانات الاستفسار.'))}
<section><div class="wrap narrow"><p class="sub">{T("When you submit the enquiry form, your name, phone number and message are sent to us through WhatsApp" + fs + " so we can reply. We use analytics to measure site use. Contact " + E(C['email']) + " to ask us to delete your data.",
        "عند إرسال نموذج الاستفسار، يصلنا اسمك ورقم جوالك ورسالتك عبر واتساب" + fs + " لنتمكن من الرد عليك. نستخدم أدوات التحليلات لقياس استخدام الموقع. راسلنا على " + E(C['email']) + " لطلب حذف بياناتك.")}</p></div></section>"""
    page("/privacy/", T("Privacy | Omnexa Solutions", "الخصوصية | " + brand()), T("Privacy information for Omnexa Solutions.", "معلومات الخصوصية لدى أومنكسا سوليوشنز."), body)


def build_404():
    use("en")
    write("/404.html", f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | الصفحة غير موجودة</title><meta name="robots" content="noindex">{FONTS_AR}<link rel="stylesheet" href="/assets/style.css"></head><body class="t-home"><main><div class="hero slim"><div class="wrap"><h1>Page not found</h1><p class="lead"><a href="/">Back to home</a></p><h1 dir="rtl" lang="ar" style="margin-top:28px">الصفحة غير موجودة</h1><p class="lead" dir="rtl" lang="ar"><a href="/ar/">العودة إلى الصفحة الرئيسية</a></p></div></div></main></body></html>""")


def main():
    for lang in (("en",) if os.environ.get("ONLY_EN") else ("en", "ar")):
        use(lang)
        build_site()
    build_404()
    xl = lambda p: (f'<url><loc>{BASE}{p}</loc><xhtml:link rel="alternate" hreflang="en" href="{BASE}{p}"/><xhtml:link rel="alternate" hreflang="ar" href="{BASE}{"/ar" + p if p != "/" else "/ar/"}"/></url>'
                    f'<url><loc>{BASE}{"/ar" + p if p != "/" else "/ar/"}</loc><xhtml:link rel="alternate" hreflang="en" href="{BASE}{p}"/><xhtml:link rel="alternate" hreflang="ar" href="{BASE}{"/ar" + p if p != "/" else "/ar/"}"/></url>')
    urls = "".join(xl(p) for p in PAGES)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">{urls}</urlset>')
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    print(len(PAGES), "pages per language")


main()
