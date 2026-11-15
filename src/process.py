"""Process workflow content and animated step illustrations.
Durations are typical, not commitments. No guarantees are stated here."""

PROCESS = {
"pest": [
 dict(id="enquire", icon="call", title="Request an inspection", time="We reply during business hours",
      short="Call, WhatsApp or send the form.",
      we="Take your enquiry, note the site, the pest and a convenient time, and confirm the visit.",
      you="Tell us what you have seen, the type of site, and who will give access.",
      get="A confirmed visit time and the technician's name."),
 dict(id="inspect", icon="inspect", title="Site inspection", time="Typically 30 to 90 minutes",
      short="We find the pest, the entry points and the cause.",
      we="Inspect inside and outside, identify the pest, find entry points and the conditions that attract it, and take photos.",
      you="Give access and point out where you have seen activity. Tell us about children, pets and food areas.",
      get="Findings explained on the spot, in plain language."),
 dict(id="plan", icon="plan", title="Written plan and quotation", time="Same visit or shortly after",
      short="Method, products, visits and price in writing.",
      we="Write up the method, the products, the preparation needed, the number of visits and the price.",
      you="Review the scope, ask questions, and approve.",
      get="A written quotation. Nothing starts before you agree."),
 dict(id="treat", icon="treat", title="Treatment", time="Depends on site size and pest",
      short="Carried out with minimal disruption.",
      we="Carry out the treatment in protective equipment, place and number bait stations, and seal gaps where agreed.",
      you="Complete the preparation steps and keep people and pets out of treated areas for the stated time.",
      get="Re-entry time and safety instructions, before we leave."),
 dict(id="report", icon="report", title="Service report", time="Handed over after every visit",
      short="A record of what was found and done.",
      we="Leave a written report: findings, areas treated, products used with their registration numbers, and recommendations.",
      you="Keep the report with your records. Food and hospitality sites will need it for audits.",
      get="A dated, signed service report."),
 dict(id="follow", icon="follow", title="Follow-up and monitoring", time="Timed to the pest's life cycle",
      short="Making sure the problem stays solved.",
      we="Return for the follow-up visit, check activity, and adjust the plan. Contracts get scheduled visits and trend reviews.",
      you="Tell us if you see any activity between visits.",
      get="An updated report and, for contracts, a trend summary."),
],
"iso": [
 dict(id="consult", icon="talk", title="Free consultation", time="One meeting",
      short="Which standard, and why.",
      we="Understand why you need ISO (a tender, a customer, growth), agree the right standard and the scope.",
      you="Share the tender or customer requirement, your headcount and your sites.",
      get="A recommended standard, a rough timeline and a written quotation."),
 dict(id="gap", icon="gap", title="Gap analysis", time="Typically 1 to 2 weeks",
      short="What you have, and what is missing.",
      we="Compare your current practice with the standard, interview managers, and list every gap.",
      you="Give access to managers and to the documents you already use.",
      get="A gap report and a dated project plan."),
 dict(id="docs", icon="docs", title="Design and documentation", time="Typically 4 to 8 weeks",
      short="Policies, process maps and procedures.",
      we="Write the policy, process maps, procedures and forms with your team, in your own words and workflow.",
      you="Name process owners, review drafts and approve them.",
      get="Your management system documents."),
 dict(id="train", icon="train", title="Implementation and training", time="Typically 4 to 8 weeks",
      short="Put it into daily use.",
      we="Train staff and internal auditors, and support your team while the system starts running.",
      you="Run the processes and keep the records.",
      get="A trained team and a running system with records."),
 dict(id="audit", icon="audit", title="Internal audit and review", time="Typically 2 to 3 weeks",
      short="Find the problems before the auditor does.",
      we="Audit the system against the standard, report findings, and support corrective actions.",
      you="Fix the findings and hold the management review.",
      get="An internal audit report and management review minutes."),
 dict(id="cert", icon="cert", title="Certification audit", time="Scheduled by the certification body",
      short="Stage 1 and Stage 2, by an accredited body.",
      we="Help you choose an accredited certification body, prepare you, and support you through the audit and any findings.",
      you="Host the auditors. The certification body, not us, decides.",
      get="A certificate from the certification body, if you meet the standard."),
 dict(id="renew", icon="renew", title="Maintain and renew", time="Three-year certificate cycle",
      short="Surveillance audits and recertification.",
      we="Support annual surveillance audits and prepare you for recertification.",
      you="Keep operating the system and keep the records up to date.",
      get="A certificate that stays valid."),
],
}

