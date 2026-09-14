#!/usr/bin/env python3
"""Build Diversification_Variance_Problems.pdf from course materials (screenshots)."""

import os
import textwrap
import pymupdf

from create_exam_prep_pdf import (
    PW,
    PH,
    COLOR,
    MUTED,
    place_image,
    mock_q29_shots,
    sample_q22_shots,
)

UPLOADS = "/home/ubuntu/.cursor/projects/workspace/uploads"
LECTURE = f"{UPLOADS}/Econ351Lecture_2__Chapter_9___2__5b08.pdf"
OUT = "/workspace/Diversification_Variance_Problems.pdf"
IMG_DIR = "/workspace/diversification_images"
os.makedirs(IMG_DIR, exist_ok=True)

FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_NAME = "DejaVu"
FONT_NAME_BOLD = "DejaVu-Bold"

SOURCES_CHECKED = [
    ("Homework 1 Ch.4", "No diversification/variance problems"),
    ("Homework 2 Ch.9", "No diversification/variance problems"),
    ("Sample Questions Ch.4", "No diversification/variance problems"),
    ("Sample Questions Ch.9", "Question 22 - Feng/Nan portfolios (included)"),
    ("Mock Midterm 1", "Question 29 - John/Marc variance (included)"),
    ("Econ351 Lecture Ch.9", "Variance, correlation, diversification slides (included)"),
    ("Practice Test 1 Q24", "Same as Sample Q22"),
    ("Practice Test 2 Q24", "Same as Mock Q29"),
    ("Practice Test 3 Q24", "Same as Sample Q22"),
]

FORMULAS = [
    "Expected value: E[x] = p1*x1 + p2*x2 + ... + pn*xn",
    "Variance: Var(x) = sum( pi * (xi - E[x])^2 )",
    "Higher variance = more risk / more volatile outcomes",
    "Correlation: do variables move together? (positive / negative / zero)",
    "Diversification: combine assets that are NOT fully positively correlated",
    "Negatively correlated portfolio -> lower variance than either asset alone",
    "Positively correlated portfolio -> higher variance (less diversification benefit)",
]

PROBLEMS = [
    {
        "id": "D-1",
        "source": "Sample Questions Ch.9 - Question 22 | Practice Tests 1 & 3 Q24",
        "shots": lambda: sample_q22_shots("D1_q22"),
        "note": "Feng: agriculture (A & B). Nan: airline/oil (C & D).",
    },
    {
        "id": "D-2",
        "source": "Mock Midterm 1 - Question 29 | Practice Test 2 Q24",
        "shots": lambda: mock_q29_shots("D2_q29"),
        "note": "John: half A + half B (positively correlated). Marc: half C + half D (negatively correlated).",
    },
    {
        "id": "D-3",
        "source": "Econ351 Lecture Ch.9 - Variance (formula)",
        "shots": lambda: [render_lecture_page(6, "D3_var_formula")],
        "note": "Lecture slide: variance definition and formula.",
    },
    {
        "id": "D-4",
        "source": "Econ351 Lecture Ch.9 - Variance (numeric examples)",
        "shots": lambda: [render_lecture_page(7, "D4_var_examples")],
        "note": "Compare Investment 1 (low variance) vs Investment 2 (high variance).",
    },
    {
        "id": "D-5",
        "source": "Econ351 Lecture Ch.9 - Correlation",
        "shots": lambda: [render_lecture_page(9, "D5_corr")],
        "note": "Correlation measures whether variables move together.",
    },
    {
        "id": "D-6",
        "source": "Econ351 Lecture Ch.9 - Diversification",
        "shots": lambda: [render_lecture_page(60, "D6_diversify")],
        "note": "Diversified portfolio (Nvidia + Sony) reduces risk vs single stock.",
    },
]

ANSWERS = [
    ("D-1", "a) A & B positively correlated. b) C & D negatively correlated. c) Feng has riskier portfolio."),
    ("D-1 detail", "Feng: $190 if rain, $150 if drought (EV=$170, high spread). Nan: always $170 (diversified)."),
    ("D-2", "(D) John's investment has higher variance and John is less risk averse than Marc."),
    ("D-3/D-4", "Var(Inv1)=100; Var(Inv2)=90,000. Same expected value can have very different risk."),
    ("D-5", "Positive correlation: variables move together. Correlation does not imply causation."),
    ("D-6", "Hold assets with outcomes not fully correlated to reduce portfolio risk."),
]


