#!/usr/bin/env python3
"""Build Marginal_Utility_Guide.pdf — total utility, MU, and second derivative."""

import textwrap
import pymupdf

OUT = "/workspace/Marginal_Utility_Guide.pdf"
PW, PH = 612, 792
COLOR = (0.12, 0.31, 0.47)
MUTED = (0.45, 0.45, 0.45)
ACCENT = (0.55, 0.15, 0.15)

FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_NAME = "DejaVu"
FONT_NAME_BOLD = "DejaVu-Bold"


def setup_page_fonts(page):
    page.insert_font(fontname=FONT_NAME, fontfile=FONT_REG)
    page.insert_font(fontname=FONT_NAME_BOLD, fontfile=FONT_BOLD)


def write_lines(page, x, y, lines, size=11, color=(0, 0, 0), leading=16, bold=False):
    font = FONT_NAME_BOLD if bold else FONT_NAME
    for line in lines:
        page.insert_text((x, y), line, fontsize=size, fontname=font, color=color)
        y += leading
    return y


def write_paragraph(page, x, y, text, size=11, width=85, leading=16, color=(0, 0, 0), bold=False):
    for para in text.split("\n"):
        if not para.strip():
            y += 8
            continue
        wrapped = textwrap.wrap(para, width=width) or [""]
        y = write_lines(page, x, y, wrapped, size=size, color=color, leading=leading, bold=bold)
    return y


def section_page(out, title, body, bullets=None, box=None):
    p = out.new_page(width=PW, height=PH)
    setup_page_fonts(p)
    y = write_lines(p, 48, 48, [title], size=16, color=COLOR, bold=True)
    y += 10
    y = write_paragraph(p, 48, y, body, size=11)
    if bullets:
        y += 8
        for b in bullets:
            y = write_paragraph(p, 60, y, f"- {b}", size=10, width=80)
    if box:
        y += 16
        box_y0 = y
        for line in box:
            y = write_paragraph(p, 60, y, line, size=10, width=78, color=ACCENT, bold=("KEY" in line or "Example" in line))
        p.draw_rect(pymupdf.Rect(48, box_y0 - 8, PW - 48, y + 8), color=COLOR, width=0.8)
    return p


