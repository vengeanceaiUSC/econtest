#!/usr/bin/env python3
"""Generate focused practice-set PDFs — one file per category with exact question counts."""

import os
import re
import pymupdf

UPLOADS = "/home/ubuntu/.cursor/projects/workspace/uploads"
OUT_DIR = "/workspace/exam_prep_images"
PDF_OUT_DIR = "/workspace/practice_sets"

PDFS = {
    "HW1": f"{UPLOADS}/Homework_1__Chapter_4__9bce.pdf",
    "HW2": f"{UPLOADS}/Homework_2__Chapter_9__b189.pdf",
    "S4": f"{UPLOADS}/SampleQuestionsChapter04ConsumerTheory_a895.pdf",
    "S9": f"{UPLOADS}/SampleQuestionsChapter09Uncertainty_4bdd.pdf",
    "MOCK": f"{UPLOADS}/Mock_Midterm_1_129f.pdf",
}

DPI = 132
JPEG_QUALITY = 78
PW, PH = 612, 792
COLOR = (0.12, 0.31, 0.47)
MUTED = (0.45, 0.45, 0.45)

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(PDF_OUT_DIR, exist_ok=True)

STUDY_SETS = [
    {"slug": "01_Consumer_Problems", "ch": 4, "category": "Consumer Problems", "count": 2, "ids": [1, 2]},
    {"slug": "02_Labor_Leisure", "ch": 4, "category": "Labor-Leisure", "count": 2, "ids": [3, 4]},
    {"slug": "03_Intertemporal_Consumption", "ch": 4, "category": "Intertemporal Consumption", "count": 2, "ids": [5, 6]},
    {"slug": "04_Elasticity_Types_of_Goods", "ch": 4, "category": "Elasticity / Types of Goods", "count": 3, "ids": [7, 8, 9]},
    {"slug": "05_Budget_Line", "ch": 4, "category": "Budget Line", "count": 1, "ids": [10]},
    {"slug": "06_Assumptions_Preferences", "ch": 4, "category": "Assumptions / Preferences", "count": 2, "ids": [11, 12]},
    {"slug": "07_Insurance_Problems", "ch": 9, "category": "Insurance Problems", "count": 5, "ids": [13, 14, 15, 16, 17]},
    {"slug": "08_Risk_Attitudes", "ch": 9, "category": "Risk Attitudes", "count": 4, "ids": [18, 19, 20, 21]},
    {"slug": "09_Certainty_Equivalent_Risk_Premium", "ch": 9, "category": "Certainty Equivalent & Risk Premium", "count": 2, "ids": [22, 23]},
    {"slug": "10_Diversification", "ch": 9, "category": "Diversification", "count": 1, "ids": [24]},
]

QUESTION_INFO = {
    1: ("Consumer Problem #1", "HW1 Ex 3"),
    2: ("Consumer Problem #2", "Sample Q26"),
    3: ("Labor-Leisure #1", "Course-style"),
    4: ("Labor-Leisure #2", "Course-style"),
    5: ("Intertemporal #1", "Sample Q41"),
    6: ("Intertemporal #2", "Mock Q24-25"),
    7: ("Elasticity #1", "HW1 Ex 4"),
    8: ("Elasticity #2", "Sample Q39"),
    9: ("Elasticity #3", "Sample Q38"),
    10: ("Budget Line", "Sample Q10"),
    11: ("Preferences #1", "HW1 Ex 2.2"),
    12: ("Preferences #2", "Sample Q8"),
    13: ("Insurance #1", "HW2 Ex 3"),
    14: ("Insurance #2", "HW2 Ex 3b"),
    15: ("Insurance #3", "Sample Q18"),
    16: ("Insurance #4", "Mock Q27"),
    17: ("Insurance #5", "Mock Q25-26"),
    18: ("Risk Attitudes #1", "HW2 Ex 2"),
    19: ("Risk Attitudes #2", "Sample Q6"),
    20: ("Risk Attitudes #3", "Sample Q8"),
    21: ("Risk Attitudes #4", "Mock Q28"),
    22: ("CE & RP #1", "HW2 Ex 1"),
    23: ("CE & RP #2", "Sample Q12"),
    24: ("Diversification", "Sample Q22"),
}

