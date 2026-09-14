#!/usr/bin/env python3
"""Generate full 24-question simulation practice tests matching the midterm format."""

import os
import textwrap
import pymupdf
from exam_config import EXAM_STRUCTURE, PRACTICE_TESTS, validate_exam_structure

UPLOADS = "/home/ubuntu/.cursor/projects/workspace/uploads"
OUT_DIR = "/workspace/exam_prep_images"
PDF_OUT_DIR = "/workspace/practice_tests"

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

def render_page(pdf_key, page_1based, tag=""):
    doc = pymupdf.open(PDFS[pdf_key])
    page = doc[page_1based - 1]
    mat = pymupdf.Matrix(DPI / 72, DPI / 72)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    path = os.path.join(OUT_DIR, f"{tag}_{pdf_key}_p{page_1based}.jpg")
    pix.save(path, jpg_quality=JPEG_QUALITY)
    return path


def render_crop(pdf_key, page_1based, y0, y1, tag=""):
    doc = pymupdf.open(PDFS[pdf_key])
    page = doc[page_1based - 1]
    return render_region_crop(pdf_key, page_1based, 0, page.rect.width, y0, y1, tag)


def render_region_crop(pdf_key, page_1based, x0, x1, y0, y1, tag=""):
    """Crop a rectangular region (supports two-column exam layouts)."""
    doc = pymupdf.open(PDFS[pdf_key])
    page = doc[page_1based - 1]
    if y1 is None:
        y1 = page.rect.height
    y0, y1 = max(0, y0 - 6), min(page.rect.height, y1)
    x0, x1 = max(0, x0), min(page.rect.width, x1)
    if y1 - y0 < 20 or x1 - x0 < 20:
        return render_page(pdf_key, page_1based, tag)
    mat = pymupdf.Matrix(DPI / 72, DPI / 72)
    pix = page.get_pixmap(matrix=mat, clip=pymupdf.Rect(x0, y0, x1, y1), alpha=False)
    path = os.path.join(OUT_DIR, f"{tag}_crop.jpg")
    pix.save(path, jpg_quality=JPEG_QUALITY)
    return path


def two_column_question(pdf_key, page, left_y0, end_label_right, tag, right_y0=70):
    """Crop a question that starts at the bottom-left and continues top-right (two-column PDF)."""
    doc = pymupdf.open(PDFS[pdf_key])
    pg = doc[page - 1]
    mid = pg.rect.width / 2
    right_y1 = pg.rect.height
    if end_label_right:
        hits = [h for h in pg.search_for(end_label_right) if h.x0 >= mid - 10]
        if hits:
            right_y1 = min(h.y0 for h in hits)
    return [
        render_region_crop(pdf_key, page, 0, mid, left_y0, None, f"{tag}_L"),
        render_region_crop(pdf_key, page, mid, pg.rect.width, right_y0, right_y1, f"{tag}_R"),
    ]


def sample_q22_shots(tag="Q054"):
    return two_column_question("S9", 7, left_y0=620, end_label_right="Question 23", tag=tag)


def mock_q29_shots(tag="Q055"):
    return two_column_question("MOCK", 11, left_y0=592, end_label_right="Question 30", tag=tag)


def column_crop(pdf_key, page, start, end, column, tag, y0_override=None, y1_override=None):
    """Crop a region in the left or right column of a two-column exam page."""
    doc = pymupdf.open(PDFS[pdf_key])
    pg = doc[page - 1]
    mid = pg.rect.width / 2
    y0 = y0_override if y0_override is not None else (y_of(pdf_key, page, start) if start else 0)
    if y0 is None:
        y0 = 0
    if y1_override is not None:
        y1 = y1_override
    elif end:
        y1 = y_of(pdf_key, page, end)
        if y1 is None or y1 <= y0:
            y1 = pg.rect.height
    else:
        y1 = pg.rect.height
    x0, x1 = (0, mid) if column == "L" else (mid, pg.rect.width)
    return render_region_crop(pdf_key, page, x0, x1, y0, y1, tag)


