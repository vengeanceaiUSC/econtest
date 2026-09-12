#!/usr/bin/env python3
"""Generate Exam Prep PDF with screenshots from original source PDFs."""

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

DPI = 144
JPEG_QUALITY = 82
os.makedirs(OUT_DIR, exist_ok=True)


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
    y0 = max(0, y0 - 6)
    y1 = min(page.rect.height, y1)
    if y1 - y0 < 20:
        return render_page(pdf_key, page_1based, tag)
    clip = (0, y0, page.rect.width, y1)
    mat = pymupdf.Matrix(DPI / 72, DPI / 72)
    pix = page.get_pixmap(matrix=mat, clip=pymupdf.Rect(*clip), alpha=False)
    path = os.path.join(OUT_DIR, f"q{tag}_{pdf_key}_crop.jpg")
    pix.save(path, jpg_quality=JPEG_QUALITY)
    return path


def y_of(pdf_key, page_1based, label):
    doc = pymupdf.open(PDFS[pdf_key])
    page = doc[page_1based - 1]
    hits = page.search_for(label)
    return hits[0].y0 if hits else None


def hw_crop(pdf_key, page, start_label, end_label, tag):
    y0 = y_of(pdf_key, page, start_label)
    y1 = y_of(pdf_key, page, end_label) if end_label else None
    if y0 is None:
        return [render_page(pdf_key, page, tag)]
    if y1 is None or y1 <= y0:
        doc = pymupdf.open(PDFS[pdf_key])
        y1 = doc[page - 1].rect.height
    return [render_crop(pdf_key, page, y0, y1, tag)]


