# -*- coding: utf-8 -*-
"""Generates the Google Ads keyword plan, ad copy and negative keywords as CSV files.
Run: python3 ads/build_ads.py   (writes into ./ads). Edit the data below, then re-run.
Keyword volumes are NOT included: validate every keyword in Google Keyword Planner before launch."""
import csv, os, sys

BASE = "https://omnexasol.com"
OUT = os.path.dirname(os.path.abspath(__file__))
CITY_AR = {"Riyadh": "الرياض", "Jeddah": "جدة"}


def url(path, ar):
    return BASE + ("/ar" + path if ar else path)


# ------------------------------------------------------------------ campaigns
# (campaign name, language, service)
CAMPAIGNS = {
    "01 Pest | Arabic": ("Arabic", "pest"), "02 Pest | English": ("English", "pest"),
    "03 ISO Consultancy | Arabic": ("Arabic", "iso"), "04 ISO Consultancy | English": ("English", "iso"),
    "05 ISO Training | Arabic": ("Arabic", "train"), "06 ISO Training | English": ("English", "train"),
}

# ------------------------------------------------------------------ keywords
# Each ad group: (name, landing path (None = per city), priority, [keywords]); {c} is replaced by the city name in that language
PEST_AR = [
    ("General | Riyadh", "/pest-control/riyadh/", 1, ["مكافحة حشرات الرياض", "شركة مكافحة حشرات الرياض", "شركات مكافحة الحشرات في الرياض", "مكافحة الحشرات المنزلية الرياض", "رش مبيدات الرياض", "شركة رش مبيدات بالرياض", "مكافحة الآفات الرياض"]),
    ("General | Jeddah", "/pest-control/jeddah/", 1, ["مكافحة حشرات جدة", "شركة مكافحة حشرات جدة", "شركات مكافحة الحشرات في جدة", "مكافحة الحشرات المنزلية جدة", "رش مبيدات جدة", "شركة رش مبيدات بجدة", "مكافحة الآفات جدة"]),
    ("Termite", "/pest-control/termite-control/", 1, ["مكافحة النمل الابيض", "شركة مكافحة النمل الابيض الرياض", "شركة مكافحة النمل الابيض جدة", "علاج النمل الابيض", "معالجة النمل الابيض", "مكافحة الارضة", "معالجة التربة ضد النمل الابيض", "مكافحة النمل الابيض قبل البناء"]),
    ("Rodents", "/pest-control/rodent-control/", 1, ["مكافحة الفئران", "مكافحة القوارض", "مكافحة الجرذان", "شركة مكافحة فئران الرياض", "شركة مكافحة فئران جدة", "التخلص من الفئران في المنزل"]),
    ("Cockroaches", "/pest-control/cockroach-control/", 1, ["مكافحة الصراصير", "شركة مكافحة صراصير الرياض", "شركة مكافحة صراصير جدة", "مكافحة الصراصير في المطابخ", "القضاء على الصراصير", "مكافحة النمل والصراصير"]),
    ("Bed bugs", "/pest-control/bed-bug-treatment/", 2, ["مكافحة بق الفراش", "علاج بق الفراش", "شركة مكافحة بق الفراش", "القضاء على بق الفراش", "بق الفراش في الفنادق"]),
    ("Fumigation", "/pest-control/fumigation/", 2, ["تبخير مستودعات", "شركة تبخير", "تبخير حاويات", "تبخير بضائع", "تبخير الحبوب والمخازن"]),
    ("Mosquito and dengue", "/pest-control/mosquito-control/", 2, ["مكافحة البعوض", "مكافحة حمى الضنك", "رش البعوض", "شركة مكافحة بعوض جدة", "مكافحة البعوض والذباب"]),
    ("Birds", "/pest-control/bird-control/", 3, ["مكافحة الحمام", "شباك حمام", "تركيب شباك للحمام", "مكافحة الطيور على المباني", "طرد الحمام"]),
    ("Snakes and wildlife", "/pest-control/wildlife-control/", 3, ["مكافحة الثعابين", "شركة مكافحة ثعابين", "إزالة الثعابين", "مكافحة السحالي", "مكافحة الحيوانات الضالة"]),
    ("Commercial", "/pest-control/commercial-ipm/", 1, ["مكافحة حشرات للمطاعم", "مكافحة الحشرات للمصانع", "مكافحة الآفات للمنشآت الغذائية", "عقد مكافحة حشرات سنوي", "مكافحة حشرات المستودعات", "مكافحة الآفات للفنادق"]),
]
PEST_EN = [
    ("General | Riyadh", "/pest-control/riyadh/", 1, ["pest control riyadh", "pest control company riyadh", "pest control in riyadh", "exterminator riyadh", "home pest control riyadh"]),
    ("General | Jeddah", "/pest-control/jeddah/", 1, ["pest control jeddah", "pest control company jeddah", "pest control in jeddah", "exterminator jeddah", "home pest control jeddah"]),
    ("Termite", "/pest-control/termite-control/", 1, ["termite control riyadh", "termite treatment riyadh", "termite control jeddah", "termite treatment jeddah", "anti termite treatment saudi arabia", "pre construction termite treatment"]),
    ("Rodents", "/pest-control/rodent-control/", 1, ["rodent control riyadh", "rat control riyadh", "rodent control jeddah", "rat control jeddah", "mice control saudi arabia"]),
    ("Cockroaches", "/pest-control/cockroach-control/", 1, ["cockroach control riyadh", "cockroach control jeddah", "cockroach treatment saudi arabia", "kitchen pest control riyadh"]),
    ("Bed bugs", "/pest-control/bed-bug-treatment/", 2, ["bed bug treatment riyadh", "bed bug treatment jeddah", "bed bug control saudi arabia", "bed bugs hotel treatment"]),
    ("Fumigation", "/pest-control/fumigation/", 2, ["warehouse fumigation riyadh", "warehouse fumigation jeddah", "container fumigation jeddah", "fumigation services saudi arabia", "stored product fumigation"]),
    ("Mosquito and dengue", "/pest-control/mosquito-control/", 2, ["mosquito control jeddah", "mosquito control riyadh", "dengue mosquito control saudi arabia", "mosquito fogging jeddah"]),
    ("Birds", "/pest-control/bird-control/", 3, ["bird control riyadh", "pigeon control riyadh", "bird netting riyadh", "pigeon control jeddah"]),
    ("Snakes and wildlife", "/pest-control/wildlife-control/", 3, ["snake removal riyadh", "snake removal jeddah", "snake control saudi arabia", "lizard control"]),
    ("Commercial", "/pest-control/commercial-ipm/", 1, ["commercial pest control riyadh", "restaurant pest control riyadh", "commercial pest control jeddah", "factory pest control saudi arabia", "pest control contract riyadh", "HACCP pest control"]),
]
ISO_AR = [
    ("General | Riyadh", "/iso-consultancy/riyadh/", 1, ["استشارات ايزو الرياض", "مكتب استشارات ايزو الرياض", "شركة استشارات ايزو الرياض", "الحصول على شهادة ايزو الرياض", "مستشار ايزو الرياض"]),
    ("General | Jeddah", "/iso-consultancy/jeddah/", 1, ["استشارات ايزو جدة", "مكتب استشارات ايزو جدة", "شركة استشارات ايزو جدة", "الحصول على شهادة ايزو جدة", "مستشار ايزو جدة"]),
    ("ISO 9001", "/iso-consultancy/iso-9001/", 1, ["ايزو 9001", "شهادة ايزو 9001", "تطبيق نظام ايزو 9001", "استشارات ايزو 9001", "ايزو 9001 الرياض", "ايزو 9001 جدة", "نظام ادارة الجودة"]),
    ("ISO 22000 and HACCP", "/iso-consultancy/iso-22000/", 1, ["ايزو 22000", "شهادة ايزو 22000", "شهادة هاسب", "تطبيق نظام هاسب", "ايزو 22000 سلامة الغذاء", "استشارات هاسب الرياض"]),
    ("ISO 45001", "/iso-consultancy/iso-45001/", 2, ["ايزو 45001", "شهادة ايزو 45001", "ايزو 45001 السلامة والصحة المهنية", "استشارات ايزو 45001"]),
    ("ISO 14001", "/iso-consultancy/iso-14001/", 2, ["ايزو 14001", "شهادة ايزو 14001", "نظام الادارة البيئية", "استشارات ايزو 14001"]),
    ("ISO 27001", "/iso-consultancy/iso-27001/", 2, ["ايزو 27001", "شهادة ايزو 27001", "امن المعلومات ايزو 27001", "استشارات ايزو 27001"]),
    ("Other standards", "/iso-consultancy/other-standards/", 3, ["ايزو 50001", "ايزو 22301", "ايزو 37001", "شهادة الحلال استشارات", "ايزو 13485"]),
]
ISO_EN = [
    ("General | Riyadh", "/iso-consultancy/riyadh/", 1, ["iso consultants riyadh", "iso consultancy riyadh", "iso certification consultant riyadh", "iso 9001 consultants riyadh"]),
    ("General | Jeddah", "/iso-consultancy/jeddah/", 1, ["iso consultants jeddah", "iso consultancy jeddah", "iso certification consultant jeddah", "iso 9001 consultants jeddah"]),
    ("ISO 9001", "/iso-consultancy/iso-9001/", 1, ["iso 9001 consultant saudi arabia", "iso 9001 implementation", "iso 9001 certification saudi arabia", "quality management system consultant"]),
    ("ISO 22000 and HACCP", "/iso-consultancy/iso-22000/", 1, ["iso 22000 consultant saudi arabia", "haccp consultant riyadh", "haccp consultant jeddah", "food safety consultant saudi arabia"]),
    ("ISO 45001", "/iso-consultancy/iso-45001/", 2, ["iso 45001 consultant saudi arabia", "iso 45001 certification riyadh", "occupational health and safety iso 45001"]),
    ("ISO 14001", "/iso-consultancy/iso-14001/", 2, ["iso 14001 consultant saudi arabia", "iso 14001 certification riyadh", "environmental management system consultant"]),
    ("ISO 27001", "/iso-consultancy/iso-27001/", 2, ["iso 27001 consultant saudi arabia", "iso 27001 certification riyadh", "information security consultant riyadh"]),
    ("Other standards", "/iso-consultancy/other-standards/", 3, ["iso 50001 consultant saudi arabia", "iso 22301 consultant", "iso 37001 consultant", "halal certification consultant saudi arabia"]),
]
TRAIN_AR = [
    ("General", "/iso-consultancy/training/", 2, ["دورات ايزو الرياض", "دورات ايزو جدة", "تدريب ايزو", "دورة مدقق داخلي ايزو", "دورة المدقق الداخلي الرياض"]),
    ("ISO 9001", "/iso-consultancy/iso-9001-training/", 1, ["دورة ايزو 9001", "تدريب ايزو 9001", "دورة مدقق داخلي ايزو 9001", "دورة ايزو 9001 الرياض", "دورة ايزو 9001 جدة"]),
    ("ISO 14001", "/iso-consultancy/iso-14001-training/", 2, ["دورة ايزو 14001", "دورة مدقق داخلي ايزو 14001", "تدريب ايزو 14001"]),
    ("ISO 45001", "/iso-consultancy/iso-45001-training/", 2, ["دورة ايزو 45001", "دورة مدقق داخلي ايزو 45001", "دورة السلامة والصحة المهنية ايزو 45001"]),
    ("ISO 22000 and HACCP", "/iso-consultancy/iso-22000-training/", 1, ["دورة هاسب", "دورة هاسب الرياض", "دورة ايزو 22000", "دورة سلامة الغذاء هاسب", "دورة مدقق داخلي ايزو 22000"]),
    ("ISO 27001", "/iso-consultancy/iso-27001-training/", 2, ["دورة ايزو 27001", "دورة مدقق داخلي ايزو 27001", "تدريب امن المعلومات ايزو 27001"]),
]
TRAIN_EN = [
    ("General", "/iso-consultancy/training/", 2, ["iso training riyadh", "iso training jeddah", "iso internal auditor course", "iso internal auditor training saudi arabia"]),
    ("ISO 9001", "/iso-consultancy/iso-9001-training/", 1, ["iso 9001 training riyadh", "iso 9001 training jeddah", "iso 9001 internal auditor course", "iso 9001 foundation course", "iso 9001 training saudi arabia"]),
    ("ISO 14001", "/iso-consultancy/iso-14001-training/", 2, ["iso 14001 training saudi arabia", "iso 14001 internal auditor course"]),
    ("ISO 45001", "/iso-consultancy/iso-45001-training/", 2, ["iso 45001 training saudi arabia", "iso 45001 internal auditor course"]),
    ("ISO 22000 and HACCP", "/iso-consultancy/iso-22000-training/", 1, ["haccp training riyadh", "haccp training jeddah", "iso 22000 internal auditor course", "food safety training saudi arabia"]),
    ("ISO 27001", "/iso-consultancy/iso-27001-training/", 2, ["iso 27001 training saudi arabia", "iso 27001 internal auditor course"]),
]
GROUPS = {"01 Pest | Arabic": PEST_AR, "02 Pest | English": PEST_EN, "03 ISO Consultancy | Arabic": ISO_AR, "04 ISO Consultancy | English": ISO_EN,
          "05 ISO Training | Arabic": TRAIN_AR, "06 ISO Training | English": TRAIN_EN}