def build_pdf():
    out = pymupdf.open()

    p = out.new_page(width=PW, height=PH)
    setup_page_fonts(p)
    write_lines(p, 72, 110, ["ECON 351 - Marginal Utility Guide"], size=24, color=COLOR, bold=True)
    write_lines(p, 72, 150, ["Total Utility, Marginal Utility, and the Second Derivative"], size=14)
    y = 210
    write_lines(p, 72, y, ["What this guide covers:"], size=12, color=COLOR, bold=True)
    y += 22
    for item in [
        "Total Utility (TU) - overall satisfaction from wealth or goods",
        "Marginal Utility (MU) - extra satisfaction from one more unit (1st derivative)",
        "Second derivative - whether MU is rising, falling, or flat",
        "How this connects to risk attitudes on the exam",
    ]:
        y = write_lines(p, 84, y, [item], size=11)

    section_page(
        out,
        "1. Total Utility (TU)",
        (
            "Total Utility is the overall satisfaction you get from a given amount of "
            "wealth or goods.\n\n"
            "Think of it as the height of your happiness at a specific quantity."
        ),
        bullets=[
            "TU(0) = satisfaction from zero units",
            "TU(3) = total satisfaction from 3 units",
            "TU generally rises as you get more, but not always at the same rate",
        ],
        box=[
            "Example: If 1 slice of pizza gives 10 utils total and 2 slices give 25 utils total,",
            "then TU(1) = 10 and TU(2) = 25.",
        ],
    )

    section_page(
        out,
        "2. Marginal Utility (MU) - First Derivative",
        (
            "Marginal Utility is the additional satisfaction from getting exactly ONE more unit.\n\n"
            "In calculus terms: MU = dU/dx (or u'(I) for income).\n\n"
            "Discrete version (what you often use on homework):"
        ),
        bullets=[
            "MU at unit 2 = TU(2) - TU(1)",
            "MU at unit 3 = TU(3) - TU(2)",
            "MU answers: 'How much extra utility do I get from the next unit?'",
        ],
        box=[
            "Example: TU(1) = 10 and TU(2) = 20",
            "MU at unit 2 = 20 - 10 = 10 additional utils from the 2nd unit.",
        ],
    )

    section_page(
        out,
        "3. Second Derivative - Is MU Increasing or Decreasing?",
        (
            "The second derivative measures the rate at which marginal utility is changing.\n\n"
            "It tells you whether satisfaction from each extra unit is:"
        ),
        bullets=[
            "Accelerating (MU rising) -> second derivative > 0 -> risk-loving",
            "Slowing down (MU falling) -> second derivative < 0 -> risk-averse",
            "Staying flat (MU constant) -> second derivative = 0 -> risk-neutral",
        ],
        box=[
            "KEY EXAMPLE (increasing marginal utility):",
            "At unit 1, MU = 10 additional utils (going from 0 to 1 gives +10).",
            "At unit 2, MU = 20 additional utils (going from 1 to 2 gives +20).",
            "MU went from 10 to 20 -> marginal utility is INCREASING.",
            "So the second derivative is positive -> risk-loving preferences.",
        ],
    )

    section_page(
        out,
        "4. Compare: Decreasing vs Increasing Marginal Utility",
        (
            "Most exam utility functions show diminishing marginal utility (risk averse)."
        ),
        bullets=[
            "Risk averse: MU falls as you get more (e.g. MU = 9/I, or u = sqrt(I))",
            "Risk neutral: MU stays constant (e.g. u = I, so MU = 1 always)",
            "Risk loving: MU rises as you get more (e.g. u = I^2, so MU = 2I rises with I)",
        ],
        box=[
            "Decreasing MU example: TU(1)=10, TU(2)=18 -> MU at 2 = 8 (less than 10).",
            "Increasing MU example: TU(1)=10, TU(2)=30 -> MU at 2 = 20 (more than 10).",
            "Exam shortcut: u''(I) < 0 risk averse | u''(I) = 0 risk neutral | u''(I) > 0 risk loving",
        ],
    )

    p = out.new_page(width=PW, height=PH)
    setup_page_fonts(p)
    y = write_lines(p, 48, 48, ["5. Quick Reference Table"], size=16, color=COLOR, bold=True)
    y += 20
    rows = [
        ("Concept", "Meaning", "Calculus", "Risk attitude"),
        ("Total Utility", "Overall satisfaction", "U(x) or u(I)", "-"),
        ("Marginal Utility", "Extra utility from +1 unit", "u'(I) or dU/dx", "-"),
        ("MU decreasing", "Each next unit adds less", "u''(I) < 0", "Risk averse"),
        ("MU constant", "Each next unit adds same", "u''(I) = 0", "Risk neutral"),
        ("MU increasing", "Each next unit adds more", "u''(I) > 0", "Risk loving"),
    ]
    col_x = [48, 155, 300, 430]
    for r, row in enumerate(rows):
        bold = r == 0
        for c, val in enumerate(row):
            write_lines(p, col_x[c], y, [val], size=10 if r else 10, bold=bold,
                        color=COLOR if r == 0 else (0, 0, 0))
        y += 18 if r == 0 else 22
    y += 20
    write_paragraph(
        p, 48, y,
        "Remember: the second derivative is about whether MU itself is going up or down.\n"
        "If MU at 1 is 10 and MU at 2 is 20, MU is increasing -> risk-loving.",
        size=11, color=ACCENT, bold=False,
    )

    out.save(OUT, garbage=4, deflate=True)
    print(f"Saved: {OUT} ({len(out)} pages)")


if __name__ == "__main__":
    build_pdf()
