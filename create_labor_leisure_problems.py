#!/usr/bin/env python3
"""Extract labor-leisure problems from practice tests + add extra problems to solve."""

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

OUT = "/workspace/Labor_Leisure_Problems.xlsx"
PDF_URL = "https://github.com/vengeanceaiUSC/econtest/releases/download/exam-prep-download/Labor_Leisure_Problems.pdf"
LINK_FONT = Font(color="0563C1", underline="single")

HEADER_FILL = PatternFill("solid", fgColor="1F4E79")
GREEN_FILL = PatternFill("solid", fgColor="C6E0B4")
YELLOW_FILL = PatternFill("solid", fgColor="FFF2CC")
HEADER_FONT = Font(bold=True, color="FFFFFF", size=11)
BOLD = Font(bold=True)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
thin = Side(style="thin", color="AAAAAA")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

# From practice tests (Q3 & Q4 on Tests 1, 2, 3 — same 2 problems)
PRACTICE_PROBLEMS = [
    {
        "id": "LL-1 (Practice Test Q3)",
        "source": "All 3 practice tests — Q3",
        "bank_id": "Q021",
        "problem": (
            "Maria has 16 hours/day for leisure (l) and work. "
            "Wage w = $20/hr, non-labor income V = $80. "
            "Utility U(c, l) = c^0.5 * l^0.5 where c = w*(16 - l) + V.\n\n"
            "Find: (a) optimal leisure l*, (b) labor hours L*, (c) consumption c*."
        ),
        "hints": "Budget: c = w*(16-l)+V. Optimum: MU_l/MU_c = w. Cobb-Douglas a=b=0.5 -> c = w*l.",
        "answer": "l* = 10 hrs, L* = 6 hrs, c* = $200",
    },
    {
        "id": "LL-2 (Practice Test Q4)",
        "source": "All 3 practice tests — Q4",
        "bank_id": "Q022",
        "problem": (
            "Same setup as LL-1, but wage rises to w = $30/hr.\n\n"
            "Find: (a) new l*, (b) new L*, (c) new c*. "
            "Does Maria work more or less than when w = $20?"
        ),
        "hints": "Use l* = (w*T + V) / (2w) with T = 16. Compare L* to LL-1.",
        "answer": "l* = 9.33 hrs, L* = 6.67 hrs, c* = $360. Works MORE.",
    },
]

# Extra problems (not in uploads — written for practice)
EXTRA_PROBLEMS = [
    {
        "id": "LL-3",
        "source": "Extra practice (study sheet)",
        "bank_id": "—",
        "problem": (
            "Alex has 8 hours/day (T = 8). Wage w = $25/hr, V = $0. "
            "U(c, l) = c^0.5 * l^0.5, c = w*(8 - l) + V.\n\n"
            "Find l*, L*, and c*."
        ),
        "hints": "l* = (w*T + V)/(2w) when a = b = 0.5.",
        "answer": "l* = 4 hrs, L* = 4 hrs, c* = $100",
    },
    {
        "id": "LL-4",
        "source": "Extra practice (study sheet)",
        "bank_id": "—",
        "problem": (
            "Same as LL-3 but V = $40 (lottery winnings). w = $25, T = 8.\n\n"
            "Find l*, L*, c*. Did leisure increase vs LL-3?"
        ),
        "hints": "Higher V shifts budget outward -> more leisure for Cobb-Douglas.",
        "answer": "l* = 4.8 hrs, L* = 3.2 hrs, c* = $120. Yes - more leisure.",
    },
    {
        "id": "LL-5",
        "source": "Extra practice (study sheet)",
        "bank_id": "—",
        "problem": (
            "Jordan: T = 24 hrs, w = $15/hr, V = $60, U(c, l) = c^0.25 * l^0.75 "
            "(loves leisure more than Maria).\n\n"
            "Find l* using MU_l/MU_c = w."
        ),
        "hints": "MRS = (0.75/0.25)*(c/l) = 3c/l = w -> c = (w/3)*l. Plug into budget.",
        "answer": "l* = 15.5 hrs, L* = 8.5 hrs, c* = $187.50",
    },
    {
        "id": "LL-6",
        "source": "Extra practice (study sheet)",
        "bank_id": "—",
        "problem": (
            "Sam: T = 10 hrs, V = $100, U(c, l) = c^0.5 * l^0.5.\n"
            "(a) w = $10: find l*, L*\n"
            "(b) w = $40: find l*, L*\n"
            "(c) As wage rises, work more or less?"
        ),
        "hints": "l* = (w*T+V)/(2w). Compare L* = T - l*.",
        "answer": "(a) l*=6, L*=4  (b) l*=7.5, L*=2.5  (c) Works LESS",
    },
]

