#!/usr/bin/env python3
"""Build Labor_Leisure_Problems.pdf — all labor-leisure problems for the course."""

import textwrap
import pymupdf

OUT = "/workspace/Labor_Leisure_Problems.pdf"
PW, PH = 612, 792
COLOR = (0.12, 0.31, 0.47)
MUTED = (0.45, 0.45, 0.45)

FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_NAME = "DejaVu"
FONT_NAME_BOLD = "DejaVu-Bold"

SOURCES_CHECKED = [
    ("Homework 1 Ch.4", "No labor-leisure exercises"),
    ("Homework 2 Ch.9", "No labor-leisure (Ch.9 uncertainty only)"),
    ("Sample Questions Ch.4", "No labor-leisure questions found"),
    ("Sample Questions Ch.9", "No labor-leisure questions found"),
    ("Mock Midterm 1", "No labor-leisure questions found"),
    ("Econ351 Lecture (Ch.9 upload)", "Chapter 9 only - no labor-leisure"),
    ("Practice Tests 1-3", "Q3 & Q4 - Maria problems (included below)"),
]

FORMULAS = [
    "Time: T = L + l  (total hours = labor + leisure; l = leisure hours)",
    "Budget: c = w*L + V = w*(T - l) + V",
    "Optimum: MU_l / MU_c = w",
    "Cobb-Douglas U = c^a * l^b: at optimum b*c = a*w*l",
    "Special case a = b = 0.5: c = w*l  and  l* = (w*T + V) / (2w)",
    "Labor hours: L* = T - l*",
    "Consumption: c* = w*l* + V",
]

PROBLEMS = [
    {
        "id": "LL-1",
        "source": "Practice Tests 1, 2, 3 - Question 3",
        "text": (
            "Maria has 16 hours per day for leisure (l) and work.\n"
            "Wage w = $20/hr, non-labor income V = $80.\n"
            "Utility U(c, l) = c^0.5 * l^0.5, where c = w*(16 - l) + V.\n\n"
            "(a) Write the budget constraint.\n"
            "(b) Find optimal leisure l*.\n"
            "(c) Find labor hours L* and consumption c*."
        ),
    },
    {
        "id": "LL-2",
        "source": "Practice Tests 1, 2, 3 - Question 4",
        "text": (
            "Same setup as LL-1, but wage rises to w = $30/hr.\n\n"
            "(a) Find new l*, L*, and c*.\n"
            "(b) Does Maria work more or less than when w = $20? Explain."
        ),
    },
    {
        "id": "LL-3",
        "source": "Extra drill - standard Cobb-Douglas",
        "text": (
            "Alex has T = 8 hours/day, w = $25/hr, V = $0.\n"
            "U(c, l) = c^0.5 * l^0.5, where c = w*(8 - l).\n\n"
            "Find l*, L*, and c*."
        ),
    },
    {
        "id": "LL-4",
        "source": "Extra drill - non-labor income change",
        "text": (
            "Same as LL-3 but V = $40 (lottery winnings).\n\n"
            "Find l*, L*, c*. Did leisure increase compared to LL-3?"
        ),
    },
    {
        "id": "LL-5",
        "source": "Extra drill - leisure-loving preferences",
        "text": (
            "Jordan: T = 24 hrs, w = $15/hr, V = $60.\n"
            "U(c, l) = c^0.25 * l^0.75 (more leisure-loving than Maria).\n\n"
            "Use MU_l / MU_c = w to find l*, L*, c*."
        ),
    },
    {
        "id": "LL-6",
        "source": "Extra drill - wage comparative statics",
        "text": (
            "Sam: T = 10 hrs, V = $100, U(c, l) = c^0.5 * l^0.5.\n"
            "(a) If w = $10, find l* and L*.\n"
            "(b) If w = $40, find l* and L*.\n"
            "(c) As wage rises, does Sam work more or less?"
        ),
    },
]