FORMULA_CH4 = [
    "Budget: p1*q1 + p2*q2 = I  |  Slope = -p1/p2",
    "Optimum: MRS = MU1/MU2 = p1/p2",
    "Cobb-Douglas: q1* = [a/(a+b)]*I/p1",
    "Labor-Leisure: c = wL + V; MU_l/MU_c = w",
    "Intertemporal: c1 + c2/(1+r) = I1 + I2/(1+r)",
    "IT optimum: MU1/MU2 = 1+r",
    "Price elasticity: Ep = (P/Q)(dQ/dP)",
    "Income elasticity: EI = (I/Q)(dQ/dI)",
    "Cross-price: Exy = (Py/Qx)(dQx/dPy)",
]

FORMULA_CH9 = [
    "E[x] = sum(pi * xi)",
    "E[u] = sum(pi * u(xi))",
    "Risk averse: u'' < 0  |  neutral: u''=0  |  loving: u''>0",
    "Certainty equivalent: u(CE) = E[u]",
    "Risk premium: RP = E[x] - CE",
    "Fair bet: E[payoff] = 0",
    "Fair insurance: P_fair = E[loss]",
    "Max premium: E[u with ins] = E[u no ins]",
    "Insurance RP: P_max - P_fair",
    "Diversify: negative correlation lowers variance",
]


def validate_counts():
    total = sum(s["count"] for s in STUDY_SETS)
    assert total == 24, f"Expected 24 questions, got {total}"
    ch4 = sum(s["count"] for s in STUDY_SETS if s["ch"] == 4)
    ch9 = sum(s["count"] for s in STUDY_SETS if s["ch"] == 9)
    assert ch4 == 12 and ch9 == 12
    for i, s in enumerate(STUDY_SETS, 1):
        assert len(s["ids"]) == s["count"], f"Set {i} count mismatch: {s['count']} vs {len(s['ids'])}"


def render_page(pdf_key, page_1based, tag=""):
    doc = pymupdf.open(PDFS[pdf_key])
    page = doc[page_1based - 1]
    mat = pymupdf.Matrix(DPI / 72, DPI / 72)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    path = os.path.join(OUT_DIR, f"q{tag}_{pdf_key}_p{page_1based}.jpg")
    pix.save(path, jpg_quality=JPEG_QUALITY)
    return path


def render_crop(pdf_key, page_1based, y0, y1, tag=""):
    doc = pymupdf.open(PDFS[pdf_key])
    page = doc[page_1based - 1]
    if y1 is None:
        y1 = page.rect.height
    y0, y1 = max(0, y0 - 6), min(page.rect.height, y1)
    if y1 - y0 < 20:
        return render_page(pdf_key, page_1based, tag)
    mat = pymupdf.Matrix(DPI / 72, DPI / 72)
    pix = page.get_pixmap(matrix=mat, clip=pymupdf.Rect(0, y0, page.rect.width, y1), alpha=False)
    path = os.path.join(OUT_DIR, f"q{tag}_crop.jpg")
    pix.save(path, jpg_quality=JPEG_QUALITY)
    return path


def y_of(pdf_key, page, label):
    hits = pymupdf.open(PDFS[pdf_key])[page - 1].search_for(label)
    return hits[0].y0 if hits else None


def hw_crop(pdf_key, page, start, end, tag):
    doc = pymupdf.open(PDFS[pdf_key])
    pg = doc[page - 1]
    y0 = y_of(pdf_key, page, start)
    if y0 is None:
        return [render_page(pdf_key, page, tag)]
    y1 = y_of(pdf_key, page, end) if end else pg.rect.height
    if end and (y1 is None or y1 <= y0):
        y1 = pg.rect.height
    return [render_crop(pdf_key, page, y0, y1, tag)]