LECTURE_NOTE = (
    "The uploaded file 'Econ351Lecture_2__Chapter_9___2__ea6a.pdf' is Chapter 9 "
    "(Uncertainty & Risk) only. It contains NO labor-leisure problems. "
    "Labor-leisure is Chapter 4 consumer theory."
)

wb = Workbook()

# Sheet 1: Problems to solve
ws = wb.active
ws.title = "Problems to Solve"
ws["A1"] = "Labor-Leisure Problems — ECON 351"
ws["A1"].font = Font(bold=True, size=14)
ws.merge_cells("A1:F1")
ws["A2"] = LECTURE_NOTE
ws["A2"].font = Font(italic=True, color="666666", size=10)
ws.merge_cells("A2:F2")
pdf_link = ws.cell(row=3, column=1, value="Full PDF version (all problems + answer key):")
pdf_link.font = BOLD
link = ws.cell(row=3, column=3, value="Labor_Leisure_Problems.pdf")
link.hyperlink = PDF_URL
link.font = LINK_FONT
ws.merge_cells("A3:B3")
ws.merge_cells("C3:F3")

headers = ["#", "ID", "Source", "Problem (solve on paper)", "Hints", "Your work space"]
for c, h in enumerate(headers, 1):
    cell = ws.cell(row=5, column=c, value=h)
    cell.font = HEADER_FONT
    cell.fill = HEADER_FILL
    cell.alignment = CENTER
    cell.border = BORDER

all_probs = PRACTICE_PROBLEMS + EXTRA_PROBLEMS
for i, p in enumerate(all_probs, 1):
    r = i + 5
    fill = YELLOW_FILL if "Practice Test" in p["source"] else GREEN_FILL
    row = [i, p["id"], p["source"], p["problem"], p["hints"], ""]
    for c, val in enumerate(row, 1):
        cell = ws.cell(row=r, column=c, value=val)
        cell.fill = fill
        cell.border = BORDER
        cell.alignment = WRAP

ws.column_dimensions["A"].width = 4
ws.column_dimensions["B"].width = 22
ws.column_dimensions["C"].width = 28
ws.column_dimensions["D"].width = 55
ws.column_dimensions["E"].width = 35
ws.column_dimensions["F"].width = 25
ws.freeze_panes = "A6"
ws.row_dimensions[6].height = 80
ws.row_dimensions[7].height = 70
for r in range(8, 5 + len(all_probs) + 1):
    ws.row_dimensions[r].height = 70

# Sheet 2: Answer key
ws2 = wb.create_sheet("Answer Key")
ws2["A1"] = "Answer Key — Labor-Leisure"
ws2["A1"].font = Font(bold=True, size=14)
headers2 = ["ID", "Bank ID", "Answer / Solution sketch"]
for c, h in enumerate(headers2, 1):
    cell = ws2.cell(row=3, column=c, value=h)
    cell.font = HEADER_FONT
    cell.fill = HEADER_FILL
    cell.alignment = CENTER
    cell.border = BORDER
for i, p in enumerate(all_probs, 4):
    for c, val in enumerate([p["id"], p.get("bank_id", ""), p["answer"]], 1):
        cell = ws2.cell(row=i, column=c, value=val)
        cell.border = BORDER
        cell.alignment = WRAP
ws2.column_dimensions["A"].width = 22
ws2.column_dimensions["B"].width = 10
ws2.column_dimensions["C"].width = 60

# Sheet 3: Formulas
ws3 = wb.create_sheet("Formula Sheet")
formulas = [
    ("Setup", "T = total hours, l = leisure, L = labor hours, L = T - l"),
    ("Budget", "c = w*L + V = w*(T - l) + V"),
    ("Optimum", "MU_l / MU_c = w  (MRS = wage)"),
    ("Cobb-Douglas U = c^a * l^b", "At optimum: b*c = a*w*l"),
    ("Cobb-Douglas a = b = 0.5", "c = w*l  and  l* = (w*T + V) / (2w)"),
    ("Consumption", "c* = w*l* + V  (or w*L* + V)"),
]
ws3["A1"] = "Labor-Leisure Formula Sheet"
ws3["A1"].font = Font(bold=True, size=14)
for i, (topic, formula) in enumerate(formulas, 3):
    ws3.cell(row=i, column=1, value=topic).font = BOLD
    ws3.cell(row=i, column=2, value=formula).alignment = WRAP
ws3.column_dimensions["A"].width = 28
ws3.column_dimensions["B"].width = 50

wb.save(OUT)
print(f"Saved: {OUT} ({len(all_probs)} problems)")