# Each scene is 160x110. Classes: ln (ink line), ac (accent line), fl (accent fill), tn (tint fill), w (white fill)
# Animations (see style.css) run when the panel/step is active.
_S = {
"call": '<rect class="w ln" x="58" y="12" width="44" height="86" rx="9"/><path class="ln" d="M72 20h16"/><circle class="ln" cx="80" cy="88" r="3"/>'
        '<g class="a-pop"><path class="fl" d="M104 28h30a6 6 0 0 1 6 6v14a6 6 0 0 1-6 6h-18l-8 7v-7h-4a6 6 0 0 1-6-6V34a6 6 0 0 1 6-6z"/></g>'
        '<g class="a-blink"><circle class="wf" cx="112" cy="41" r="2.4"/><circle class="wf b2" cx="120" cy="41" r="2.4"/><circle class="wf b3" cx="128" cy="41" r="2.4"/></g>',
"inspect": '<path class="w ln" d="M36 92V54l44-34 44 34v38z"/><rect class="tn ln" x="68" y="64" width="24" height="28" rx="2"/>'
        '<g class="a-scan"><circle class="ac glass" cx="60" cy="48" r="16"/><path class="ac" d="m72 60 16 16"/></g>',
"plan": '<rect class="w ln" x="46" y="10" width="68" height="90" rx="6"/>'
        '<path class="ac a-draw d1" pathLength="1" d="M58 30h44"/><path class="ac a-draw d2" pathLength="1" d="M58 44h44"/><path class="ac a-draw d3" pathLength="1" d="M58 58h30"/>'
        '<g class="a-pop"><circle class="fl" cx="100" cy="84" r="11"/><path class="wl" d="m95 84 4 4 7-8"/></g>',
"treat": '<g class="a-ring"><circle class="ac" cx="80" cy="56" r="40" fill="none"/></g><g class="a-ring r2"><circle class="ac" cx="80" cy="56" r="40" fill="none"/></g>'
        '<g class="a-pop"><path class="fl" d="M80 18l26 10v20c0 17-11 28-26 33-15-5-26-16-26-33V28z"/><path class="wl" d="m68 54 8 8 16-18"/></g>',
"report": '<rect class="w ln" x="44" y="14" width="72" height="88" rx="6"/><rect class="fl" x="66" y="8" width="28" height="12" rx="4"/>'
        '<rect class="ln" x="54" y="36" width="10" height="10" rx="2"/><path class="ac a-draw d1" pathLength="1" d="m56 41 3 3 5-6"/><path class="ln" d="M72 41h34"/>'
        '<rect class="ln" x="54" y="56" width="10" height="10" rx="2"/><path class="ac a-draw d2" pathLength="1" d="m56 61 3 3 5-6"/><path class="ln" d="M72 61h34"/>'
        '<rect class="ln" x="54" y="76" width="10" height="10" rx="2"/><path class="ac a-draw d3" pathLength="1" d="m56 81 3 3 5-6"/><path class="ln" d="M72 81h26"/>',
"follow": '<rect class="w ln" x="30" y="18" width="100" height="78" rx="8"/><path class="ln" d="M30 38h100M54 10v14M106 10v14"/>'
        '<g class="ln" fill="none"><path d="M44 52h12M70 52h12M96 52h12M44 66h12M70 66h12M96 66h12M44 80h12M70 80h12"/></g>'
        '<g class="a-hop"><circle class="fl" cx="102" cy="80" r="9"/><path class="wl" d="m98 80 3 3 6-7"/></g>',
"talk": '<g class="a-pop"><path class="fl" d="M24 22h56a8 8 0 0 1 8 8v20a8 8 0 0 1-8 8H48l-12 11V58h-12a8 8 0 0 1-8-8V30a8 8 0 0 1 8-8z" transform="translate(4 0)"/></g>'
        '<g class="a-pop p2"><path class="w ln" d="M86 46h50a8 8 0 0 1 8 8v20a8 8 0 0 1-8 8h-10v11l-12-11H86a8 8 0 0 1-8-8V54a8 8 0 0 1 8-8z"/></g>'
        '<path class="wl" d="M36 34h36M36 44h24"/>',
"gap": '<path class="ln" d="M24 96h112"/><rect class="tn ln a-grow" x="40" y="58" width="30" height="38" rx="3"/><rect class="w ln" x="90" y="22" width="30" height="74" rx="3"/>'
        '<path class="ac a-draw d2" pathLength="1" d="M55 52V30h30"/><g class="a-pop"><path class="fl" d="M78 22l10 8-10 8z"/></g>',
"docs": '<g class="a-slide s1"><rect class="tn ln" x="42" y="22" width="64" height="72" rx="5"/></g><g class="a-slide s2"><rect class="w ln" x="52" y="14" width="64" height="72" rx="5"/></g>'
        '<g class="a-slide s3"><rect class="w ln" x="62" y="6" width="64" height="72" rx="5"/><path class="ac" d="M74 24h40M74 36h40M74 48h26"/></g>',
"train": '<rect class="w ln" x="22" y="12" width="116" height="46" rx="5"/><path class="ac a-draw d1" pathLength="1" d="M36 28h50"/><path class="ac a-draw d2" pathLength="1" d="M36 42h34"/>'
        '<g class="a-pop"><circle class="fl" cx="48" cy="76" r="7"/><path class="fl" d="M36 100a12 12 0 0 1 24 0z"/></g>'
        '<g class="a-pop p2"><circle class="fl" cx="80" cy="76" r="7"/><path class="fl" d="M68 100a12 12 0 0 1 24 0z"/></g>'
        '<g class="a-pop p3"><circle class="fl" cx="112" cy="76" r="7"/><path class="fl" d="M100 100a12 12 0 0 1 24 0z"/></g>',
"audit": '<rect class="w ln" x="36" y="10" width="72" height="92" rx="6"/>'
        '<rect class="ln" x="46" y="26" width="10" height="10" rx="2"/><path class="ac a-draw d1" pathLength="1" d="m48 31 3 3 5-6"/><path class="ln" d="M64 31h34"/>'
        '<rect class="ln" x="46" y="48" width="10" height="10" rx="2"/><path class="ac a-draw d2" pathLength="1" d="m48 53 3 3 5-6"/><path class="ln" d="M64 53h34"/>'
        '<rect class="ln" x="46" y="70" width="10" height="10" rx="2"/><path class="ac a-draw d3" pathLength="1" d="m48 75 3 3 5-6"/><path class="ln" d="M64 75h26"/>'
        '<g class="a-scan2"><circle class="ac glass" cx="112" cy="60" r="14"/><path class="ac" d="m122 70 14 14"/></g>',
"cert": '<rect class="w ln" x="26" y="16" width="108" height="78" rx="6"/><path class="ln" d="M42 34h50M42 46h36M42 58h28"/>'
        '<g class="a-stamp"><path class="gold-f" d="M106 78l-8 22 10-5 6 9 4-24z"/><circle class="gold-f" cx="112" cy="68" r="19"/><circle class="wl" cx="112" cy="68" r="14" fill="none" stroke-dasharray="2 4"/><path class="wl" d="m104 68 6 6 11-12"/></g>',
"renew": '<g class="a-spin"><path class="ac" fill="none" d="M80 22a34 34 0 0 1 29 17"/><path class="ac" fill="none" d="M109 71a34 34 0 0 1-58 0"/><path class="ac" fill="none" d="M51 39A34 34 0 0 1 80 22"/>'
        '<path class="fl" d="m106 30 8 12-14 2z"/><path class="fl" d="m60 84-14-4 8-12z"/><path class="fl" d="m54 36 14-2-4 12z"/></g>'
        '<text x="80" y="62" text-anchor="middle" class="svgt">3 yr</text>',
}


