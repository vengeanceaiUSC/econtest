#!/usr/bin/env python3
"""Build Intertemporal_Consumption_Problems.pdf from course materials (screenshots)."""

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
    sample_q41_shots,
    sample_q42_shots,
    mock_q25_shots,
)

OUT = "/workspace/Intertemporal_Consumption_Problems.pdf"

FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_NAME = "DejaVu"
FONT_NAME_BOLD = "DejaVu-Bold"

SOURCES_CHECKED = [
    ("Homework 1 Ch.4 Ex 5", "5.1-5.6 intertemporal consumption (Shohei contract)"),
    ("Sample Questions Ch.4", "Q41-Q42 (save vs borrow, two interest rates)"),
    ("Mock Midterm 1", "Q24-Q25 (budget constraint + optimum)"),
    ("Homework 2 Ch.9", "No intertemporal questions"),
    ("Sample Questions Ch.9", "No intertemporal questions"),
    ("Practice Tests 1-3", "2 intertemporal questions each (Q023-Q027 bank IDs)"),
]

FORMULAS = [
    "Present-value budget: c1 + c2/(1+r) = I1 + I2/(1+r)",
    "Future-value budget: (1+r)c1 + c2 = (1+r)I1 + I2",
    "With unit prices p1=p2=1: q1 + q2/(1+r) = I1 + I2/(1+r)",
    "Optimum (two goods): MU1/MU2 = p1/(p2/(1+r)) = (1+r) when p1=p2=1",
    "Cobb-Douglas u = q1*q2: at optimum q2 = (1+r)q1",
    "Cobb-Douglas u = c1^a c2^b: c2/c1 = (b/a)(1+r) at optimum",
    "PV of income stream: PV = I1 + I2/(1+r)",
    "Saving: spend less than I1 in period 1 (lend). Borrowing: spend more than I1.",
]

PROBLEMS = [
    {
        "id": "IT-1",
        "source": "Homework 1 Ch.4 - Exercise 5 (5.1 through 5.6)",
        "shots": lambda: hw_crop("HW1", 2, "Exercise 5", None, "IT1_hw5"),
        "note": "Shohei contract problem - PV, MRS, optimum c1/c2, contract comparison.",
    },
    {
        "id": "IT-2",
        "source": "Sample Questions Ch.4 - Question 41 | Practice Tests (Q025)",
        "shots": lambda: sample_q41_shots("IT2_q41"),
        "note": "I1=10, I2=12, r=0.5, u=q1*q2. Find optimum and whether consumer saves.",
    },
    {
        "id": "IT-3",
        "source": "Sample Questions Ch.4 - Question 42",
        "shots": lambda: sample_q42_shots("IT3_q42"),
        "note": "Same setup as Q41 but r=0.05. Consumer borrows instead of saves.",
    },
    {
        "id": "IT-4",
        "source": "Mock Midterm 1 - Question 24 | Practice Tests (Q026)",
        "shots": lambda: pdf_crop("MOCK", 5, "Question 24", "Question 25", "IT4_mock24"),
        "note": "I1=60, I2=125, r=0.25, u=q1*q2. Identify the intertemporal budget constraint.",
    },
    {
        "id": "IT-5",
        "source": "Mock Midterm 1 - Question 25 | Practice Tests (Q027)",
        "shots": lambda: mock_q25_shots("IT5_mock25"),
        "note": "Using Q24 setup, find optimal q1 in period 1.",
    },
]

ANSWERS = [
    ("IT-1 (5.1)", "PV1 = 10 + 90/1.2 = 85M; PV2 = 42 + 54/1.2 = 87M. Contract 1 is cheaper."),
    ("IT-1 (5.2)", "Higher exponent on c2 means Shohei values future consumption more (patient). MUc1/MUc2 = (2/3)(c2/c1)."),
    ("IT-1 (5.3)", "MRS = (1+r) = 1.2, so c2 = 1.8 c1."),
    ("IT-1 (5.4)", "Budget: c1 + c2/1.2 = 85. With c2=1.8c1: c1* = 34, c2* = 61.2."),
    ("IT-1 (5.5)", "Budget: c1 + c2/1.2 = 87. c1* = 34.8, c2* = 62.64."),
    ("IT-1 (5.6)", "Compare utility from each contract; Angels could offer a front-loaded contract if cash-constrained."),
    ("IT-2 (Q41)", "q1* = 9, q2* = 13.5. Consumer saves 1 (spends 9 < I1=10)."),
    ("IT-3 (Q42)", "q1* = 75/7, q2* = 45/4. Consumer borrows 5/7 (spends more than I1 in period 1)."),
    ("IT-4 (Mock Q24)", "(A) q1 + 0.8q2 = 160. PV budget with 1/(1+r) = 0.8."),
    ("IT-5 (Mock Q25)", "(D) q1 = 80. Cobb-Douglas u=q1*q2 gives q2=(1+r)q1; budget yields q1=80."),
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
    write_lines(p, 72, 100, ["ECON 351 - Intertemporal Consumption Problems"], size=22, color=COLOR, bold=True)
    write_lines(p, 72, 135, ["Screenshots from homework, sample exam, and mock midterm"], size=13)
    y = 175
    write_lines(p, 72, y, ["Sources checked:"], size=11, color=COLOR, bold=True)
    y += 20
    for src, note in SOURCES_CHECKED:
        y = write_lines(p, 72, y, [f"  - {src}: {note}"], size=9)
    y += 14
    write_lines(p, 72, y, [f"{len(PROBLEMS)} problem sets in this PDF (all intertemporal problems found)."], size=10)

    p = out.new_page(width=PW, height=PH)
    setup_page_fonts(p)
    write_lines(p, 40, 45, ["Intertemporal Consumption - Formula Sheet"], size=14, color=COLOR, bold=True)
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
