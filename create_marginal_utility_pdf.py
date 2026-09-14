#!/usr/bin/env python3
"""Build Marginal_Utility_Guide.pdf — total utility, MU, second derivative, and graphs."""

import os
import textwrap

import matplotlib.pyplot as plt
import numpy as np
import pymupdf

OUT = "/workspace/Marginal_Utility_Guide.pdf"
GRAPH_DIR = "/workspace/mu_graphs"
PW, PH = 612, 792
COLOR = (0.12, 0.31, 0.47)
MUTED = (0.45, 0.45, 0.45)
ACCENT = (0.55, 0.15, 0.15)

FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_NAME = "DejaVu"
FONT_NAME_BOLD = "DejaVu-Bold"

os.makedirs(GRAPH_DIR, exist_ok=True)


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
            y = write_paragraph(
                p, 60, y, line, size=10, width=78, color=ACCENT,
                bold=line.startswith("KEY") or line.startswith("NEGATIVE") or line.startswith("POSITIVE") or line.startswith("NEUTRAL"),
            )
        p.draw_rect(pymupdf.Rect(48, box_y0 - 8, PW - 48, y + 8), color=COLOR, width=0.8)
    return p


def make_graph_pair(tag, u_fn, mu_fn, title, u_label, mu_label, color):
    """Create side-by-side Total Utility and Marginal Utility graphs."""
    x = np.linspace(0.5, 5, 200)
    tu = u_fn(x)
    mu = mu_fn(x)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    fig.suptitle(title, fontsize=14, fontweight="bold", color="#1f4e79")

    axes[0].plot(x, tu, color=color, linewidth=2.5)
    axes[0].set_title("Total Utility U(x)", fontsize=11, fontweight="bold")
    axes[0].set_xlabel("Quantity / Income")
    axes[0].set_ylabel("Total Utility")
    axes[0].grid(True, alpha=0.3)
    axes[0].text(0.04, 0.95, u_label, transform=axes[0].transAxes, va="top", fontsize=9,
                 bbox=dict(boxstyle="round", facecolor="white", alpha=0.85))

    axes[1].plot(x, mu, color=color, linewidth=2.5)
    axes[1].set_title("Marginal Utility MU = U'(x)", fontsize=11, fontweight="bold")
    axes[1].set_xlabel("Quantity / Income")
    axes[1].set_ylabel("Marginal Utility")
    axes[1].grid(True, alpha=0.3)
    axes[1].text(0.04, 0.95, mu_label, transform=axes[1].transAxes, va="top", fontsize=9,
                 bbox=dict(boxstyle="round", facecolor="white", alpha=0.85))

    plt.tight_layout()
    path = os.path.join(GRAPH_DIR, f"{tag}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def generate_graphs():
    paths = {}
    paths["concave"] = make_graph_pair(
        "risk_averse",
        u_fn=lambda x: np.sqrt(x),
        mu_fn=lambda x: 0.5 / np.sqrt(x),
        title="Risk Averse: Concave Utility (u'' < 0)",
        u_label="Concave TU curve\n(bends downward)",
        mu_label="MU decreasing\n(slopes down)",
        color="#1f77b4",
    )
    paths["linear"] = make_graph_pair(
        "risk_neutral",
        u_fn=lambda x: x,
        mu_fn=lambda x: np.ones_like(x),
        title="Risk Neutral: Linear Utility (u'' = 0)",
        u_label="Straight TU line",
        mu_label="Flat MU line\n(constant)",
        color="#2ca02c",
    )
    paths["convex"] = make_graph_pair(
        "risk_loving",
        u_fn=lambda x: x ** 2,
        mu_fn=lambda x: 2 * x,
        title="Risk Loving: Convex Utility (u'' > 0)",
        u_label="Convex TU curve\n(bends upward)",
        mu_label="MU increasing\n(slopes up)",
        color="#d62728",
    )
    return paths


def graph_page(out, title, notes, graph_path):
    p = out.new_page(width=PW, height=PH)
    setup_page_fonts(p)
    y = write_lines(p, 48, 40, [title], size=15, color=COLOR, bold=True)
    y += 8
    for note in notes:
        y = write_paragraph(p, 48, y, note, size=10, width=90)
    if os.path.exists(graph_path):
        rect = pymupdf.Rect(36, y + 10, PW - 36, PH - 36)
        p.insert_image(rect, filename=graph_path)
    return p


def build_pdf():
    graphs = generate_graphs()
    out = pymupdf.open()

    p = out.new_page(width=PW, height=PH)
    setup_page_fonts(p)
    write_lines(p, 72, 100, ["ECON 351 - Marginal Utility Guide"], size=24, color=COLOR, bold=True)
    write_lines(p, 72, 140, ["Total Utility, Marginal Utility, and the Second Derivative"], size=14)
    y = 200
    write_lines(p, 72, y, ["What this guide covers:"], size=12, color=COLOR, bold=True)
    y += 22
    for item in [
        "Total Utility (TU) - overall satisfaction from wealth or goods",
        "Marginal Utility (MU) - extra satisfaction from one more unit (1st derivative)",
        "Second derivative - whether MU is increasing, decreasing, or flat",
        "Graphs for concave, linear, and convex utility (risk averse / neutral / loving)",
    ]:
        y = write_lines(p, 84, y, [item], size=11)

    section_page(
        out,
        "1. Total Utility (TU)",
        "Total Utility is the overall satisfaction derived from a given amount of wealth or goods.",
        bullets=[
            "TU(x) = total happiness at quantity x",
            "Shown as the height of the utility curve",
        ],
        box=["Example: TU(1) = 10 and TU(2) = 25 means 2 units give 25 total utils."],
    )

    section_page(
        out,
        "2. Marginal Utility (MU) - First Derivative",
        "Marginal Utility is the additional satisfaction gained from getting exactly one more unit.",
        bullets=[
            "MU = u'(x) = dU/dx",
            "Discrete: MU at unit 2 = TU(2) - TU(1)",
            "MU is the slope of the Total Utility curve",
        ],
        box=["Example: TU(1)=10, TU(2)=20 -> MU at unit 2 = 10 additional utils."],
    )

    section_page(
        out,
        "3. Second Derivative - Is MU Increasing?",
        (
            "The Second Derivative measures the rate at which marginal utility is changing. "
            "It tells you whether satisfaction from each extra unit is accelerating, slowing down, or staying flat."
        ),
        bullets=[
            "Second derivative > 0  -> MU is INCREASING",
            "Second derivative < 0  -> MU is DECREASING",
            "Second derivative = 0  -> MU is FLAT",
        ],
        box=[
            "KEY EXAMPLE (increasing marginal utility):",
            "MU at unit 1 = 10 utility increase",
            "MU at unit 2 = 20 utility increase",
            "MU went from 10 to 20 -> marginal utility is increasing -> u'' > 0 -> risk-loving",
        ],
    )

    section_page(
        out,
        "4. Risk Attitudes from Utility Shape",
        "Match the shape of utility to MU and the sign of the second derivative:",
        box=[
            "NEGATIVE (u'' < 0): Concave utility. MU is going DOWN. Second derivative is negative because MU is decreasing. -> Risk averse",
            "POSITIVE (u'' > 0): Convex utility. MU is going UP. MU increases faster every unit. -> Risk loving",
            "NEUTRAL (u'' = 0): Linear utility. Flat MU line. Second derivative is 0. -> Risk neutral",
        ],
    )

    graph_page(
        out,
        "5. Graph: Risk Averse (Concave Utility, u'' < 0)",
        [
            "Utility function example: U(x) = sqrt(x)",
            "Total Utility: concave curve (bends downward)",
            "Marginal Utility: decreasing line (each extra unit adds less)",
            "u'' < 0 because MU is falling as x rises",
        ],
        graphs["concave"],
    )

    graph_page(
        out,
        "6. Graph: Risk Neutral (Linear Utility, u'' = 0)",
        [
            "Utility function example: U(x) = x",
            "Total Utility: straight line",
            "Marginal Utility: flat horizontal line (constant MU every unit)",
            "u'' = 0 because MU never changes",
        ],
        graphs["linear"],
    )

    graph_page(
        out,
        "7. Graph: Risk Loving (Convex Utility, u'' > 0)",
        [
            "Utility function example: U(x) = x^2",
            "Total Utility: convex curve (bends upward)",
            "Marginal Utility: increasing line (each extra unit adds MORE)",
            "u'' > 0 because MU is rising - e.g. MU at 1 could be 10, at 2 could be 20",
        ],
        graphs["convex"],
    )

    p = out.new_page(width=PW, height=PH)
    setup_page_fonts(p)
    y = write_lines(p, 48, 48, ["8. Quick Reference Table"], size=16, color=COLOR, bold=True)
    y += 20
    rows = [
        ("Shape", "MU behavior", "u'' sign", "Risk attitude", "Example U(x)"),
        ("Concave", "MU decreasing", "Negative", "Risk averse", "sqrt(x)"),
        ("Linear", "MU flat", "Zero", "Risk neutral", "x"),
        ("Convex", "MU increasing", "Positive", "Risk loving", "x^2"),
    ]
    col_x = [48, 130, 230, 330, 430]
    for r, row in enumerate(rows):
        bold = r == 0
        for c, val in enumerate(row):
            write_lines(p, col_x[c], y, [val], size=9, bold=bold, color=COLOR if r == 0 else (0, 0, 0))
        y += 18 if r == 0 else 24
    y += 16
    write_paragraph(
        p, 48, y,
        "Remember: second derivative tells you if MU is increasing or decreasing.\n"
        "If MU at 1 = 10 and MU at 2 = 20, MU is increasing -> convex utility -> risk-loving.",
        size=11, color=ACCENT,
    )

    out.save(OUT, garbage=4, deflate=True)
    print(f"Saved: {OUT} ({len(out)} pages)")


if __name__ == "__main__":
    build_pdf()
