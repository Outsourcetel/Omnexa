# Page content. Keep claims factual and unsupported superlatives out (Google Ads policy).
# {city} is replaced with config primary_city at build time.

PEST_STEPS = [
    ("Site inspection", "A technician inspects the premises, identifies the pest, entry points and conditions that attract it."),
    ("Treatment plan", "You get a written plan with the method, products, and any preparation needed."),
    ("Treatment", "Treatment is carried out with minimal disruption to your operations or household."),
    ("Follow-up and records", "Follow-up visits and service reports, so you can show what was done."),
]

PEST = {
    "hub": dict(
        slug="pest-control",
        title="Pest Control in {city}, Saudi Arabia | Omnexa Solutions",
        desc="Pest control in {city} for homes, restaurants, warehouses and factories. Termites, rodents, cockroaches, bed bugs and fumigation. Free site inspection.",
        h1="Pest Control in {city}",
        lead="Inspection-led pest management for homes, restaurants, hotels, warehouses and food facilities. Request a free site inspection today.",
        service="Pest Control",
        intro="Omnexa Solutions provides pest control and Integrated Pest Management (IPM) programmes in {city} and across Saudi Arabia. We start with an inspection, recommend a treatment plan, and keep service records for every visit.",
        bullets=["General insect control (cockroaches, ants, flies)", "Termite control (pre- and post-construction)", "Rodent control", "Bed bug treatment", "Fumigation for warehouses and stored goods", "Bird and reptile control", "Mosquito control", "Scheduled contracts for commercial sites"],
        steps=PEST_STEPS,
        faqs=[
            ("Do you offer a free inspection?", "Yes. Request a free site inspection using the form, WhatsApp or phone, and we will arrange a visit."),
            ("Do you serve businesses as well as homes?", "Yes. We serve homes, restaurants, hotels, healthcare sites, warehouses and food facilities, including scheduled contracts."),
            ("Is the treatment safe for people and pets?", "Treatment methods and products depend on the pest and the site. Tell us about children, pets or food areas when you book, and we will plan around them."),
            ("Will you give us service reports?", "Yes. We provide service records after visits, which are useful for audits and inspections."),
        ],
        children=["termite-control", "rodent-control", "cockroach-control", "bed-bug-treatment", "fumigation", "commercial-ipm"],
    ),
    "termite-control": dict(
        title="Termite Control in {city} | Pre & Post Construction | Omnexa Solutions",
        desc="Termite treatment in {city}: inspection, soil and wood treatment, and pre-construction anti-termite protection. Book a free inspection.",
        h1="Termite Control in {city}",
        lead="Find out whether you have termites and get a treatment plan. Free site inspection.",
        service="Termite Control",
        intro="Termites often cause damage before they are noticed. We inspect for activity, identify the type, and recommend a treatment suited to the building and its stage of construction.",
        bullets=["Inspection and activity assessment", "Post-construction treatment for existing buildings", "Pre-construction soil treatment", "Wood and structural treatment", "Follow-up inspections", "Written treatment records"],
        steps=PEST_STEPS,
        faqs=[
            ("How do I know if I have termites?", "Common signs are mud tubes, hollow-sounding wood, discarded wings and damaged skirting or door frames. An inspection confirms it."),
            ("Can termites be prevented in a new building?", "Pre-construction treatment of the soil is commonly done before the slab is poured. Contact us early in the project."),
            ("How long does treatment take?", "It depends on the size of the property and the infestation. We confirm the scope and timing after the inspection."),
        ],
    ),
    "rodent-control": dict(
        title="Rodent & Rat Control in {city} | Omnexa Solutions",
        desc="Rat and mouse control in {city} for homes, restaurants and warehouses. Inspection, proofing and monitoring. Request a free inspection.",
        h1="Rodent Control in {city}",
        lead="Stop rats and mice at the source: inspection, proofing advice, and monitoring.",
        service="Rodent Control",
        intro="Rodents carry contamination risks and damage cables, stock and structures. We find how they get in, treat the activity, and advise on proofing so they do not return.",
        bullets=["Inspection and entry-point identification", "Baiting and trapping, placed away from food and children", "Proofing recommendations", "Monitoring stations for commercial sites", "Service reports for audits"],
        steps=PEST_STEPS,
        faqs=[
            ("Is rodent control safe around food areas?", "We plan placement around food handling and storage areas and use monitoring methods suited to the site."),
            ("Do you offer regular contracts?", "Yes. Restaurants, warehouses and food facilities usually need scheduled visits and monitoring."),
        ],
    ),
    "cockroach-control": dict(
        title="Cockroach & Insect Control in {city} | Omnexa Solutions",
        desc="Cockroach, ant and fly control in {city} for homes and commercial kitchens. Free inspection and treatment plan.",
        h1="Cockroach and Insect Control in {city}",
        lead="Targeted treatment for cockroaches, ants, flies and other crawling and flying insects.",
        service="Cockroach / Insect Control",
        intro="Cockroaches and other insects are common in kitchens, drains and storage areas. We identify the species and the source, then treat accordingly.",
        bullets=["Inspection of kitchens, drains and storage areas", "Gel, spray and monitoring treatments as suited", "Fly and flying insect control", "Ant control", "Advice on sanitation and sealing", "Follow-up visits"],
        steps=PEST_STEPS,
        faqs=[
            ("How quickly do I see results?", "It depends on the infestation and the site. We advise on expectations after inspecting."),
            ("Do I need to leave the property?", "Sometimes for a short time. We tell you what preparation is needed before treatment."),
        ],
    ),
    "bed-bug-treatment": dict(
        title="Bed Bug Treatment in {city} | Omnexa Solutions",
        desc="Bed bug inspection and treatment in {city} for homes, hotels and staff accommodation. Book a free inspection.",
        h1="Bed Bug Treatment in {city}",
        lead="Inspection and treatment for homes, hotels and staff accommodation.",
        service="Bed Bug Treatment",
        intro="Bed bugs spread through luggage, furniture and bedding. Effective treatment needs a proper inspection, preparation, and follow-up.",
        bullets=["Room-by-room inspection", "Treatment of beds, frames and furniture", "Preparation guidance", "Follow-up inspection", "Programmes for hotels and accommodation"],
        steps=PEST_STEPS,
        faqs=[
            ("Do I need to wash bedding first?", "We give a preparation checklist when you book, including bedding and clothing."),
            ("Can you treat a whole hotel or camp?", "Yes. We plan room-by-room treatment for hotels and staff accommodation."),
        ],
    ),
    "fumigation": dict(
        title="Fumigation Services in {city} | Warehouses & Stored Goods | Omnexa Solutions",
        desc="Fumigation for warehouses, containers and stored products in {city}. Request an assessment and quotation.",
        h1="Fumigation Services in {city}",
        lead="Fumigation for warehouses, stored goods and structures, planned and carried out with safety controls.",
        service="Fumigation",
        intro="Fumigation is used for stored-product pests and difficult infestations. It requires planning, sealing, safe handling and clearance before re-entry.",
        bullets=["Site assessment and fumigation plan", "Warehouse and storage fumigation", "Container and commodity fumigation", "Safety and re-entry clearance procedures", "Treatment records"],
        steps=PEST_STEPS,
        faqs=[
            ("Is the site closed during fumigation?", "Yes. The area is sealed and re-entry follows a clearance procedure. We plan timing with you."),
            ("Do you need notice?", "Fumigation requires scheduling and preparation. Contact us with the site details for a plan and quotation."),
        ],
    ),
    "commercial-ipm": dict(
        title="Commercial Pest Control & IPM in {city} | Food, Hotels, Healthcare",
        desc="Integrated Pest Management programmes in {city} for food facilities, hotels, hospitals and warehouses. Scheduled visits and audit-ready records.",
        h1="Commercial Pest Control and IPM in {city}",
        lead="Scheduled Integrated Pest Management programmes with monitoring and audit-ready records.",
        service="Commercial IPM Programme",
        intro="Commercial sites need ongoing control, not one-off treatments. An IPM programme combines inspection, prevention, monitoring and targeted treatment, with documentation.",
        bullets=["Risk assessment and site survey", "Monitoring devices and trend reporting", "Scheduled service visits", "Documentation for audits (e.g. food-safety schemes)", "Staff awareness guidance", "Coverage for food, hospitality, healthcare, retail and logistics sites"],
        steps=PEST_STEPS,
        faqs=[
            ("What is IPM?", "Integrated Pest Management combines prevention, monitoring and targeted treatment to control pests while limiting unnecessary chemical use."),
            ("Can you support our food-safety audits?", "We provide service reports and records. Which audit requirements apply depends on your scheme, so tell us what you are audited against."),
            ("Do you also help with ISO 22000 or HACCP?", "Yes, our ISO consultancy team can help with food-safety management systems. See the ISO consultancy section."),
        ],
    ),
}