def scene(key, lang="en"):
    inner = _S[key]
    if lang == "ar":
        inner = inner.replace(">3 yr<", ">3 سنوات<")
    return ('<svg class="scene" viewBox="0 0 160 110" role="img" aria-hidden="true">' + inner + "</svg>")


# Sample service report fields (clearly marked as a sample on the page)
SAMPLE_REPORT = [
    ("Date and time", "14 March, 10:30 to 11:45"),
    ("Site", "Restaurant kitchen and store, ground floor"),
    ("Technician", "Name and ID shown on the report"),
    ("Findings", "German cockroach activity behind the dishwasher and under the prep sink. No rodent activity."),
    ("Areas treated", "Kitchen, dry store, staff area, floor drains"),
    ("Products used", "Product name and registration number for each product"),
    ("Re-entry", "Kitchen may be used again after 2 hours"),
    ("Recommendations", "Seal gap at the dishwasher wall. Keep cardboard out of the store."),
    ("Next visit", "Follow-up in 2 weeks"),
]

# Illustrative project plan (weeks): (label, start, end, who)
SAMPLE_GANTT = [
    ("Gap analysis", 1, 2, "us"),
    ("Documentation", 3, 10, "us"),
    ("Implementation and training", 8, 16, "us"),
    ("Internal audit", 15, 17, "us"),
    ("Management review", 17, 18, "you"),
    ("Stage 1 audit", 18, 19, "cb"),
    ("Stage 2 audit", 21, 23, "cb"),
]