# ------------------------------------------------------------------ ad copy
# Headlines <= 30 characters, descriptions <= 90. No prices, guarantees, superlatives or unverifiable claims.
SHARED = {
 ("pest", "ar"): dict(
    h=["فحص مجاني للموقع", "اطلب فحصاً مجانياً", "تقرير خدمة مكتوب", "نخدم الرياض وجدة", "مكافحة تبدأ بالفحص", "تواصل عبر واتساب", "أومنكسا سوليوشنز", "اتصل الآن"],
    d=["اطلب فحصاً مجانياً للموقع. نقدم خطة مكتوبة ونتابع بعد المعالجة.", "للمنازل والمطاعم والمستودعات في الرياض وجدة. تواصل معنا عبر واتساب."]),
 ("pest", "en"): dict(
    h=["Free Site Inspection", "Request a Free Inspection", "Written Service Report", "Riyadh and Jeddah", "Inspection-Led Pest Control", "WhatsApp Us Today", "Omnexa Solutions", "Call Now"],
    d=["Request a free site inspection. We give a written plan and follow up after treatment.", "For homes, restaurants and warehouses in Riyadh and Jeddah. Message us on WhatsApp."]),
 ("iso", "ar"): dict(
    h=["استشارة أيزو مجانية", "احجز استشارة مجانية", "نجهّزك لتدقيق الشهادة", "تحليل الفجوات والتوثيق", "الرياض وجدة", "تواصل عبر واتساب", "أومنكسا سوليوشنز", "اتصل الآن"],
    d=["نحلل الفجوات ونبني النظام مع فريقك ونجهّزك لتدقيق جهة منح الشهادات المعتمدة.", "احجز استشارة أيزو مجانية في الرياض أو جدة. تواصل معنا عبر واتساب."]),
 ("iso", "en"): dict(
    h=["Free ISO Consultation", "Book a Free Consultation", "We Prepare You for the Audit", "Gap Analysis to Audit Prep", "Riyadh and Jeddah", "WhatsApp Us Today", "Omnexa Solutions", "Call Now"],
    d=["We run the gap analysis, build the system with your team and prepare you for the audit.", "Book a free ISO consultation in Riyadh or Jeddah. Message us on WhatsApp."]),
 ("train", "ar"): dict(
    h=["اطلب عرض سعر", "دورات في مقرّكم", "شهادة حضور", "الرياض وجدة", "تدريب عملي بأمثلتكم", "تواصل عبر واتساب", "أومنكسا سوليوشنز", "اتصل الآن"],
    d=["دورات تأسيسية ومدقق داخلي لفريقك، في مقرّكم أو مقرّنا. اطلب عرض سعر.", "أخبرنا بالدورة وعدد المشاركين والمواعيد وسنرسل لك عرض سعر مكتوباً."]),
 ("train", "en"): dict(
    h=["Request a Quote", "Courses at Your Premises", "Attendance Certificates", "Riyadh and Jeddah", "Practical, Hands-On Training", "WhatsApp Us Today", "Omnexa Solutions", "Call Now"],
    d=["Foundation and auditor courses for your team, at your site or ours. Request a quote.", "Tell us the course, number of people and dates. We will send a written quote."]),
}
SPECIFIC = {  # ad group -> (headlines, descriptions) per language; written for each group
 ("pest", "ar"): {
  "General | Riyadh": (["مكافحة حشرات في الرياض", "شركة مكافحة حشرات الرياض", "للمنازل والشركات"], ["مكافحة حشرات في الرياض تبدأ بالفحص وتنتهي بتقرير مكتوب. اطلب فحصاً مجانياً."]),
  "General | Jeddah": (["مكافحة حشرات في جدة", "شركة مكافحة حشرات جدة", "للمنازل والشركات"], ["مكافحة حشرات في جدة تبدأ بالفحص وتنتهي بتقرير مكتوب. اطلب فحصاً مجانياً."]),
  "Termite": (["مكافحة النمل الأبيض", "معالجة التربة قبل البناء", "فحص النمل الأبيض مجاناً"], ["فحص ومعالجة النمل الأبيض للفلل والمباني الجديدة والقائمة، مع سجل معالجة مكتوب."]),
  "Rodents": (["مكافحة الفئران والقوارض", "سدّ المنافذ والمراقبة", "محطات طُعم آمنة"], ["نكتشف منافذ الدخول ونعالج النشاط وننصح بالحماية حتى لا تعود القوارض."]),
  "Cockroaches": (["مكافحة الصراصير", "مكافحة المطابخ والمطاعم", "معالجة المصارف"], ["نحدد النوع ومصدر الإصابة ونعالج المطبخ والمصارف، مع زيارة متابعة."]),
  "Bed bugs": (["مكافحة بق الفراش", "للمنازل والفنادق", "فحص ومعالجة ومتابعة"], ["فحص غرفة بغرفة ومعالجة الأسرّة والأثاث، مع زيارة متابعة بعد فقس البيض."]),
  "Fumigation": (["تبخير المستودعات", "تبخير الحاويات والبضائع", "إجراءات سلامة وتصريح"], ["تبخير مخطط بإجراءات سلامة وتصريح مكتوب قبل إعادة الدخول. اطلب معاينة."]),
  "Mosquito and dengue": (["مكافحة البعوض", "مكافحة بعوض حمى الضنك", "فحص مواقع التكاثر"], ["نحدد مواقع التكاثر ونعالج اليرقات والبعوض البالغ للمنازل والمجمعات والمنشآت."]),
  "Birds": (["مكافحة الحمام والطيور", "شباك وأشواك وأسلاك", "تنظيف الأعشاش"], ["حماية دائمة من الحمام بالشباك والأشواك وتنظيف الأعشاش والفضلات بمعدات وقاية."]),
  "Snakes and wildlife": (["مكافحة الثعابين", "مكافحة السحالي", "إمساك آمن بفنيين مدرّبين"], ["إمساك الثعابين وإزالتها بأمان على أيدي فنيين مدرّبين، ونصائح لمنع عودتها."]),
  "Commercial": (["مكافحة حشرات للمنشآت", "مطاعم ومصانع وفنادق", "سجلات جاهزة للتدقيق"], ["برامج مجدولة مع نقاط مراقبة وتقارير بعد كل زيارة، جاهزة لتدقيق سلامة الغذاء."]),
 },
 ("pest", "en"): {
  "General | Riyadh": (["Pest Control in Riyadh", "Pest Control Company Riyadh", "Homes and Businesses"], ["Pest control in Riyadh that starts with an inspection and ends with a written report."]),
  "General | Jeddah": (["Pest Control in Jeddah", "Pest Control Company Jeddah", "Homes and Businesses"], ["Pest control in Jeddah that starts with an inspection and ends with a written report."]),
  "Termite": (["Termite Control", "Pre-Construction Treatment", "Free Termite Inspection"], ["Termite inspection and treatment for villas and buildings, with a written record."]),
  "Rodents": (["Rodent and Rat Control", "Proofing and Monitoring", "Secure Bait Stations"], ["We find entry points, treat the activity and advise on proofing so rodents stay out."]),
  "Cockroaches": (["Cockroach Control", "Kitchens and Restaurants", "Drain Treatment Included"], ["We identify the species and the source, treat kitchens and drains, and follow up."]),
  "Bed bugs": (["Bed Bug Treatment", "Homes and Hotels", "Inspection and Follow-Up"], ["Room-by-room inspection, treatment of beds and furniture, and a follow-up visit."]),
  "Fumigation": (["Warehouse Fumigation", "Container Fumigation", "Safety Clearance Issued"], ["Planned fumigation with safety procedures and a written clearance before re-entry."]),
  "Mosquito and dengue": (["Mosquito Control", "Dengue Mosquito Control", "Breeding-Site Inspection"], ["We find breeding sites and treat larvae and adult mosquitoes at homes and compounds."]),
  "Birds": (["Bird and Pigeon Control", "Netting, Spikes and Wires", "Nest Cleaning"], ["Lasting protection from pigeons with netting, spikes and wires, plus safe nest cleaning."]),
  "Snakes and wildlife": (["Snake Removal", "Lizard Control", "Trained Handlers"], ["Safe snake capture and removal by trained staff, plus advice to stop them returning."]),
  "Commercial": (["Commercial Pest Control", "Restaurants and Factories", "Audit-Ready Records"], ["Scheduled programmes with monitoring points and a report after every visit."]),
 },
 ("iso", "ar"): {
  "General | Riyadh": (["استشارات أيزو في الرياض", "مستشار أيزو الرياض", "من الفجوات إلى التدقيق"], ["استشارات أيزو في الرياض: تحليل الفجوات والتوثيق والتدقيق الداخلي والتحضير للشهادة."]),
  "General | Jeddah": (["استشارات أيزو في جدة", "مستشار أيزو جدة", "من الفجوات إلى التدقيق"], ["استشارات أيزو في جدة: تحليل الفجوات والتوثيق والتدقيق الداخلي والتحضير للشهادة."]),
  "ISO 9001": (["استشارات ISO 9001", "نظام إدارة الجودة", "يشمل إصدار 2026"], ["نبني نظام إدارة الجودة معك ونجهّزك لتدقيق ISO 9001، بما في ذلك إصدار 2026."]),
  "ISO 22000 and HACCP": (["استشارات ISO 22000 وهاسب", "سلامة الغذاء", "للمصانع والمطابخ"], ["نطبّق نظام سلامة الغذاء وهاسب لمصانع الأغذية والمطابخ ونجهّزك للتدقيق."]),
  "ISO 45001": (["استشارات ISO 45001", "الصحة والسلامة المهنية", "للمقاولين والمصانع"], ["نبني نظام الصحة والسلامة المهنية ونجهّزك لتدقيق ISO 45001."]),
  "ISO 14001": (["استشارات ISO 14001", "نظام الإدارة البيئية", "يشمل إصدار 2026"], ["نطبّق نظام الإدارة البيئية ISO 14001 ونجهّزك لتدقيق الشهادة، بما في ذلك إصدار 2026."]),
  "ISO 27001": (["استشارات ISO 27001", "أمن المعلومات", "تقييم المخاطر والسياسات"], ["نطبّق نظام أمن المعلومات ISO 27001 من تقييم المخاطر إلى التحضير للتدقيق."]),
  "Other standards": (["معايير أيزو أخرى", "ISO 50001 و22301 و37001", "أنظمة سلامة الغذاء"], ["استشارات ISO 50001 و22301 و37001 وأنظمة سلامة الغذاء ومراجعات الموردين."]),
 },
 ("iso", "en"): {
  "General | Riyadh": (["ISO Consultants in Riyadh", "ISO Consultancy Riyadh", "Gap Analysis to Audit"], ["ISO consultancy in Riyadh: gap analysis, documentation, internal audit, audit prep."]),
  "General | Jeddah": (["ISO Consultants in Jeddah", "ISO Consultancy Jeddah", "Gap Analysis to Audit"], ["ISO consultancy in Jeddah: gap analysis, documentation, internal audit, audit prep."]),
  "ISO 9001": (["ISO 9001 Consultants", "Quality Management System", "Includes the 2026 Edition"], ["We build your quality system and prepare you for the ISO 9001 audit, incl. 2026 edition."]),
  "ISO 22000 and HACCP": (["ISO 22000 and HACCP", "Food Safety Consultants", "Factories and Kitchens"], ["We implement ISO 22000 and HACCP for food factories and kitchens. Audit prep included."]),
  "ISO 45001": (["ISO 45001 Consultants", "Health and Safety System", "Contractors and Factories"], ["We build your health and safety system and prepare you for the ISO 45001 audit."]),
  "ISO 14001": (["ISO 14001 Consultants", "Environmental Management", "Includes the 2026 Edition"], ["We implement ISO 14001 and prepare you for the audit, including the 2026 edition."]),
  "ISO 27001": (["ISO 27001 Consultants", "Information Security", "Risk Assessment and Policies"], ["We implement ISO 27001 from risk assessment to audit preparation."]),
  "Other standards": (["Other ISO Standards", "ISO 50001, 22301, 37001", "Food Safety Schemes"], ["Consultancy for ISO 50001, 22301, 37001, food safety schemes and supplier audits."]),
 },
 ("train", "ar"): {
  "General": (["دورات أيزو في الرياض وجدة", "دورات المدقق الداخلي", "تدريب في مقرّكم"], ["دورات تأسيسية ومدقق داخلي على معايير الأيزو، في مقرّكم أو مقرّنا. اطلب عرض سعر."]),
  "ISO 9001": (["دورة ISO 9001", "دورة المدقق الداخلي", "دورة الانتقال لإصدار 2026"], ["دورات ISO 9001: تأسيسية ومدقق داخلي والانتقال إلى إصدار 2026. اطلب عرض سعر."]),
  "ISO 14001": (["دورة ISO 14001", "دورة المدقق الداخلي", "الإدارة البيئية"], ["دورات ISO 14001: تأسيسية ومدقق داخلي والانتقال إلى إصدار 2026. اطلب عرض سعر."]),
  "ISO 45001": (["دورة ISO 45001", "دورة المدقق الداخلي", "ورشة تقييم المخاطر"], ["دورات ISO 45001: تأسيسية ومدقق داخلي وورشة تقييم المخاطر. اطلب عرض سعر."]),
  "ISO 22000 and HACCP": (["دورة هاسب (HACCP)", "دورة ISO 22000", "فريق هاسب والمدققون"], ["دورات هاسب وISO 22000: توعية وفريق هاسب ومدقق داخلي. اطلب عرض سعر."]),
  "ISO 27001": (["دورة ISO 27001", "دورة المدقق الداخلي", "ورشة تقييم المخاطر"], ["دورات ISO 27001: تأسيسية ومدقق داخلي وورشة تقييم مخاطر أمن المعلومات. اطلب عرض سعر."]),
 },
 ("train", "en"): {
  "General": (["ISO Training Riyadh Jeddah", "Internal Auditor Courses", "Training at Your Site"], ["ISO foundation and internal auditor courses, at your site or ours. Request a quote."]),
  "ISO 9001": (["ISO 9001 Training", "Internal Auditor Course", "2026 Transition Course"], ["ISO 9001 foundation, internal auditor and 2026 transition courses. Request a quote."]),
  "ISO 14001": (["ISO 14001 Training", "Internal Auditor Course", "Environmental Management"], ["ISO 14001 foundation, internal auditor and 2026 transition courses. Request a quote."]),
  "ISO 45001": (["ISO 45001 Training", "Internal Auditor Course", "Risk Assessment Workshop"], ["ISO 45001 foundation, internal auditor and risk assessment courses. Request a quote."]),
  "ISO 22000 and HACCP": (["HACCP Training", "ISO 22000 Courses", "HACCP Team and Auditors"], ["HACCP and ISO 22000 courses: awareness, HACCP team and internal auditor. Request a quote."]),
  "ISO 27001": (["ISO 27001 Training", "Internal Auditor Course", "Risk Assessment Workshop"], ["ISO 27001 foundation, internal auditor and risk assessment courses. Request a quote."]),
 },
}

