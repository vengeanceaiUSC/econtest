#!/usr/bin/env python3
"""Build Labor_Leisure_Problems.pdf — all labor-leisure problems for the course."""

import os
import textwrap
import pymupdf

OUT = "/workspace/Labor_Leisure_Problems.pdf"
PW, PH = 612, 792
COLOR = (0.12, 0.31, 0.47)
MUTED = (0.45, 0.45, 0.45)

PDF_URL = "https://github.com/vengeanceaiUSC/econtest/releases/download/exam-prep-download/Labor_Leisure_Problems.pdf"

SOURCES_CHECKED = [
    ("Homework 1 Ch.4", "No labor-leisure exercises"),
    ("Homework 2 Ch.9", "No labor-leisure (Ch.9 uncertainty only)"),
    ("Sample Questions Ch.4", "No labor-leisure questions found"),
    ("Sample Questions Ch.9", "No labor-leisure questions found"),
    ("Mock Midterm 1", "No labor-leisure questions found"),
    ("Econ351 Lecture (Ch.9 upload)", "Chapter 9 only — no labor-leisure"),
    ("Practice Tests 1–3", "Q3 & Q4 — Maria problems (included below)"),
]

FORMULAS = [
    "Time: T = L + ℓ  (total hours = labor + leisure)",
    "Budget: c = w·L + V = w(T − ℓ) + V",
    "Optimum: MU_ℓ / MU_c = w",
    "Cobb-Douglas U = c^α ℓ^β: at optimum β·c = α·w·ℓ",
    "Special case α = β = 0.5: c = w·ℓ  and  ℓ* = (w·T + V) / (2w)",
    "Labor hours: L* = T − ℓ*",
    "Consumption: c* = w·ℓ* + V",
]

PROBLEMS = [
    {
        "id": "LL-1",
        "source": "Practice Tests 1, 2, 3 — Question 3",
        "text": (
            "Maria has 16 hours per day for leisure (ℓ) and work.\n"
            "Wage w = $20/hr, non-labor income V = $80.\n"
            "Utility U(c, ℓ) = c^0.5 ℓ^0.5, where c = w(16 − ℓ) + V.\n\n"
            "(a) Write the budget constraint.\n"
            "(b) Find optimal leisure ℓ*.\n"
            "(c) Find labor hours L* and consumption c*."
        ),
    },
    {
        "id": "LL-2",
        "source": "Practice Tests 1, 2, 3 — Question 4",
        "text": (
            "Same setup as LL-1, but wage rises to w = $30/hr.\n\n"
            "(a) Find new ℓ*, L*, and c*.\n"
            "(b) Does Maria work more or less than when w = $20? Explain."
        ),
    },
    {
        "id": "LL-3",
        "source": "Extra drill — standard Cobb-Douglas",
        "text": (
            "Alex has T = 8 hours/day, w = $25/hr, V = $0.\n"
            "U(c, ℓ) = c^0.5 ℓ^0.5, c = w(8 − ℓ).\n\n"
            "Find ℓ*, L*, and c*."
        ),
    },
    {
        "id": "LL-4",
        "source": "Extra drill — non-labor income change",
        "text": (
            "Same as LL-3 but V = $40 (lottery winnings).\n\n"
            "Find ℓ*, L*, c*. Did leisure increase compared to LL-3?"
        ),
    },
    {
        "id": "LL-5",
        "source": "Extra drill — leisure-loving preferences",
        "text": (
            "Jordan: T = 24 hrs, w = $15/hr, V = $60.\n"
            "U(c, ℓ) = c^0.25 ℓ^0.75 (more leisure-loving than Maria).\n\n"
            "Use MU_ℓ/MU_c = w to find ℓ*, L*, c*."
        ),
    },
    {
        "id": "LL-6",
        "source": "Extra drill — wage comparative statics",
        "text": (
            "Sam: T = 10 hrs, V = $100, U(c, ℓ) = c^0.5 ℓ^0.5.\n"
            "(a) If w = $10, find ℓ* and L*.\n"
            "(b) If w = $40, find ℓ* and L*.\n"
            "(c) As wage rises, does Sam work more or less?"
        ),
    },
]