ISO_STEPS = [
    ("Gap analysis", "We review your current processes against the standard and list what is missing."),
    ("Documentation and implementation", "We help you write the procedures and put them into practice."),
    ("Internal audit and review", "We support an internal audit and management review before the external audit."),
    ("Certification audit support", "You select an accredited certification body, and we prepare you for its audit."),
]

ISO = {
    "hub": dict(
        slug="iso-consultancy",
        title="ISO Consultants in Saudi Arabia | ISO 9001, 22000, 45001 | Omnexa Solutions",
        desc="ISO consultancy in Saudi Arabia: gap analysis, documentation, internal audit and certification preparation for ISO 9001, 22000, 45001, 14001 and 27001.",
        h1="ISO Consultants in Saudi Arabia",
        lead="Practical help to implement ISO management systems and prepare for certification. Book a free consultation.",
        service="ISO Consultancy",
        intro="Omnexa Solutions provides ISO consultancy: gap analysis, documentation, implementation, internal audit support and certification preparation. Certificates are issued by accredited certification bodies, and we prepare you for their audits.",
        bullets=["ISO 9001 Quality Management", "ISO 22000 Food Safety Management", "ISO 45001 Occupational Health and Safety", "ISO 14001 Environmental Management", "ISO 27001 Information Security", "Staff training and internal auditor training", "Surveillance audit support", "Support for tenders that require ISO"],
        steps=ISO_STEPS,
        faqs=[
            ("Are you a certification body?", "No. We are consultants. We help you implement the standard and prepare. The certificate is issued by an accredited certification body that you choose."),
            ("How long does ISO certification take?", "It varies with company size, existing processes and the standard. We give a timeline after the gap analysis."),
            ("Which ISO standard do I need?", "It depends on your industry and customers. ISO 9001 suits most companies; food businesses often need ISO 22000; contractors often need ISO 45001 and 14001."),
            ("Do you work outside Riyadh?", "Yes. We work with companies across Saudi Arabia and the Gulf. Some stages can be done remotely."),
        ],
        children=["iso-9001", "iso-22000", "iso-45001", "iso-14001", "iso-27001"],
    ),
    "iso-9001": dict(
        title="ISO 9001 Certification Consultants in Saudi Arabia | Omnexa Solutions",
        desc="ISO 9001 consultancy in Saudi Arabia, including the 2026 edition: gap analysis, documentation, internal audit and certification audit support.",
        h1="ISO 9001 Consultants in Saudi Arabia",
        lead="Implement a quality management system and prepare for ISO 9001 certification, including the new 2026 edition.",
        service="ISO 9001",
        intro="ISO 9001 is the international standard for quality management systems. It is widely requested in tenders and supplier approvals.",
        bullets=["Gap analysis against ISO 9001 (2015 or 2026 edition)", "Quality manual, procedures and records", "Process mapping and risk assessment", "Internal auditor training", "Management review support", "Certification audit preparation"],
        steps=ISO_STEPS,
        faqs=[
            ("Is ISO 9001 only for large companies?", "No. It applies to companies of any size and sector."),
            ("What documents will I need?", "At least a scope, policy, objectives, procedures and records that match your processes. We build them with you."),
        ],
    ),
    "iso-22000": dict(
        title="ISO 22000 Food Safety Consultants in Saudi Arabia | Omnexa Solutions",
        desc="ISO 22000 and HACCP consultancy for food manufacturers, caterers and restaurants in Saudi Arabia.",
        h1="ISO 22000 Food Safety Consultants",
        lead="Food safety management system implementation and audit preparation.",
        service="ISO 22000",
        intro="ISO 22000 sets requirements for a food safety management system across the food chain. It is relevant to manufacturers, caterers, packers and storage operators.",
        bullets=["Gap analysis and hazard analysis (HACCP)", "Prerequisite programmes", "Documentation and records", "Staff food-safety training", "Internal audit", "Certification audit preparation"],
        steps=ISO_STEPS,
        faqs=[
            ("What is the link between ISO 22000 and HACCP?", "ISO 22000 includes HACCP principles within a wider management system."),
            ("Do you also offer pest control for food sites?", "Yes. See our commercial pest control and IPM programme."),
        ],
    ),
    "iso-45001": dict(
        title="ISO 45001 Health & Safety Consultants in Saudi Arabia | Omnexa Solutions",
        desc="ISO 45001 occupational health and safety consultancy for contractors, factories and facilities in Saudi Arabia.",
        h1="ISO 45001 Health and Safety Consultants",
        lead="Build an occupational health and safety management system and prepare for certification.",
        service="ISO 45001",
        intro="ISO 45001 helps organisations manage health and safety risks. It is commonly requested of contractors and industrial companies.",
        bullets=["Hazard identification and risk assessment", "Policies, procedures and records", "Emergency preparedness", "HSE training", "Internal audit", "Certification audit preparation"],
        steps=ISO_STEPS,
        faqs=[("Does it replace local regulations?", "No. It is a management system standard and works alongside legal requirements.")],
    ),
    "iso-14001": dict(
        title="ISO 14001 Environmental Management Consultants | Omnexa Solutions",
        desc="ISO 14001 environmental management consultancy in Saudi Arabia: implementation and audit preparation.",
        h1="ISO 14001 Environmental Management Consultants",
        lead="Implement an environmental management system and prepare for certification.",
        service="ISO 14001",
        intro="ISO 14001 helps organisations manage environmental responsibilities, from waste to energy to compliance.",
        bullets=["Environmental aspects and impacts register", "Legal and compliance register", "Procedures and records", "Internal audit", "Certification audit preparation"],
        steps=ISO_STEPS,
        faqs=[("Who needs ISO 14001?", "It is often requested by contractors, manufacturers and companies in supply chains with environmental requirements.")],
    ),
    "iso-27001": dict(
        title="ISO 27001 Information Security Consultants | Omnexa Solutions",
        desc="ISO 27001 information security consultancy: risk assessment, policies and certification audit preparation.",
        h1="ISO 27001 Information Security Consultants",
        lead="Implement an information security management system and prepare for certification.",
        service="ISO 27001",
        intro="ISO 27001 sets requirements for managing information security risks. It is requested by many IT, finance and outsourcing buyers.",
        bullets=["Scope and risk assessment", "Statement of Applicability", "Policies and controls", "Awareness training", "Internal audit", "Certification audit preparation"],
        steps=ISO_STEPS,
        faqs=[("Is ISO 27001 only for IT companies?", "No. Any organisation handling sensitive information can use it.")],
    ),
}