def sample_q6_shots(tag="Q006"):
    y7 = y_of("S4", 2, "Question 7")
    return [
        column_crop("S4", 2, "Question 6", None, "L", f"{tag}_L"),
        column_crop("S4", 2, None, None, "R", f"{tag}_R", y0_override=70, y1_override=y7),
    ]


def sample_q9_shots(tag="Q009"):
    y10 = y_of("S4", 3, "Question 10")
    return two_column_question("S4", 3, left_y0=620, end_label_right="Question 10", tag=tag)


def sample_q31_shots(tag="Q031"):
    y32 = y_of("S4", 9, "Question 32")
    return [
        column_crop("S4", 9, "Question 31", None, "L", f"{tag}_L"),
        column_crop("S4", 9, None, None, "R", f"{tag}_R", y0_override=70, y1_override=y32),
    ]


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


def pdf_crop(pdf_key, page, start, end, tag):
    """Crop a labeled question region; include setup pages when a question says 'from previous'."""
    return hw_crop(pdf_key, page, start, end, tag)


def tom_insurance_setup(tag="tom_setup"):
    """Sample Ch.9 Q15 — Tom's house/insurance setup (needed for Q16–Q17)."""
    return pdf_crop("S9", 5, "Question 15", "Question 16", tag)


def merge_images(*parts):
    """Combine multiple crop callables into one images_for entry."""
    def fn():
        out = []
        for part in parts:
            if callable(part):
                out.extend(part())
            else:
                out.extend(part)
        return out
    return fn