def images_for(qnum):
    m = {
        1: lambda: hw_crop("HW1", 1, "Exercise 3", None, qnum),
        2: lambda: [render_page("S4", 8, qnum)],
        3: lambda: [("text", ["Maria: 16 hrs/day, w=$20, V=$80, U=c^0.5 l^0.5. Find l*, L*, c*.", "(Course-style)"])],
        4: lambda: [("text", ["Same setup, w=$30. Find l*, L*, c*. More or less work?"])],
        5: lambda: [render_page("S4", 11, qnum), render_page("S4", 12, f"{qnum}b")],
        6: lambda: [render_page("MOCK", 5, qnum)],
        7: lambda: hw_crop("HW1", 2, "Exercise 4", "Exercise 5", qnum),
        8: lambda: [render_page("S4", 11, qnum)],
        9: lambda: [render_page("S4", 11, f"{qnum}a")],
        10: lambda: [render_page("S4", 3, qnum)],
        11: lambda: hw_crop("HW1", 1, "Exercise 2", "Exercise 3", qnum),
        12: lambda: [render_page("S4", 3, f"{qnum}a")],
        13: lambda: [render_page("HW2", 2, qnum)],
        14: lambda: [render_page("HW2", 2, f"{qnum}a")],
        15: lambda: [render_page("S9", 6, qnum)],
        16: lambda: [render_page("MOCK", 10, qnum)],
        17: lambda: [render_page("MOCK", 9, qnum)],
        18: lambda: hw_crop("HW2", 1, "Exercise 2", None, qnum),
        19: lambda: [render_page("S9", 2, qnum)],
        20: lambda: [render_page("S9", 3, qnum), render_page("S9", 4, f"{qnum}b")],
        21: lambda: [render_page("MOCK", 11, qnum)],
        22: lambda: hw_crop("HW2", 1, "Exercise 1", "Exercise 2", qnum),
        23: lambda: [render_page("S9", 5, qnum)],
        24: lambda: [render_page("S9", 7, qnum), render_page("S9", 8, f"{qnum}b")],
    }
    return m[qnum]()


def cover_page(out, set_num, study_set):
    p = out.new_page(width=PW, height=PH)
    p.insert_text((72, 120), "ECON 351 — Focused Practice Set", fontsize=20, fontname="helv")
    p.insert_text((72, 160), f"Set {set_num} of 10", fontsize=12, fontname="helv", color=MUTED)
    p.insert_text((72, 210), f"Chapter {study_set['ch']}", fontsize=22, fontname="helv", color=COLOR)
    p.insert_text((72, 250), study_set["category"], fontsize=18, fontname="helv", color=COLOR)
    n = study_set["count"]
    p.insert_text((72, 300), f"{n} question{'s' if n != 1 else ''} in this practice set", fontsize=14, fontname="helv")
    ids = ", ".join(f"Q{i}" for i in study_set["ids"])
    p.insert_text((72, 330), f"Questions: {ids}", fontsize=11, fontname="helv", color=MUTED)
    p.insert_text((72, 380), "Screenshots from original HW, sample questions, and mock midterm.", fontsize=10, fontname="helv", color=MUTED)
    return p


def place_image_on_page(p, img_path, y_start, margin=36):
    pix = pymupdf.open(img_path)[0].get_pixmap(alpha=False)
    scale = min((PW - 2 * margin) / pix.width, (PH - y_start - margin) / pix.height)
    w, h = pix.width * scale, pix.height * scale
    p.insert_image(pymupdf.Rect(margin, y_start, margin + w, y_start + h), filename=img_path)
    return y_start + h + 12


def add_question(out, study_set, set_num, qid, idx):
    label, source = QUESTION_INFO[qid]
    items = images_for(qid)
    p = out.new_page(width=PW, height=PH)
    p.insert_text((40, 42), f"Set {set_num}: {study_set['category']}", fontsize=10, fontname="helv", color=COLOR)
    p.insert_text((40, 58), f"Question {idx} of {study_set['count']}  (Practice Q{qid})", fontsize=13, fontname="helv")
    p.insert_text((40, 74), f"{label} — {source}", fontsize=9, fontname="helv", color=MUTED)
    y = 92
    img_i = 0
    for item in items:
        if isinstance(item, tuple) and item[0] == "text":
            for line in item[1]:
                p.insert_text((40, y), line, fontsize=11, fontname="helv")
                y += 15
        elif isinstance(item, str) and os.path.exists(item):
            if y > PH - 120:
                p = out.new_page(width=PW, height=PH)
                p.insert_text((40, 42), f"Practice Q{qid} — continued", fontsize=10, fontname="helv", color=MUTED)
                y = 60
            y = place_image_on_page(p, item, y)
            img_i += 1


def build_study_set_pdf(study_set, set_num):
    out = pymupdf.open()
    cover_page(out, set_num, study_set)
    for idx, qid in enumerate(study_set["ids"], 1):
        add_question(out, study_set, set_num, qid, idx)
    path = os.path.join(PDF_OUT_DIR, f"{study_set['slug']}.pdf")
    out.save(path, garbage=4, deflate=True)
    expected_pages = 1 + study_set["count"]  # cover + one page per question (min)
    print(f"  {study_set['slug']}.pdf — {study_set['count']} Q, {len(out)} pages")
    return path, len(out)