OTHER = [
    ("HVAC and AC maintenance", "AC installation, servicing, cleaning and annual maintenance contracts."),
    ("Electrical works", "Electrical installation, panels, generators, UPS and fault tracing."),
    ("Plumbing and painting", "Plumbing works, leak repair, and interior and exterior painting."),
    ("Construction and fit-out", "Civil, MEP and interior fit-out works."),
]


# ---------------------------------------------------------------------------
# In-depth content blocks. Keyed by (family, slug); slug "hub" for hub pages.
# Block types:
#   ("table", id, kicker, title, intro, [headers], [[cells]...], note)
#   ("list",  id, kicker, title, intro, [items])
#   ("cards", id, kicker, title, intro, [(heading, text)...])
#   ("prose", id, kicker, title, [paragraphs])
#   ("callout", id, title, text)
# Facts here were checked in Nov 2026: Balady qualification for public health
# pest control; SFDA registration number on public health pesticide labels;
# ISO 9001:2026 published 16 Sep 2026 with an expected ~3-year transition.
# ---------------------------------------------------------------------------
EXTRA = {
("pest", "hub"): [
    ("table", "pests", "Know your pest", "Pests we deal with in {city}",
     "Most call-outs fall into six groups. The signs tell us what we are dealing with before treatment starts.",
     ["Pest", "Signs you may notice", "Why it matters", "How we treat it"],
     [
      ["Cockroaches", "Droppings like ground pepper, egg cases, a musty smell, sightings at night near drains and kitchens", "They contaminate food and surfaces, and are a hygiene finding in food premises", "Gel baits in hiding places, targeted residual treatment, drain treatment, then a follow-up visit"],
      ["Termites", "Mud tubes on walls or skirting, hollow-sounding wood, discarded wings, doors that start to stick", "Damage to door frames, cabinets and structural timber that is costly to repair", "Soil barrier treatment before or after construction, baiting, and wood treatment"],
      ["Rats and mice", "Droppings, gnaw marks, greasy rub marks along walls, scratching sounds at night", "They contaminate stock and damage cables and packaging", "Proofing of entry points, tamper-resistant bait stations, traps and monitoring"],
      ["Bed bugs", "Bites in lines or clusters, small blood spots on sheets, dark spots along mattress seams", "They spread between rooms quickly, which is serious for hotels and staff housing", "Detailed inspection, treatment of beds and furniture, and a follow-up after the egg cycle"],
      ["Ants and flies", "Trails leading to food, flies around waste areas and drains", "Nuisance and food contamination", "Baiting, removing the source, and fly control units for commercial kitchens"],
      ["Stored-product insects", "Beetles, moths or webbing in grain, flour, dates or packaged goods", "Stock loss and rejected consignments", "Inspection, stock rotation advice, and fumigation where needed"],
     ], None),
    ("cards", "who", "Who we work for", "Homes and businesses need different things", None,
     [
      ("Homes and villas", "One-off or seasonal treatments, planned around children, pets and food areas, with clear preparation instructions before we arrive."),
      ("Restaurants and food businesses", "Scheduled visits, monitoring points and service records that a municipal inspector or food-safety auditor can read."),
      ("Warehouses and logistics", "Rodent monitoring, stored-product pest control and fumigation, planned around receiving and dispatch."),
      ("Hotels, compounds and healthcare", "Room-by-room programmes, discreet service and a fast response when a guest or resident reports a problem."),
     ]),
    ("list", "price", "Pricing", "What affects the price",
     "We quote in writing after the inspection, so you know the scope and cost before any work starts. The quotation depends on:",
     ["The size and type of property", "The pest, and how established the infestation is", "How many visits the treatment needs", "Whether it is a one-off treatment or a service contract", "Access and timing, such as night or out-of-hours work"]),
    ("list", "prepare", "Before and after", "How to prepare for a treatment",
     "A little preparation makes treatment more effective. We confirm the exact steps for your site when you book.",
     ["Tell us about children, pets, fish tanks, pregnancy or respiratory conditions in the household", "Clear the areas to be treated: under sinks, kitchen cupboards, storage rooms", "Cover or put away food, utensils and children's toys", "Keep people and pets out of treated rooms for the period we advise", "Afterwards, ventilate as instructed and avoid mopping treated edges for the period we advise", "Keep the service report: it lists what was used and where"]),
    ("callout", "licence", "Check your provider's licence",
     "In Saudi Arabia, a company offering public health pest control needs a qualification issued through the Balady municipal platform. Public health pesticides also carry an SFDA registration number on the label. Ask any provider to show you both before work starts.{pest_licence_line}"),
],
("pest", "termite-control"): [
    ("list", "signs", "Early warning", "Signs of termites in a building",
     "Termites stay hidden, so the signs are easy to miss. Call for an inspection if you see any of these:",
     ["Mud tubes, the width of a pencil, on walls, skirting or foundations", "Wood that sounds hollow when tapped", "Blistered paint or a rippled surface on door frames and cabinets", "Small piles of discarded wings near windows or lights", "Doors or windows that begin to stick", "Fine soil or mud packed into joints and cracks"]),
    ("prose", "how", "How it happens", "How termites get into buildings",
     ["The termites that damage buildings here are mainly subterranean. They nest in the soil and travel to timber through cracks in the floor slab, expansion joints, and gaps around pipes and cable conduits.",
      "They build mud tubes to stay protected from dry air and light, which is why the damage is often well advanced before anyone sees an insect. Door frames, skirting, wardrobes and kitchen cabinets are usually attacked first.",
      "Because the colony is in the ground, spraying the visible insects does not solve the problem. Treatment has to put a treated zone between the soil and the building, or eliminate the colony through baiting."]),
    ("table", "methods", "Treatment options", "Which termite treatment is right for your building",
     "We recommend a method after the inspection. These are the main options.",
     ["Method", "When it is used", "How it works", "Disruption"],
     [
      ["Pre-construction soil treatment", "New buildings, before the floor slab is poured", "Termiticide is applied to the compacted soil under and around the foundations to form a treated zone", "None for occupants. It has to be scheduled with the contractor"],
      ["Post-construction barrier (drill and inject)", "Existing buildings with termite activity, or at risk", "Small holes are drilled along walls and floor joints, termiticide is injected into the soil beneath, and the holes are sealed", "Low. Rooms stay in use; some furniture is moved"],
      ["Baiting system", "Where drilling is not suitable, or for long-term monitoring", "Stations are placed around the building. Termites feed on the bait and carry it back to the colony", "Minimal. It works over weeks to months"],
      ["Wood and joinery treatment", "Affected frames, cabinets and timber", "Infested wood is treated directly or replaced", "Limited to the affected item"],
     ], None),
    ("cards", "contractors", "For developers and contractors", "Pre-construction anti-termite treatment", None,
     [
      ("Timing", "Soil treatment is applied after final compaction and before the vapour barrier and slab. Tell us your pour dates early so it does not hold up the programme."),
      ("Perimeter", "The external perimeter is treated after backfilling and final grading, so the treated zone is not disturbed by later earthworks."),
      ("Handover records", "You receive a treatment record for the project file, stating the areas treated, the product and the quantity applied."),
     ]),
    ("list", "price", "Pricing", "What affects the price of termite treatment",
     "We measure the building at the inspection and quote in writing. The price depends on:",
     ["The treated area or the length of walls to be treated", "Construction type and floor finishes", "How far the activity has spread", "The method: barrier, baiting or both", "The warranty period you ask for"]),
    ("callout", "writing", "Ask for it in writing",
     "Before you agree to any termite treatment, ask for the product name and its registration number, the areas to be treated, the quantity to be applied, and the warranty terms. A reputable provider gives you all four."),
],
("iso", "hub"): [
    ("table", "which", "Start here", "Which ISO standard do you need?",
     "The right standard depends on your industry and on what your customers and tenders ask for.",
     ["Standard", "What it covers", "Who usually needs it"],
     [
      ["ISO 9001 Quality", "Consistent delivery and customer satisfaction", "Almost any company. Commonly requested in tenders and supplier approvals"],
      ["ISO 22000 Food safety", "Control of food-safety hazards across the food chain, including HACCP principles", "Food manufacturers, caterers, central kitchens, packers and cold stores"],
      ["ISO 45001 Health and safety", "Workplace hazards, incident prevention and legal compliance", "Contractors, factories, and facility and maintenance companies"],
      ["ISO 14001 Environment", "Waste, emissions, resource use and compliance obligations", "Manufacturers, contractors, and suppliers to clients with environmental requirements"],
      ["ISO 27001 Information security", "Risk assessment and controls to protect information", "IT, software, finance and outsourcing firms, and any company that handles client data"],
     ], "Many companies combine two or three standards in one integrated management system, which reduces duplicated documents and audit days."),
    ("callout", "new9001", "ISO 9001:2026 has been published",
     "The new edition of ISO 9001 was published in September 2026. A transition period of about three years is expected, during which existing ISO 9001:2015 certificates remain valid. If you are starting now, we agree with you and your certification body which edition to implement."),
    ("cards", "roles", "Who does what", "Consultant, certification body, accreditation body", None,
     [
      ("We are the consultant", "We run the gap analysis, build the system with your team, train your staff, carry out the internal audit and prepare you for the certification audit."),
      ("The certification body audits you", "An independent body audits in two stages: Stage 1 checks your documentation and readiness, Stage 2 checks that the system is working. It issues the certificate."),
      ("The accreditation body checks the certifier", "A credible certificate comes from a certification body accredited by a recognised accreditation body, such as the Saudi Accreditation Center or the GCC Accreditation Center."),
      ("After certification", "The certificate normally runs for three years, with surveillance audits each year and a recertification audit at the end. We can support those too."),
     ]),
    ("table", "timeline", "Timeline", "How long ISO certification takes",
     "Most small and mid-sized companies take three to six months. It depends on your size, the number of sites, and how much is already in place.",
     ["Phase", "What happens", "Typical duration"],
     [
      ["Gap analysis", "We compare your current practice with the standard and agree a plan", "1 to 2 weeks"],
      ["Design and documentation", "Policies, process maps, procedures and forms are written with your team", "4 to 8 weeks"],
      ["Implementation and training", "The system is put into use and staff are trained", "4 to 8 weeks"],
      ["Internal audit and management review", "We audit the system, you fix the findings, management reviews the results", "2 to 3 weeks"],
      ["Certification audit", "The certification body carries out Stage 1 and Stage 2", "2 to 4 weeks, by its schedule"],
     ], "Durations are typical, not a commitment. We give you a dated plan after the gap analysis."),
    ("list", "cost", "Cost", "What ISO certification costs",
     "There are two separate costs, plus the ongoing ones. We give a fixed written quotation for our part after the free consultation.",
     ["Consultancy fee: depends on the standard, number of sites, headcount, and how much you already have in place", "Certification body fee: based on audit days, which are set by headcount, sites and the risk level of your activity", "Annual surveillance audits by the certification body", "A recertification audit every three years", "Your own staff time to run the system"]),
    ("list", "credible", "Buyer's guide", "How to avoid a worthless certificate",
     "Certificates from non-accredited bodies are often rejected in tenders. Before you pay anyone, check:",
     ["The certification body is accredited, and the accreditation covers the standard and your sector", "The certificate can be verified on the certification body's public register", "A real audit takes place, on site or remote, with an audit report", "Nobody is promising a certificate within days or a guaranteed pass", "The consultant and the certification body are separate organisations"]),
],
("iso", "iso-9001"): [
    ("callout", "new9001", "ISO 9001:2026 has been published",
     "The new edition was published in September 2026, replacing ISO 9001:2015. A transition period of about three years is expected, during which 2015 certificates remain valid. New to ISO 9001? We agree the edition with your certification body before work starts. Already certified? We can run a gap analysis against the new edition."),
    ("table", "clauses", "Inside the standard", "What ISO 9001 requires, clause by clause",
     "The requirements sit in clauses 4 to 10. This is what each asks for and what we produce with you.",
     ["Clause", "What the standard asks for", "What we do with you"],
     [
      ["4. Context of the organisation", "Understand your business and interested parties; define the scope and processes", "Scope statement, process map, interested-party register"],
      ["5. Leadership", "Top management commitment, a quality policy, clear roles", "Quality policy, responsibilities matrix, management briefing"],
      ["6. Planning", "Risks and opportunities, quality objectives, planning of changes", "Risk register, measurable objectives with owners and dates"],
      ["7. Support", "People, infrastructure, competence, awareness and documented information", "Training matrix, document control, calibration and maintenance records"],
      ["8. Operation", "Sales, design where applicable, purchasing, delivery, and control of nonconforming output", "Procedures and forms for your core processes, supplier evaluation"],
      ["9. Performance evaluation", "Monitoring, customer satisfaction, internal audit and management review", "KPIs, internal audit programme and report, management review minutes"],
      ["10. Improvement", "Nonconformity, corrective action and continual improvement", "Corrective action log and a root-cause method your team can use"],
     ], "Clause numbers follow the harmonised structure shared by ISO management system standards, so the same framework carries over to ISO 14001, 45001 and 22000."),
    ("list", "documents", "Deliverables", "What you will have at the end",
     "A working system, not a shelf of binders. Typical documents and records:",
     ["Scope of the quality management system", "Quality policy and measurable objectives", "Process map and process descriptions", "Risk and opportunity register", "Procedures and forms for core processes", "Training and competence records", "Supplier evaluation records", "Internal audit report", "Management review minutes", "Corrective action log"]),
    ("table", "audits", "The audit", "What happens at the certification audit",
     "The certification body, not the consultant, carries out these audits.",
     ["Audit", "Purpose", "When"],
     [
      ["Stage 1", "Reviews your documentation and checks you are ready for Stage 2", "Once the system is documented and running"],
      ["Stage 2", "Checks the system is implemented and effective, by interviewing staff and sampling records", "Usually a few weeks after Stage 1"],
      ["Surveillance", "Confirms the system is being maintained", "Normally once a year"],
      ["Recertification", "A full review to renew the certificate", "Every three years"],
     ], None),
    ("list", "fails", "Avoid these", "Common reasons companies get nonconformities",
     "We see the same gaps repeatedly. The internal audit we run before certification is designed to catch them.",
     ["No internal audit was completed before the certification audit", "Management review was not held, or not recorded", "Quality objectives are not measurable", "Documents in use are out of date or uncontrolled", "Suppliers are not evaluated", "Calibration records are missing for measuring equipment", "Corrective actions are closed without a root cause", "Staff cannot explain the quality policy or their role in it"]),
],
}

