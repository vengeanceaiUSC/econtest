#!/usr/bin/env python3
"""Generate Exam Prep PDF — organized by teacher's category sets with source screenshots."""

import os
import pymupdf

UPLOADS = "/home/ubuntu/.cursor/projects/workspace/uploads"
OUT_DIR = "/workspace/exam_prep_images"
OUT_PDF = "/workspace/Exam_Prep.pdf"

PDFS = {
    "HW1": f"{UPLOADS}/Homework_1__Chapter_4__9bce.pdf",
    "HW2": f"{UPLOADS}/Homework_2__Chapter_9__b189.pdf",
    "S4": f"{UPLOADS}/SampleQuestionsChapter04ConsumerTheory_a895.pdf",
    "S9": f"{UPLOADS}/SampleQuestionsChapter09Uncertainty_4bdd.pdf",
    "MOCK": f"{UPLOADS}/Mock_Midterm_1_129f.pdf",
}

DPI = 132
JPEG_QUALITY = 78
os.makedirs(OUT_DIR, exist_ok=True)

# Teacher's study set structure — order and counts per category
STUDY_SETS = [
    # Chapter 4 — 12 questions
    {"ch": 4, "category": "Consumer Problems", "count": 2, "ids": [1, 2]},
    {"ch": 4, "category": "Labor-Leisure", "count": 2, "ids": [3, 4]},
    {"ch": 4, "category": "Intertemporal Consumption", "count": 2, "ids": [5, 6]},
    {"ch": 4, "category": "Elasticity / Types of Goods", "count": 3, "ids": [7, 8, 9]},
    {"ch": 4, "category": "Budget Line", "count": 1, "ids": [10]},
    {"ch": 4, "category": "Assumptions / Preferences", "count": 2, "ids": [11, 12]},
    # Chapter 9 — 12 questions
    {"ch": 9, "category": "Insurance Problems", "count": 5, "ids": [13, 14, 15, 16, 17]},
    {"ch": 9, "category": "Risk Attitudes", "count": 4, "ids": [18, 19, 20, 21]},
    {"ch": 9, "category": "Certainty Equivalent & Risk Premium", "count": 2, "ids": [22, 23]},
    {"ch": 9, "category": "Diversification", "count": 1, "ids": [24]},
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


def section_page(out, ch, category, count, set_num):
    pw, ph = 612, 792
    p = out.new_page(width=pw, height=ph)
    color = (0.12, 0.31, 0.47)
    p.insert_text((72, 280), f"CHAPTER {ch}", fontsize=22, fontname="helv", color=color)
    p.insert_text((72, 320), category, fontsize=20, fontname="helv", color=color)
    p.insert_text((72, 360), f"{count} question{'s' if count > 1 else ''}", fontsize=16, fontname="helv")
    p.insert_text((72, 400), f"Study Set {set_num} of 10", fontsize=11, fontname="helv", color=(0.45, 0.45, 0.45))
    ids = [q for s in STUDY_SETS if s["ch"] == ch and s["category"] == category for q in s["ids"]]
    p.insert_text((72, 430), f"Questions: {', '.join(f'Q{i}' for i in ids)}", fontsize=11, fontname="helv", color=(0.45, 0.45, 0.45))
    return p


def insert_image(out, img_path, header=None):
    pw, ph = 612, 792
    p = out.new_page(width=pw, height=ph)
    y = 40
    if header:
        p.insert_text((40, y), header, fontsize=9, fontname="helv", color=(0.45, 0.45, 0.45))
        y += 16
    pix = pymupdf.open(img_path)[0].get_pixmap(alpha=False)
    m = 36
    scale = min((pw - 2 * m) / pix.width, (ph - y - m) / pix.height)
    w, h = pix.width * scale, pix.height * scale
    p.insert_image(pymupdf.Rect(m, y, m + w, y + h), filename=img_path)


def formula_sheet_page(out):
    pw, ph = 612, 792
    p = out.new_page(width=pw, height=ph)
    p.insert_text((40, 40), "ONE-PAGE FORMULA SHEET", fontsize=16, fontname="helv", color=(0.12, 0.31, 0.47))
    y = 70
    p.insert_text((40, y), "CHAPTER 4 — Consumer Theory", fontsize=12, fontname="helv", color=(0.12, 0.31, 0.47))
    y += 20
    for line in FORMULA_CH4:
        p.insert_text((40, y), line, fontsize=9, fontname="helv")
        y += 13
    y += 10
    p.insert_text((40, y), "CHAPTER 9 — Uncertainty & Risk", fontsize=12, fontname="helv", color=(0.12, 0.31, 0.47))
    y += 20
    for line in FORMULA_CH9:
        p.insert_text((40, y), line, fontsize=9, fontname="helv")
        y += 13


def build_pdf():
    out = pymupdf.open()
    pw, ph = 612, 792

    # Cover
    p = out.new_page(width=pw, height=ph)
    p.insert_text((72, 140), "ECON 351 Exam Prep", fontsize=26, fontname="helv")
    p.insert_text((72, 175), "24-Question Focused Study Set", fontsize=16, fontname="helv")
    y = 220
    p.insert_text((72, y), "Organized by teacher topic breakdown:", fontsize=11, fontname="helv")
    y += 22
    p.insert_text((72, y), "Ch.4 (12): 2 consumer | 2 labor-leisure | 2 intertemporal | 3 elasticity", fontsize=10, fontname="helv")
    y += 16
    p.insert_text((72, y), "         1 budget line | 2 preferences", fontsize=10, fontname="helv")
    y += 16
    p.insert_text((72, y), "Ch.9 (12): 5 insurance | 4 risk attitudes | 2 CE & RP | 1 diversification", fontsize=10, fontname="helv")
    y += 30
    p.insert_text((72, y), "Problems = screenshots from original HW, samples, mock midterm.", fontsize=10, fontname="helv", color=(0.45, 0.45, 0.45))

    # Study plan table page
    p = out.new_page(width=pw, height=ph)
    p.insert_text((40, 50), "STUDY SET OVERVIEW", fontsize=16, fontname="helv", color=(0.12, 0.31, 0.47))
    y = 80
    current_ch = None
    set_n = 0
    for s in STUDY_SETS:
        if s["ch"] != current_ch:
            current_ch = s["ch"]
            p.insert_text((40, y), f"--- Chapter {current_ch} ({sum(x['count'] for x in STUDY_SETS if x['ch']==current_ch)} questions) ---", fontsize=11, fontname="helv", color=(0.12, 0.31, 0.47))
            y += 18
        set_n += 1
        ids = ", ".join(f"Q{i}" for i in s["ids"])
        line = f"Set {set_n}: {s['category']} ({s['count']}) — {ids}"
        p.insert_text((50, y), line, fontsize=10, fontname="helv")
        y += 15

    # Questions by study set
    set_n = 0
    current_ch = None
    for s in STUDY_SETS:
        set_n += 1
        if s["ch"] != current_ch:
            current_ch = s["ch"]
            p = out.new_page(width=pw, height=ph)
            p.insert_text((72, 360), f"CHAPTER {current_ch}", fontsize=28, fontname="helv", color=(0.12, 0.31, 0.47))
            total = sum(x["count"] for x in STUDY_SETS if x["ch"] == current_ch)
            p.insert_text((72, 400), f"{total} questions total", fontsize=14, fontname="helv")

        section_page(out, s["ch"], s["category"], s["count"], set_n)

        for idx, qid in enumerate(s["ids"], 1):
            label, source = QUESTION_INFO[qid]
            p = out.new_page(width=pw, height=ph)
            p.insert_text((40, 45), f"Set {set_n}: {s['category']}", fontsize=10, fontname="helv", color=(0.12, 0.31, 0.47))
            p.insert_text((40, 62), f"Q{qid} ({idx} of {s['count']}) — {label}", fontsize=13, fontname="helv")
            p.insert_text((40, 78), source, fontsize=9, fontname="helv", color=(0.45, 0.45, 0.45))

            items = images_for(qid)
            y = 100
            img_i = 0
            for item in items:
                if isinstance(item, tuple) and item[0] == "text":
                    for line in item[1]:
                        p.insert_text((40, y), line, fontsize=11, fontname="helv")
                        y += 15
                elif isinstance(item, str) and os.path.exists(item):
                    hdr = f"Q{qid} — page {img_i + 1}" if img_i else None
                    insert_image(out, item, hdr)
                    img_i += 1

    formula_sheet_page(out)
    out.save(OUT_PDF, garbage=4, deflate=True)
    print(f"Saved: {OUT_PDF} ({len(out)} pages)")


if __name__ == "__main__":
    build_pdf()