def build_chapter_pdf(chapter):
    sets = [s for s in STUDY_SETS if s["ch"] == chapter]
    out = pymupdf.open()
    p = out.new_page(width=PW, height=PH)
    total = sum(s["count"] for s in sets)
    p.insert_text((72, 140), f"ECON 351 — Chapter {chapter} Practice Set", fontsize=22, fontname="helv")
    p.insert_text((72, 180), f"{total} questions total", fontsize=14, fontname="helv")
    y = 220
    for i, s in enumerate(sets, 1):
        global_set = STUDY_SETS.index(s) + 1
        line = f"Set {global_set}: {s['category']} ({s['count']})"
        p.insert_text((72, y), line, fontsize=11, fontname="helv")
        y += 16
    set_num = 0
    for s in sets:
        set_num = STUDY_SETS.index(s) + 1
        p = out.new_page(width=PW, height=PH)
        p.insert_text((72, 300), s["category"], fontsize=18, fontname="helv", color=COLOR)
        p.insert_text((72, 330), f"{s['count']} question{'s' if s['count'] != 1 else ''}", fontsize=12, fontname="helv")
        for idx, qid in enumerate(s["ids"], 1):
            add_question(out, s, set_num, qid, idx)
    path = os.path.join(PDF_OUT_DIR, f"Chapter_{chapter}_All_{total}_Questions.pdf")
    out.save(path, garbage=4, deflate=True)
    print(f"  Chapter_{chapter}_All_{total}_Questions.pdf — {total} Q, {len(out)} pages")
    return path


def build_formula_pdf():
    out = pymupdf.open()
    p = out.new_page(width=PW, height=PH)
    p.insert_text((40, 40), "ONE-PAGE FORMULA SHEET", fontsize=16, fontname="helv", color=COLOR)
    y = 70
    p.insert_text((40, y), "CHAPTER 4 — Consumer Theory", fontsize=12, fontname="helv", color=COLOR)
    y += 20
    for line in FORMULA_CH4:
        p.insert_text((40, y), line, fontsize=9, fontname="helv")
        y += 13
    y += 10
    p.insert_text((40, y), "CHAPTER 9 — Uncertainty & Risk", fontsize=12, fontname="helv", color=COLOR)
    y += 20
    for line in FORMULA_CH9:
        p.insert_text((40, y), line, fontsize=9, fontname="helv")
        y += 13
    path = os.path.join(PDF_OUT_DIR, "Formula_Sheet.pdf")
    out.save(path, garbage=4, deflate=True)
    print(f"  Formula_Sheet.pdf — 1 page")
    return path


def build_manifest():
    lines = [
        "ECON 351 — 24-Question Focused Study Set",
        "=" * 50,
        "",
        "Each PDF below has EXACTLY the question count for that category.",
        "",
        "CHAPTER 4 (12 questions total)",
        "  01_Consumer_Problems.pdf              2 questions",
        "  02_Labor_Leisure.pdf                  2 questions",
        "  03_Intertemporal_Consumption.pdf      2 questions",
        "  04_Elasticity_Types_of_Goods.pdf      3 questions",
        "  05_Budget_Line.pdf                    1 question",
        "  06_Assumptions_Preferences.pdf        2 questions",
        "  Chapter_4_All_12_Questions.pdf       12 questions (all Ch.4 sets)",
        "",
        "CHAPTER 9 (12 questions total)",
        "  07_Insurance_Problems.pdf             5 questions",
        "  08_Risk_Attitudes.pdf                 4 questions",
        "  09_Certainty_Equivalent_Risk_Premium.pdf  2 questions",
        "  10_Diversification.pdf                1 question",
        "  Chapter_9_All_12_Questions.pdf       12 questions (all Ch.9 sets)",
        "",
        "REFERENCE",
        "  Formula_Sheet.pdf                     1 page",
        "",
        "GRAND TOTAL: 24 practice questions across 10 category sets",
    ]
    path = os.path.join(PDF_OUT_DIR, "README.txt")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path


def build_all():
    validate_counts()
    print("Building category practice PDFs (exact counts per type):")
    built = []
    for i, s in enumerate(STUDY_SETS, 1):
        path, pages = build_study_set_pdf(s, i)
        built.append((s["slug"], s["count"], pages))
    print("\nBuilding chapter combined PDFs:")
    build_chapter_pdf(4)
    build_chapter_pdf(9)
    build_formula_pdf()
    build_manifest()
    total_q = sum(c for _, c, _ in built)
    print(f"\nDone: {len(built)} category PDFs, {total_q} questions, output in {PDF_OUT_DIR}/")


if __name__ == "__main__":
    build_all()