MORE_FAQS = {
("pest", "hub"): [
    ("How long does a treatment take?", "A typical apartment or villa treatment takes one to two hours. Larger sites and termite work take longer. We confirm the time when we quote."),
    ("How soon can we use the rooms again?", "It depends on the product and method. We tell you the re-entry time for each area before we start, and it is written on the service report."),
    ("Do you offer contracts for restaurants and warehouses?", "Yes. Contracts include scheduled visits, monitoring points and a service report after every visit."),
    ("Will one treatment be enough?", "For some pests, yes. Cockroaches, bed bugs and rodents usually need a follow-up visit because eggs hatch or new activity appears. We tell you what to expect in the quotation."),
],
("pest", "termite-control"): [
    ("Is drilling through my floor tiles noticeable?", "Holes are small, placed along joints where possible, and sealed with matching material after injection."),
    ("Do I need to move out during treatment?", "Usually not. Rooms stay in use and we tell you if any area needs to be vacated for a short time."),
    ("How long does protection last?", "It depends on the product, the soil and the method. The warranty period is stated in the quotation, so ask to see it in writing."),
    ("Is baiting better than a chemical barrier?", "They do different jobs. A barrier protects the building quickly; baiting targets the colony and suits sites where drilling is not possible. We sometimes recommend both."),
],
("iso", "hub"): [
    ("Can you guarantee we will be certified?", "No honest consultant can, because the decision belongs to the independent certification body. What we do is prepare you thoroughly and stay with you through the audit and any findings."),
    ("Can small companies get certified?", "Yes. The standards apply to organisations of any size, and a small company's system can be short and simple."),
    ("Can we combine several standards?", "Yes. ISO 9001, 14001 and 45001 share the same structure, so they are often implemented together as one integrated system."),
    ("Do you provide training?", "Yes. Awareness training for staff and internal auditor training are part of most projects."),
],
("iso", "iso-9001"): [
    ("Should we certify to the 2015 or the 2026 edition?", "It depends on your timing and your certification body. We check the current transition rules with them at the start so you do not have to redo work."),
    ("We are already certified to ISO 9001:2015. What should we do?", "Your certificate remains valid during the transition period. Plan a gap analysis against the 2026 edition and update the system ahead of a scheduled audit."),
    ("How many staff need to be involved?", "A management representative and the owners of your main processes. We keep their time to short working sessions."),
    ("Does ISO 9001 require a quality manual?", "A manual is not mandatory, but you do need documented information that describes your system. Many companies keep a short manual because customers ask for it."),
    ("Can the audit be done remotely?", "Certification bodies can audit some activities remotely, depending on their rules and your operations. They decide, not the consultant."),
],
}