ANSWERS = [
    ("LL-1", "BC: c = 20*(16-l)+80. l*=10, L*=6, c*=$200"),
    ("LL-2", "l*=9.33, L*=6.67, c*=$360. Works MORE (w up -> l* up but L*=T-l* also up for a=b=0.5)"),
    ("LL-3", "l*=4, L*=4, c*=$100"),
    ("LL-4", "l*=4.8, L*=3.2, c*=$120. Yes - more leisure"),
    ("LL-5", "l*=15.5, L*=8.5, c*=$187.50"),
    ("LL-6", "(a) l*=6, L*=4  (b) l*=7.5, L*=2.5  (c) Works LESS as w rises"),
]


def setup_page_fonts(page):
    page.insert_font(fontname=FONT_NAME, fontfile=FONT_REG)
    page.insert_font(fontname=FONT_NAME_BOLD, fontfile=FONT_BOLD)


def write_lines(page, x, y, lines, size=11, color=(0, 0, 0), leading=15, bold=False):
    font = FONT_NAME_BOLD if bold else FONT_NAME
    for line in lines:
        page.insert_text((x, y), line, fontsize=size, fontname=font, color=color)
        y += leading
    return y


def problem_page(out, prob, num):
    p = out.new_page(width=PW, height=PH)
    setup_page_fonts(p)
    write_lines(p, 40, 45, [f"Problem {num}: {prob['id']}"], size=14, color=COLOR, bold=True)
    write_lines(p, 40, 62, [prob["source"]], size=9, color=MUTED)
    y = 90
    for para in prob["text"].split("\n"):
        if not para.strip():
            y += 8
            continue
        wrapped = textwrap.wrap(para, width=85) or [""]
        y = write_lines(p, 40, y, wrapped, size=11)
    y += 20
    write_lines(p, 40, y, ["Show your work below:"], size=10, color=MUTED)
    y += 25
    for _ in range(14):
        p.draw_line((40, y), (PW - 40, y), color=(0.8, 0.8, 0.8), width=0.5)
        y += 28


def build_pdf():
    out = pymupdf.open()

    p = out.new_page(width=PW, height=PH)
    setup_page_fonts(p)
    write_lines(p, 72, 100, ["ECON 351 - Labor-Leisure Problems"], size=22, color=COLOR, bold=True)
    write_lines(p, 72, 135, ["All practice problems + drills to solve"], size=13)
    y = 180
    write_lines(p, 72, y, ["Sources checked (uploaded course materials):"], size=11, color=COLOR, bold=True)
    y += 22
    for src, note in SOURCES_CHECKED:
        y = write_lines(p, 72, y, [f"  - {src}: {note}"], size=9)
    y += 16
    write_lines(
        p, 72, y,
        [f"{len(PROBLEMS)} problems in this PDF (2 from practice tests + 4 extra drills)."],
        size=10,
    )

    p = out.new_page(width=PW, height=PH)
    setup_page_fonts(p)
    write_lines(p, 40, 45, ["Labor-Leisure Formula Sheet"], size=14, color=COLOR, bold=True)
    y = 75
    for f in FORMULAS:
        y = write_lines(p, 40, y, [f], size=10)

    for i, prob in enumerate(PROBLEMS, 1):
        problem_page(out, prob, i)

    p = out.new_page(width=PW, height=PH)
    setup_page_fonts(p)
    write_lines(p, 40, 45, ["Answer Key"], size=14, color=COLOR, bold=True)
    y = 75
    for pid, ans in ANSWERS:
        y = write_lines(p, 40, y, [f"{pid}:"], size=11, color=COLOR, bold=True)
        y += 14
        for line in textwrap.wrap(ans, width=90):
            y = write_lines(p, 55, y, [line], size=10)
        y += 8

    out.save(OUT, garbage=4, deflate=True)
    print(f"Saved: {OUT} ({len(out)} pages)")


if __name__ == "__main__":
    build_pdf()