# ------------------------------------------------------------------ negative keywords
NEG = {
 "All campaigns": ["وظائف", "وظيفة", "توظيف", "jobs", "job", "hiring", "vacancy", "salary", "راتب", "تدريب منتهي بالتوظيف", "مجانا pdf", "pdf", "ويكيبيديا", "wikipedia", "download", "تحميل"],
 "Pest campaigns": ["ايزو", "iso", "دورة", "دورات", "course", "training", "للبيع", "شراء", "متجر", "shop", "store", "مبيد للبيع", "pesticide for sale", "buy", "diy", "بنفسك", "وصفة", "طريقة عمل", "home remedy", "natural remedy", "كيف اتخلص", "how to get rid", "game", "لعبة", "مسلسل", "فيلم", "movie"],
 "ISO consultancy campaigns": ["مكافحة", "حشرات", "pest", "تدريب", "دورة", "دورات", "course", "training", "trainer", "مدرب", "وظائف", "pdf", "نموذج", "template", "free template", "مجانا"],
 "ISO training campaigns": ["مكافحة", "حشرات", "pest", "وظائف", "pdf", "نموذج", "template", "مجانا pdf", "اسئلة وإجابات", "exam questions", "answers", "dumps"],
}
NEG_NOTE = "Add as phrase or exact negatives at campaign or account level. Review the Search Terms report weekly and extend this list."

