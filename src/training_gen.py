"""Template for per-standard training pages. No prices anywhere: customers request a quote."""


def make(S, d):
    """S: shared strings for one language. d: data for one standard. Returns (page_dict, blocks, faqs)."""
    page = dict(
        title=d["title"], desc=d["desc"], h1=d["h1"], lead=d["lead"], service=d["service"], intro=d["intro"],
        bullets=d["bullets"], steps=S["steps"], faqs=d["faqs"], cta="quote", no_notice=True, plink=False, art="train",
        inc_kicker=S["inc_kicker"], inc_title=S["inc_title"], trust=S["trust"],
    )
    std = d["std"]
    blocks = [
        ("cards", "ladder", S["ladder_k"], S["ladder_t"].format(std=std), S["ladder_intro"], d["ladder"]),
        ("table", "who", S["who_k"], S["who_t"], S["who_intro"], S["who_head"], d["who"], None),
        ("table", "content", S["content_k"], S["content_t"], S["content_intro"], S["content_head"], d["content"], S["content_note"]),
        ("list", "outcomes", S["outcomes_k"], S["outcomes_t"], S["outcomes_intro"], d["outcomes"]),
        ("cards", "delivery", S["delivery_k"], S["delivery_t"], None, S["delivery"]),
        ("list", "receive", S["receive_k"], S["receive_t"], S["receive_intro"], S["receive_items"]),
        ("list", "before", S["before_k"], S["before_t"], S["before_intro"], d["before"]),
        ("callout", "quote", S["quote_t"], S["quote_p"]),
    ]
    return page, blocks


SHARED_EN = dict(
    steps=[("Enquire", "Tell us the course, the number of people, your preferred dates and the location."),
           ("Agree the plan", "We confirm the format, language, venue and schedule in writing."),
           ("Attend the course", "Interactive sessions with exercises that use your own examples."),
           ("Certificate and follow-up", "Attendance certificates, course materials, and answers to follow-up questions.")],
    inc_kicker="Overview", inc_title="What the training covers",
    trust=["Request a quote", "Courses at your premises or ours", "Attendance certificates", "Serving Riyadh and Jeddah"],
    ladder_k="Course path", ladder_t="Courses in the {std} training path",
    ladder_intro="Choose the level that matches each person's role. We can combine levels in one programme for your team.",
    who_k="Who should attend", who_t="The right course for each role", who_intro="Most companies train several groups. This is how roles usually map to courses.",
    who_head=["Role", "Recommended course", "Why"],
    content_k="Course content", content_t="What each course covers", content_intro="Each course combines explanation with exercises, so people practise on realistic examples.",
    content_head=["Course", "Main topics", "Practical work"], content_note="Course content is adapted to your sector and to the documents you already use.",
    outcomes_k="Learning outcomes", outcomes_t="What participants will be able to do", outcomes_intro="By the end of the training, participants should be able to:",
    delivery_k="Ways to attend", delivery_t="Choose how the training is delivered",
    delivery=[("At your premises", "We come to your site in Riyadh or Jeddah and use your own procedures and records for the exercises."),
              ("At a venue we arrange", "For smaller groups or several companies, we arrange a training room in Riyadh or Jeddah."),
              ("Live online", "Available on request for courses that suit it. Ask us which formats work for the course you need."),
              ("Language", "Tell us the language your team needs when you enquire, and we will confirm what we can deliver.")],
    receive_k="What you receive", receive_t="Every participant receives", receive_intro="Each participant and the company receive:",
    receive_items=["Course materials", "A certificate of attendance", "Practical exercises and worked examples", "Attendance and competence records for your audit file", "Answers to follow-up questions after the course"],
    before_k="Before you attend", before_t="Prerequisites", before_intro="Most people can start at the foundation level. For the other courses we recommend:",
    quote_t="Get a quote for your team", quote_p="Tell us the course, the number of people, your preferred dates and the location. We will send you a written quote.",
)
SHARED_AR = dict(
    steps=[("الاستفسار", "أخبرنا بالدورة وعدد المشاركين والمواعيد المفضلة والموقع."),
           ("الاتفاق على الخطة", "نؤكد كتابةً صيغة الدورة ولغتها ومكانها وجدولها."),
           ("حضور الدورة", "جلسات تفاعلية مع تمارين تستخدم أمثلتك أنت."),
           ("الشهادة والمتابعة", "شهادات حضور ومواد الدورة، وإجابات عن الأسئلة اللاحقة.")],
    inc_kicker="نظرة عامة", inc_title="ما الذي يغطيه التدريب",
    trust=["اطلب عرض سعر", "دورات في مقرّكم أو مقرّنا", "شهادات حضور", "نخدم الرياض وجدة"],
    ladder_k="مسار الدورات", ladder_t="دورات مسار التدريب على {std}",
    ladder_intro="اختر المستوى الذي يناسب دور كل شخص. ويمكننا الجمع بين المستويات في برنامج واحد لفريقك.",
    who_k="من يحضر", who_t="الدورة المناسبة لكل دور", who_intro="تدرّب معظم الشركات عدة مجموعات. وهكذا تتوزع الأدوار عادةً على الدورات.",
    who_head=["الدور", "الدورة الموصى بها", "السبب"],
    content_k="محتوى الدورات", content_t="ماذا تغطي كل دورة", content_intro="تجمع كل دورة بين الشرح والتمارين، فيتدرب المشاركون على أمثلة واقعية.",
    content_head=["الدورة", "الموضوعات الرئيسية", "العمل التطبيقي"], content_note="يُكيَّف محتوى الدورات لقطاعك وللوثائق التي تستخدمها أصلاً.",
    outcomes_k="مخرجات التعلم", outcomes_t="ما الذي سيستطيع المشاركون فعله", outcomes_intro="بنهاية التدريب ينبغي أن يكون المشاركون قادرين على:",
    delivery_k="طرق الحضور", delivery_t="اختر طريقة تقديم التدريب",
    delivery=[("في مقرّكم", "نحضر إلى موقعكم في الرياض أو جدة ونستخدم إجراءاتكم وسجلاتكم أنتم في التمارين."),
              ("في قاعة نرتّبها", "للمجموعات الأصغر أو عدة شركات، نرتب قاعة تدريب في الرياض أو جدة."),
              ("مباشر عبر الإنترنت", "متاح عند الطلب للدورات التي تناسبه. اسألنا عن الصيغ المناسبة للدورة التي تحتاجها."),
              ("اللغة", "أخبرنا باللغة التي يحتاجها فريقك عند الاستفسار وسنؤكد ما يمكننا تقديمه.")],
    receive_k="ما تتسلّمه", receive_t="يتسلّم كل مشارك", receive_intro="يتسلّم كل مشارك والشركة:",
    receive_items=["مواد الدورة", "شهادة حضور", "تمارين عملية وأمثلة محلولة", "سجلات الحضور والكفاءة لملف التدقيق لديك", "إجابات عن الأسئلة اللاحقة بعد الدورة"],
    before_k="قبل الحضور", before_t="المتطلبات المسبقة", before_intro="يستطيع معظم الناس البدء من المستوى التأسيسي. أما بقية الدورات فنوصي بما يلي:",
    quote_t="احصل على عرض سعر لفريقك", quote_p="أخبرنا بالدورة وعدد المشاركين والمواعيد المفضلة والموقع. وسنرسل لك عرض سعر مكتوباً.",
)