def bank_images_map():
    return {
        "Q001": [("text", ["Jackie: 'Knives Out' vs 'Top Gun Maverick.' She doesn't care which. Violation?", "HW1 Ex 2.1"])],
        "Q002": lambda: hw_crop("HW1", 1, "Exercise 2", "Exercise 3", "Q002"),
        "Q003": [("text", ["Parasite > Indiana Jones > Jurassic Park, but Jurassic Park > Parasite. Violation?", "HW1 Ex 2.3"])],
        "Q004": [render_page("S4", 2, "Q004")],
        "Q005": [render_page("S4", 3, "Q005")],
        "Q007": [render_page("S4", 2, "Q007")],
        "Q008": [render_page("S4", 3, "Q008")],
        "Q009": [render_page("S4", 3, "Q009")],
        "Q010": [render_page("S4", 4, "Q010")],
        "Q014": lambda: hw_crop("HW1", 1, "Exercise 3", None, "Q014"),
        "Q015": [render_page("S4", 8, "Q015")],
        "Q016": [render_page("S4", 5, "Q016")],
        "Q017": [render_page("S4", 5, "Q017")],
        "Q018": [render_page("S4", 8, "Q018")],
        "Q019": [render_page("MOCK", 4, "Q019")],
        "Q021": [("text", ["Maria: 16 hrs/day, w=$20, V=$80, U=c^0.5 l^0.5. Find l*, L*, c*.", "(Course-style)"])],
        "Q022": [("text", ["Same setup, w=$30. Find l*, L*, c*. More or less work?", "(Course-style)"])],
        "Q023": [("text", ["Contract 1: $10M today + $90M future. Contract 2: $42M + $54M. r=0.20. Cheaper PV?", "HW1 Ex 5.1"])],
        "Q024": lambda: hw_crop("HW1", 2, "Exercise 5", None, "Q024"),
        "Q025": [render_page("S4", 11, "Q025"), render_page("S4", 12, "Q025b")],
        "Q026": lambda: pdf_crop("MOCK", 5, "Question 24", "Question 25", "Q026"),
        "Q027": lambda: merge_images(
            lambda: pdf_crop("MOCK", 5, "Question 24", "Question 25", "Q027_setup"),
            lambda: pdf_crop("MOCK", 5, "Question 25", None, "Q027"),
        )(),
        "Q028": lambda: hw_crop("HW1", 2, "Exercise 4", "Exercise 5", "Q028"),
        "Q029": [render_page("S4", 10, "Q029")],
        "Q030": [render_page("S4", 10, "Q030")],
        "Q031": [render_page("S4", 11, "Q031")],
        "Q032": [render_page("S4", 11, "Q032")],
        "Q033": [render_page("S4", 11, "Q033")],
        "Q034": [render_page("MOCK", 3, "Q034")],
        "Q035": lambda: hw_crop("HW2", 1, "Exercise 1", "Exercise 2", "Q035"),
        "Q036": lambda: pdf_crop("S9", 5, "Question 12", "Question 13", "Q036"),
        "Q037": lambda: merge_images(
            lambda: pdf_crop("S9", 5, "Question 13", "Question 14", "Q037_setup"),
            lambda: pdf_crop("S9", 5, "Question 14", "Question 15", "Q037"),
        )(),
        "Q038": [render_page("MOCK", 8, "Q038")],
        "Q039": lambda: hw_crop("HW2", 1, "Exercise 2", None, "Q039"),
        "Q040": [render_page("S9", 2, "Q040")],
        "Q041": [render_page("S9", 2, "Q041")],
        "Q042": [render_page("S9", 3, "Q042"), render_page("S9", 4, "Q042b")],
        "Q043": [render_page("S9", 4, "Q043")],
        "Q044": [render_page("S9", 3, "Q044")],
        "Q045": [render_page("MOCK", 11, "Q045")],
        "Q046": [render_page("MOCK", 11, "Q046")],
        "Q047": lambda: hw_crop("HW2", 2, "Exercise 3", None, "Q047"),
        "Q048": lambda: merge_images(
            tom_insurance_setup("Q048_setup"),
            lambda: pdf_crop("S9", 6, "Question 16", "Question 17", "Q048"),
        )(),
        "Q049": lambda: merge_images(
            tom_insurance_setup("Q049_setup"),
            lambda: pdf_crop("S9", 6, "Question 17", "Question 18", "Q049"),
        )(),
        "Q050": lambda: pdf_crop("S9", 6, "Question 18", "Question 19", "Q050"),
        "Q051": lambda: pdf_crop("S9", 6, "Question 20", None, "Q051"),
        "Q052": lambda: pdf_crop("MOCK", 10, "Question 27", None, "Q052"),
        "Q053": lambda: pdf_crop("MOCK", 9, "Question 25", "Question 26", "Q053"),
        "Q054": lambda: sample_q22_shots("Q054"),
        "Q055": lambda: mock_q29_shots("Q055"),
    }


def images_for(bank_id):
    src = bank_images_map().get(bank_id)
    if src is None:
        return []
    if callable(src):
        return src()
    return src


def place_image(p, img_path, y_start, margin=36):
    pix = pymupdf.open(img_path)[0].get_pixmap(alpha=False)
    scale = min((PW - 2 * margin) / pix.width, (PH - y_start - margin) / pix.height)
    w, h = pix.width * scale, pix.height * scale
    p.insert_image(pymupdf.Rect(margin, y_start, margin + w, y_start + h), filename=img_path)
    return y_start + h + 10


