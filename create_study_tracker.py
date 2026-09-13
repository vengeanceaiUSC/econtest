#!/usr/bin/env python3
"""Create Study_Tracker.xlsx — exam topic checklist with green checkoffs."""

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from exam_config import EXAM_STRUCTURE

OUT = "/workspace/Study_Tracker.xlsx"

# Categories left unchecked (not green)
SKIP_GREEN = {"Labor-Leisure", "Diversification"}

HEADER_FILL = PatternFill("solid", fgColor="1F4E79")
CH4_FILL = PatternFill("solid", fgColor="D6E4F0")
CH9_FILL = PatternFill("solid", fgColor="E2EFDA")
GREEN_FILL = PatternFill("solid", fgColor="C6EFCE")  # Excel green
WHITE_FILL = PatternFill("solid", fgColor="FFFFFF")
HEADER_FONT = Font(bold=True, color="FFFFFF", size=11)
BOLD = Font(bold=True)
CHECK_FONT = Font(bold=True, size=14, color="006100")
WRAP = Alignment(wrap_text=True, vertical="center")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
thin = Side(style="thin", color="AAAAAA")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

wb = Workbook()
ws = wb.active
ws.title = "Topic Checklist"

ws["A1"] = "ECON 351 — Exam Topic Tracker"
ws["A1"].font = Font(bold=True, size=14)
ws.merge_cells("A1:E1")

headers = ["Chapter", "Category", "Questions on Test", "Status", "Notes"]
for c, h in enumerate(headers, 1):
    cell = ws.cell(row=3, column=c, value=h)
    cell.font = HEADER_FONT
    cell.fill = HEADER_FILL
    cell.alignment = CENTER
    cell.border = BORDER

row = 4
ch4_total = ch9_total = 0
for section in EXAM_STRUCTURE:
    ch = section["ch"]
    cat = section["category"]
    count = section["count"]
    if ch == 4:
        ch4_total += count
    else:
        ch9_total += count

    done = cat not in SKIP_GREEN
    status = "✓ Done" if done else "— Not yet"
    notes = "" if done else "Still need to practice"

    base_fill = CH4_FILL if ch == 4 else CH9_FILL
    row_fill = GREEN_FILL if done else base_fill

    values = [f"Ch. {ch}", cat, count, status, notes]
    for c, val in enumerate(values, 1):
        cell = ws.cell(row=row, column=c, value=val)
        cell.fill = row_fill
        cell.border = BORDER
        cell.alignment = WRAP if c != 4 else CENTER
        if c == 4 and done:
            cell.font = CHECK_FONT

    row += 1

# Totals
ws.cell(row=row, column=1, value="").border = BORDER
ws.cell(row=row, column=2, value="Ch. 4 Total").font = BOLD
ws.cell(row=row, column=3, value=ch4_total).font = BOLD
ws.cell(row=row, column=4, value="12").font = BOLD
for c in range(1, 6):
    ws.cell(row=row, column=c).border = BORDER
    ws.cell(row=row, column=c).fill = CH4_FILL
row += 1

ws.cell(row=row, column=2, value="Ch. 9 Total").font = BOLD
ws.cell(row=row, column=3, value=ch9_total).font = BOLD
ws.cell(row=row, column=4, value="12").font = BOLD
for c in range(1, 6):
    ws.cell(row=row, column=c).border = BORDER
    ws.cell(row=row, column=c).fill = CH9_FILL
row += 1

ws.cell(row=row, column=2, value="GRAND TOTAL").font = BOLD
ws.cell(row=row, column=3, value=24).font = BOLD
for c in range(1, 6):
    ws.cell(row=row, column=c).border = BORDER
    ws.cell(row=row, column=c).fill = PatternFill("solid", fgColor="FFF2CC")

# Legend
row += 2
ws.cell(row=row, column=1, value="Legend:").font = BOLD
row += 1
ws.cell(row=row, column=1, value="Green = reviewed / done")
ws.cell(row=row, column=1).fill = GREEN_FILL
row += 1
ws.cell(row=row, column=1, value="Not green = still need practice (Labor-Leisure, Diversification)")
ws.cell(row=row, column=1).fill = CH4_FILL

ws.column_dimensions["A"].width = 10
ws.column_dimensions["B"].width = 36
ws.column_dimensions["C"].width = 18
ws.column_dimensions["D"].width = 14
ws.column_dimensions["E"].width = 28
ws.freeze_panes = "A4"

wb.save(OUT)
print(f"Saved: {OUT}")