def render_lecture_page(page_1based, tag):
    doc = pymupdf.open(LECTURE)
    page = doc[page_1based - 1]
    mat = pymupdf.Matrix(132 / 72, 132 / 72)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    path = os.path.join(IMG_DIR, f"{tag}_lecture_p{page_1based}.jpg")
    pix.save(path, jpg_quality=78)
    return path


def setup_page_fonts(page):
    page.insert_font(fontname=FONT_NAME, fontfile=FONT_REG)
    page.insert_font(fontname=FONT_NAME_BOLD, fontfile=FONT_BOLD)


def write_lines(page, x, y, lines, size=11, color=(0, 0, 0), leading=15, bold=False):
    font = FONT_NAME_BOLD if bold else FONT_NAME
    for line in lines:
        page.insert_text((x, y), line, fontsize=size, fontname=font, color=color)
        y += leading
    return y


def flatten_paths(items):
    out = []
    for item in items:
        if isinstance(item, list):
            out.extend(flatten_paths(item))
        elif isinstance(item, str):
            out.append(item)
    return out


def add_shot_pages(out, prob, num):
    paths = flatten_paths(prob["shots"]())
    p = out.new_page(width=PW, height=PH)
    setup_page_fonts(p)
    write_lines(p, 40, 42, [f"Problem {num}: {prob['id']}"], size=14, color=COLOR, bold=True)
    write_lines(p, 40, 58, [prob["source"]], size=9, color=MUTED)
    if prob.get("note"):
        write_lines(p, 40, 72, [prob["note"]], size=9, color=MUTED)
    y = 92
    for img_path in paths:
        if not os.path.exists(img_path):
            continue
        if y > PH - 120:
            p = out.new_page(width=PW, height=PH)
            setup_page_fonts(p)
            write_lines(p, 40, 42, [f"Problem {num}: {prob['id']} (continued)"], size=11, color=COLOR, bold=True)
            y = 60
        y = place_image(p, img_path, y)


def build_pdf():
    out = pymupdf.open()

    p = out.new_page(width=PW, height=PH)
    setup_page_fonts(p)
    write_lines(p, 72, 100, ["ECON 351 - Diversification & Variance Problems"], size=22, color=COLOR, bold=True)
    write_lines(p, 72, 135, ["Screenshots from homework, sample exam, mock midterm, lecture, and practice tests"], size=12)
    y = 175
    write_lines(p, 72, y, ["Sources checked:"], size=11, color=COLOR, bold=True)
    y += 20
    for src, note in SOURCES_CHECKED:
        y = write_lines(p, 72, y, [f"  - {src}: {note}"], size=9)
    y += 14
    write_lines(p, 72, y, [f"{len(PROBLEMS)} problem sets in this PDF."], size=10)

    p = out.new_page(width=PW, height=PH)
    setup_page_fonts(p)
    write_lines(p, 40, 45, ["Variance, Correlation & Diversification - Formula Sheet"], size=14, color=COLOR, bold=True)
    y = 75
    for f in FORMULAS:
        y = write_lines(p, 40, y, [f], size=10)

    for i, prob in enumerate(PROBLEMS, 1):
        add_shot_pages(out, prob, i)

    p = out.new_page(width=PW, height=PH)
    setup_page_fonts(p)
    write_lines(p, 40, 45, ["Answer Key"], size=14, color=COLOR, bold=True)
    y = 75
    for pid, ans in ANSWERS:
        y = write_lines(p, 40, y, [f"{pid}:"], size=11, color=COLOR, bold=True)
        y += 14
        for line in textwrap.wrap(ans, width=90):
            y = write_lines(p, 55, y, [line], size=10)
        y += 6

    out.save(OUT, garbage=4, deflate=True)
    print(f"Saved: {OUT} ({len(out)} pages)")


if __name__ == "__main__":
    build_pdf()