def exam_cover(out, test):
    p = out.new_page(width=PW, height=PH)
    p.insert_text((72, 100), "ECON 351 — Midterm Simulation", fontsize=22, fontname="helv")
    p.insert_text((72, 135), test["title"], fontsize=18, fontname="helv", color=COLOR)
    p.insert_text((72, 175), "24 Questions  |  24 points (1 pt each)", fontsize=12, fontname="helv")
    y = 220
    p.insert_text((72, y), "FORMAT (matches your teacher's breakdown):", fontsize=11, fontname="helv", color=COLOR)
    y += 22
    p.insert_text((72, y), "PART A — Chapter 4 (12 questions)", fontsize=11, fontname="helv", color=COLOR)
    y += 16
    for s in EXAM_STRUCTURE:
        if s["ch"] != 4:
            continue
        line = f"  {s['count']} {s['category']}"
        p.insert_text((72, y), line, fontsize=10, fontname="helv")
        y += 14
    y += 10
    p.insert_text((72, y), "PART B — Chapter 9 (12 questions)", fontsize=11, fontname="helv", color=COLOR)
    y += 16
    for s in EXAM_STRUCTURE:
        if s["ch"] != 9:
            continue
        line = f"  {s['count']} {s['category']}"
        p.insert_text((72, y), line, fontsize=10, fontname="helv")
        y += 14
    p.insert_text((72, 680), "Problems from HW, sample questions, and mock midterm (screenshots).", fontsize=9, fontname="helv", color=MUTED)
    p.insert_text((72, 695), "Use Formula_Sheet.pdf for reference.", fontsize=9, fontname="helv", color=MUTED)


def section_header(out, ch, label):
    p = out.new_page(width=PW, height=PH)
    p.insert_text((72, 340), f"PART {'A' if ch == 4 else 'B'}", fontsize=14, fontname="helv", color=MUTED)
    p.insert_text((72, 370), f"CHAPTER {ch}", fontsize=26, fontname="helv", color=COLOR)
    p.insert_text((72, 410), label, fontsize=13, fontname="helv")
    return p


def add_question(out, qnum, bank_id, category, ch):
    items = images_for(bank_id)
    p = out.new_page(width=PW, height=PH)
    p.insert_text((40, 42), f"Question {qnum} of 24  |  Ch. {ch}", fontsize=10, fontname="helv", color=MUTED)
    p.insert_text((40, 58), category, fontsize=9, fontname="helv", color=COLOR)
    p.insert_text((40, 76), f"[{bank_id}]", fontsize=9, fontname="helv", color=MUTED)
    y = 96
    if not items:
        p.insert_text((40, y), f"(See question bank for {bank_id} text)", fontsize=10, fontname="helv", color=MUTED)
        y += 20
    for item in items:
        if isinstance(item, tuple) and item[0] == "text":
            for line in item[1]:
                p.insert_text((40, y), line, fontsize=11, fontname="helv")
                y += 15
        elif isinstance(item, str) and os.path.exists(item):
            if y > PH - 100:
                p = out.new_page(width=PW, height=PH)
                p.insert_text((40, 42), f"Question {qnum} — continued", fontsize=10, fontname="helv", color=MUTED)
                y = 60
            y = place_image(p, item, y)


def build_practice_test(test):
    out = pymupdf.open()
    exam_cover(out, test)
    qnum = 0
    current_ch = None
    for section in EXAM_STRUCTURE:
        if section["ch"] != current_ch:
            current_ch = section["ch"]
            total = sum(s["count"] for s in EXAM_STRUCTURE if s["ch"] == current_ch)
            section_header(out, current_ch, f"{total} questions")
        for _ in range(section["count"]):
            qnum += 1
            bank_id = test["ids"][qnum - 1]
            add_question(out, qnum, bank_id, section["category"], section["ch"])
    path = os.path.join(PDF_OUT_DIR, f"{test['name']}.pdf")
    out.save(path, garbage=4, deflate=True)
    print(f"  {test['name']}.pdf — 24 questions, {len(out)} pages")
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
    print("  Formula_Sheet.pdf — 1 page")
    return path


def build_all():
    validate_exam_structure()
    for test in PRACTICE_TESTS:
        assert len(test["ids"]) == 24
    print("Building 24-question simulation practice tests:")
    for test in PRACTICE_TESTS:
        build_practice_test(test)
    build_formula_pdf()
    print(f"\nDone — output in {PDF_OUT_DIR}/")


if __name__ == "__main__":
    build_all()