ANSWERS = [
    ("LL-1", "BC: c = 20(16−ℓ)+80. ℓ*=10, L*=6, c*=$200"),
    ("LL-2", "ℓ*≈9.33, L*≈6.67, c*≈$360. Works MORE (w↑ → ℓ*↑ but L*=T−ℓ* also ↑ for α=β=0.5)"),
    ("LL-3", "ℓ*=4, L*=4, c*=$100"),
    ("LL-4", "ℓ*=4.8, L*=3.2, c*=$120. Yes — more leisure"),
    ("LL-5", "ℓ*≈15.5, L*≈8.5, c*≈$187.50"),
    ("LL-6", "(a) ℓ*=6, L*=4  (b) ℓ*=7.5, L*=2.5  (c) Works LESS as w rises"),
]


def write_lines(p, x, y, lines, size=11, color=(0, 0, 0), leading=15):
    for line in lines:
        p.insert_text((x, y), line, fontsize=size, fontname="helv", color=color)
        y += leading
    return y


def problem_page(out, prob, num):
    p = out.new_page(width=PW, height=PH)
    p.insert_text((40, 45), f"Problem {num}: {prob['id']}", fontsize=14, fontname="helv", color=COLOR)
    p.insert_text((40, 62), prob["source"], fontsize=9, fontname="helv", color=MUTED)
    y = 90
    for para in prob["text"].split("\n"):
        if not para.strip():
            y += 8
            continue
        wrapped = textwrap.wrap(para, width=85) or [""]
        y = write_lines(p, 40, y, wrapped, size=11)
    y += 20
    p.insert_text((40, y), "Show your work below:", fontsize=10, fontname="helv", color=MUTED)
    y += 25
    for _ in range(14):
        p.draw_line((40, y), (PW - 40, y), color=(0.8, 0.8, 0.8), width=0.5)
        y += 28


def build_pdf():
    out = pymupdf.open()

    # Cover
    p = out.new_page(width=PW, height=PH)
    p.insert_text((72, 100), "ECON 351 — Labor-Leisure Problems", fontsize=22, fontname="helv", color=COLOR)
    p.insert_text((72, 135), "All practice problems + drills to solve", fontsize=13, fontname="helv")
    y = 180
    p.insert_text((72, y), "Sources checked (uploaded course materials):", fontsize=11, fontname="helv", color=COLOR)
    y += 22
    for src, note in SOURCES_CHECKED:
        p.insert_text((72, y), f"  • {src}: {note}", fontsize=9, fontname="helv")
        y += 14
    y += 16
    p.insert_text((72, y), f"{len(PROBLEMS)} problems in this PDF (2 from practice tests + 4 extra drills).", fontsize=10, fontname="helv")

    # Formula sheet
    p = out.new_page(width=PW, height=PH)
    p.insert_text((40, 45), "Labor-Leisure Formula Sheet", fontsize=14, fontname="helv", color=COLOR)
    y = 75
    for f in FORMULAS:
        p.insert_text((40, y), f, fontsize=10, fontname="helv")
        y += 16

    # Problems
    for i, prob in enumerate(PROBLEMS, 1):
        problem_page(out, prob, i)

    # Answer key
    p = out.new_page(width=PW, height=PH)
    p.insert_text((40, 45), "Answer Key", fontsize=14, fontname="helv", color=COLOR)
    y = 75
    for pid, ans in ANSWERS:
        p.insert_text((40, y), f"{pid}:", fontsize=11, fontname="helv", color=COLOR)
        y += 14
        for line in textwrap.wrap(ans, width=90):
            p.insert_text((55, y), line, fontsize=10, fontname="helv")
            y += 13
        y += 8

    out.save(OUT, garbage=4, deflate=True)
    print(f"Saved: {OUT} ({len(out)} pages)")


if __name__ == "__main__":
    build_pdf()
