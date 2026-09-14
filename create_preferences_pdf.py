#!/usr/bin/env python3
"""Build Assumptions_Preferences_Problems.pdf from course materials (screenshots)."""

import os
import textwrap
import pymupdf

from create_exam_prep_pdf import (
    PW,
    PH,
    COLOR,
    MUTED,
    place_image,
    hw_crop,
    pdf_crop,
    column_crop,
    sample_q6_shots,
    sample_q9_shots,
    sample_q31_shots,
)

OUT = "/workspace/Assumptions_Preferences_Problems.pdf"

FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_NAME = "DejaVu"
FONT_NAME_BOLD = "DejaVu-Bold"

SOURCES_CHECKED = [
    ("Homework 1 Ch.4 Ex 2", "3 assumption questions (completeness, transitivity)"),
    ("Sample Questions Ch.4", "Q5-Q8, Q30-Q31 (IC slope, substitutes, complements)"),
    ("Mock Midterm 1", "Q22 (Cobb-Douglas same IC)"),
    ("Homework 2 Ch.9", "No assumptions/preferences questions"),
    ("Sample Questions Ch.9", "No assumptions/preferences questions"),
    ("Practice Tests 1-3", "2 assumptions/preferences questions each"),
]

FORMULAS = [
    "Completeness: consumer can always rank any two bundles (or be indifferent)",
    "Transitivity: if A > B and B > C, then A > C",
    "Cannot decide between bundles -> violates completeness",
    "Indifference is OK -> does NOT violate completeness",
    "IC slope (absolute value) = MRS = MU_x / MU_y",
    "Perfect substitutes: straight-line ICs, u = aX + bY",
    "Perfect complements: L-shaped ICs, fixed proportions",
    "Diminishing MRS: standard convex ICs bow toward origin",
]

PROBLEMS = [
    {
        "id": "P-1",
        "source": "Homework 1 Ch.4 - Exercise 2 (2.1, 2.2, 2.3)",
        "shots": lambda: hw_crop("HW1", 1, "Exercise 2", "Exercise 3", "P1_hw2"),
        "note": "Jackie movie theater scenarios - completeness and transitivity.",
    },
    {
        "id": "P-2",
        "source": "Sample Questions Ch.4 - Question 5 | Practice Test 3",
        "shots": lambda: pdf_crop("S4", 2, "Question 5", "Question 6", "P2_q5"),
        "note": "What does the slope of an IC tell you?",
    },
    {
        "id": "P-3",
        "source": "Sample Questions Ch.4 - Question 6 | Practice Test 2",
        "shots": lambda: sample_q6_shots("P3_q6"),
        "note": "Magnitude of IC slope = MRS (two-column page).",
    },
    {
        "id": "P-4",
        "source": "Sample Questions Ch.4 - Question 7",
        "shots": lambda: [column_crop("S4", 2, "Question 7", None, "R", "P4_q7")],
        "note": "Inka: linear utility u = (3/4)X + (2/7)Y - perfect substitutes.",
    },
    {
        "id": "P-5",
        "source": "Sample Questions Ch.4 - Question 8 | Practice Test 1",
        "shots": lambda: pdf_crop("S4", 3, "Question 8", "Question 9", "P5_q8"),
        "note": "Serena: straight-line IC slope -7/5 -> u = X/5 + Y/7.",
    },
    {
        "id": "P-6",
        "source": "Sample Questions Ch.4 - Question 9",
        "shots": lambda: sample_q9_shots("P6_q9"),
        "note": "Angelique: Cobb-Douglas baskets on same IC (two-column page).",
    },
    {
        "id": "P-7",
        "source": "Sample Questions Ch.4 - Question 30",
        "shots": lambda: pdf_crop("S4", 9, "Question 30", "Question 31", "P7_q30"),
        "note": "Tony: perfect complements 1/4 X with 1/6 Y.",
    },
    {
        "id": "P-8",
        "source": "Sample Questions Ch.4 - Question 31",
        "shots": lambda: sample_q31_shots("P8_q31"),
        "note": "Jimmy: L-shaped IC - optimal mix 9X = 4Y (two-column page).",
    },
    {
        "id": "P-9",
        "source": "Mock Midterm 1 - Question 22",
        "shots": lambda: pdf_crop("MOCK", 4, "Question 22", None, "P9_mock22"),
        "note": "Cobb-Douglas u = X^6 Y^3 - find XB on same IC as basket A.",
    },
]

ANSWERS = [
    ("P-1 (2.1)", "No violation. Indifference is allowed under completeness."),
    ("P-1 (2.2)", "Yes - violates completeness (cannot rank bundles)."),
    ("P-1 (2.3)", "Yes - violates transitivity."),
    ("P-2", "(C) the marginal rate of substitution."),
    ("P-3", "(A) called the marginal rate of substitution."),
    ("P-4", "(B) Y = 17.333"),
    ("P-5", "(D) u(X,Y) = X/5 + Y/7"),
    ("P-6", "(D) XB = 16"),
    ("P-7", "(D) 6X = 4Y"),
    ("P-8", "(A) 9X = 4Y"),
    ("P-9", "(D) XB = 16"),
]


def setup_page_fonts(page):
    page.insert_font(fontname=FONT_NAME, fontfile=FONT_REG)
    page.insert_font(fontname=FONT_NAME_BOLD, fontfile=FONT_BOLD)


def write_lines(page, x, y, lines, size=11, color=(0, 0, 0), leading=16, bold=False):
    font = FONT_NAME_BOLD if bold else FONT_NAME
    for line in lines:
        page.insert_text((x, y), line, fontsize=size, fontname=font, color=color)
        y += leading
    return y


def write_paragraph(page, x, y, text, size=11, width=85, leading=16, color=(0, 0, 0)):
    for para in text.split("\n"):
        if not para.strip():
            y += 8
            continue
        wrapped = textwrap.wrap(para, width=width) or [""]
        y = write_lines(page, x, y, wrapped, size=size, color=color, leading=leading)
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
    write_lines(p, 72, 100, ["ECON 351 - Assumptions & Preferences Problems"], size=22, color=COLOR, bold=True)
    write_lines(p, 72, 135, ["Screenshots from homework, sample exam, and mock midterm"], size=13)
    y = 175
    write_lines(p, 72, y, ["Sources checked:"], size=11, color=COLOR, bold=True)
    y += 20
    for src, note in SOURCES_CHECKED:
        y = write_lines(p, 72, y, [f"  - {src}: {note}"], size=9)
    y += 14
    write_lines(p, 72, y, [f"{len(PROBLEMS)} problem sets in this PDF."], size=10)

    p = out.new_page(width=PW, height=PH)
    setup_page_fonts(p)
    write_lines(p, 40, 45, ["Assumptions & Preferences - Formula Sheet"], size=14, color=COLOR, bold=True)
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