# ------------------------------------------------------------------ build
def city_of(group):
    return "Riyadh" if "Riyadh" in group else ("Jeddah" if "Jeddah" in group else "Riyadh + Jeddah")


def main():
    rows, copy_rows, problems = [], [], []
    for camp, (lang, svc) in CAMPAIGNS.items():
        ar = lang == "Arabic"
        for name, path, prio, kws in GROUPS[camp]:
            final = url(path, ar)
            for k in kws:
                for mt in ("Phrase", "Exact"):
                    rows.append([camp, f"{name}", k, mt, lang, city_of(name), final, f"Phase {prio}"])
            sh = SHARED[(svc, "ar" if ar else "en")]
            sp_h, sp_d = SPECIFIC[(svc, "ar" if ar else "en")][name]
            heads = sp_h + sh["h"]
            descs = sp_d + sh["d"]
            for h in heads:
                if len(h) > 30: problems.append(("headline>30", camp, name, h, len(h)))
            for d in descs:
                if len(d) > 90: problems.append(("description>90", camp, name, d, len(d)))
            if len(heads) > 15: problems.append(("too many headlines", camp, name, len(heads), 0))
            copy_rows.append([camp, name, lang, final] + heads + [""] * (15 - len(heads)) + descs + [""] * (4 - len(descs)))
    with open(os.path.join(OUT, "keyword-plan.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["Campaign", "Ad group", "Keyword", "Match type", "Language", "City", "Final URL", "Launch phase"]); w.writerows(rows)
    with open(os.path.join(OUT, "ad-copy.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["Campaign", "Ad group", "Language", "Final URL"] + [f"Headline {i}" for i in range(1, 16)] + [f"Description {i}" for i in range(1, 5)])
        w.writerows(copy_rows)
    with open(os.path.join(OUT, "negative-keywords.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["Applies to", "Negative keyword"])
        for scope, items in NEG.items():
            for k in items: w.writerow([scope, k])
    ngroups = sum(len(GROUPS[c]) for c in CAMPAIGNS)
    print(f"{len(CAMPAIGNS)} campaigns, {ngroups} ad groups, {len(rows)} keyword rows ({len(rows)//2} keywords x 2 match types), {len(copy_rows)} ads")
    if problems:
        print("LENGTH PROBLEMS:")
        for p in problems: print(" ", p)
        sys.exit(1)
    print("all headline/description lengths OK")


main()