# (num, label, ch, cat, source, images_fn)
def images_for(qnum):
    specs = {
        1: lambda: hw_crop("HW1", 1, "Exercise 3", "Exercise 4", qnum),
        2: lambda: [render_page("S4", 8, qnum)],
        3: lambda: [("text", [
            "Maria has 16 hours/day for leisure and work.",
            "Wage w = $20/hr, non-labor income V = $80.",
            "U(c,l) = c^0.5 l^0.5, c = w(16-l)+V. Find l*, L*, c*.",
            "(Course-style — not in uploaded PDFs.)",
        ])],
        4: lambda: [("text", [
            "Same as Q3 but w = $30. Find l*, L*, c*. Work more or less?",
        ])],
        5: lambda: [render_page("S4", 11, qnum), render_page("S4", 12, f"{qnum}b")],
        6: lambda: [render_page("MOCK", 5, qnum)],
        7: lambda: hw_crop("HW1", 2, "Exercise 4", "Exercise 5", qnum),
        8: lambda: [render_page("S4", 11, qnum)],
        9: lambda: [render_page("S4", 11, f"{qnum}_alt")],  # same page, full
        10: lambda: [render_page("S4", 3, qnum)],
        11: lambda: hw_crop("HW1", 1, "Exercise 2", "Exercise 3", qnum),
        12: lambda: [render_page("S4", 3, f"{qnum}_alt")],
        13: lambda: [render_page("HW2", 2, qnum)],
        14: lambda: [render_page("HW2", 2, f"{qnum}_alt")],
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
    return specs[qnum]()


QUESTIONS_META = [
    (1, "Consumer Problem #1", 4, "Consumer Problems", "HW1 Ex 3"),
    (2, "Consumer Problem #2", 4, "Consumer Problems", "Sample Q26"),
    (3, "Labor-Leisure #1", 4, "Labor-Leisure", "Course-style"),
    (4, "Labor-Leisure #2", 4, "Labor-Leisure", "Course-style"),
    (5, "Intertemporal #1", 4, "Intertemporal", "Sample Q41"),
    (6, "Intertemporal #2", 4, "Intertemporal", "Mock Q24-25"),
    (7, "Elasticity #1", 4, "Elasticity", "HW1 Ex 4"),
    (8, "Elasticity #2", 4, "Elasticity", "Sample Q39"),
    (9, "Elasticity #3", 4, "Elasticity", "Sample Q38"),
    (10, "Budget Line", 4, "Budget Line", "Sample Q10"),
    (11, "Preferences #1", 4, "Preferences", "HW1 Ex 2.2"),
    (12, "Preferences #2", 4, "Preferences", "Sample Q8"),
    (13, "Insurance #1", 9, "Insurance", "HW2 Ex 3"),
    (14, "Insurance #2", 9, "Insurance", "HW2 Ex 3 (fair premium part b)"),
    (15, "Insurance #3", 9, "Insurance", "Sample Q18"),
    (16, "Insurance #4", 9, "Insurance", "Mock Q27"),
    (17, "Insurance #5", 9, "Insurance", "Mock Q25-26"),
    (18, "Risk Attitudes #1", 9, "Risk Attitudes", "HW2 Ex 2"),
    (19, "Risk Attitudes #2", 9, "Risk Attitudes", "Sample Q6"),
    (20, "Risk Attitudes #3", 9, "Risk Attitudes", "Sample Q8"),
    (21, "Risk Attitudes #4", 9, "Risk Attitudes", "Mock Q28"),
    (22, "CE & RP #1", 9, "CE & RP", "HW2 Ex 1"),
    (23, "CE & RP #2", 9, "CE & RP", "Sample Q12"),
    (24, "Diversification", 9, "Diversification", "Sample Q22"),
]


def insert_image_page(out, img_path, header=None):
    page_w, page_h = 612, 792
    p = out.new_page(width=page_w, height=page_h)
    y = 40
    if header:
        p.insert_text((40, y), header, fontsize=10, fontname="helv", color=(0.4, 0.4, 0.4))
        y += 18
    img = pymupdf.open(img_path)
    pix = img[0].get_pixmap(alpha=False)
    margin = 36
    avail_w = page_w - 2 * margin
    avail_h = page_h - y - margin
    scale = min(avail_w / pix.width, avail_h / pix.height)
    w, h = pix.width * scale, pix.height * scale
    rect = pymupdf.Rect(margin, y, margin + w, y + h)
    p.insert_image(rect, filename=img_path)
    return p


def build_pdf():
    out = pymupdf.open()
    pw, ph = 612, 792

    p = out.new_page(width=pw, height=ph)
    p.insert_text((72, 180), "ECON 351 Exam Prep", fontsize=26, fontname="helv")
    p.insert_text((72, 220), "24-Question Practice Set", fontsize=16, fontname="helv")
    p.insert_text((72, 260), "Original problem screenshots from HW, sample questions, and mock midterm.", fontsize=11, fontname="helv")
    p.insert_text((72, 280), "Answer key at end of Excel file (Exam Prep.xlsx).", fontsize=11, fontname="helv")

    current_ch = None
    for num, label, ch, cat, source in QUESTIONS_META:
        if ch != current_ch:
            current_ch = ch
            p = out.new_page(width=pw, height=ph)
            p.insert_text((72, 72), f"Chapter {ch}", fontsize=20, fontname="helv", color=(0.12, 0.31, 0.47))

        p = out.new_page(width=pw, height=ph)
        p.insert_text((40, 50), f"Q{num} — {label}", fontsize=14, fontname="helv", color=(0.12, 0.31, 0.47))
        p.insert_text((40, 68), f"{cat} | {source}", fontsize=9, fontname="helv", color=(0.45, 0.45, 0.45))

        items = images_for(num)
        y_text = 95
        img_idx = 0
        for item in items:
            if isinstance(item, tuple) and item[0] == "text":
                for line in item[1]:
                    p.insert_text((40, y_text), line, fontsize=11, fontname="helv")
                    y_text += 16
            elif isinstance(item, str) and os.path.exists(item):
                hdr = f"Q{num} — {label} (page {img_idx + 1})" if img_idx > 0 else None
                insert_image_page(out, item, header=hdr)
                img_idx += 1

    out.save(OUT_PDF)
    print(f"Saved: {OUT_PDF} ({len(out)} pages)")


if __name__ == "__main__":
    build_pdf()
