#!/usr/bin/env python3
"""Create Study_Tracker.xlsx — exam topic checklist with green checkoffs."""

import os
import subprocess

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.worksheet.hyperlink import Hyperlink
from exam_config import EXAM_STRUCTURE
from excel_pdf_embed import add_pdf_pages_sheet, package_pdf_in_xlsx

OUT = "/workspace/Study_Tracker.xlsx"
PDF_PATH = "/workspace/Labor_Leisure_Problems.pdf"
DIV_PDF_PATH = "/workspace/Diversification_Variance_Problems.pdf"
MU_PDF_PATH = "/workspace/Marginal_Utility_Guide.pdf"
PREF_PDF_PATH = "/workspace/Assumptions_Preferences_Problems.pdf"
IT_PDF_PATH = "/workspace/Intertemporal_Consumption_Problems.pdf"

PDF_URL = "https://github.com/vengeanceaiUSC/econtest/releases/download/exam-prep-download/Labor_Leisure_Problems.pdf"
LL_XLSX_URL = "https://github.com/vengeanceaiUSC/econtest/releases/download/exam-prep-download/Labor_Leisure_Problems.xlsx"
DIV_PDF_URL = "https://github.com/vengeanceaiUSC/econtest/releases/download/exam-prep-download/Diversification_Variance_Problems.pdf"
DIV_XLSX_URL = "https://github.com/vengeanceaiUSC/econtest/releases/download/exam-prep-download/Diversification_Variance_Problems.xlsx"
MU_PDF_URL = "https://github.com/vengeanceaiUSC/econtest/releases/download/exam-prep-download/Marginal_Utility_Guide.pdf"
MU_XLSX_URL = "https://github.com/vengeanceaiUSC/econtest/releases/download/exam-prep-download/Marginal_Utility_Guide.xlsx"
PREF_PDF_URL = "https://github.com/vengeanceaiUSC/econtest/releases/download/exam-prep-download/Assumptions_Preferences_Problems.pdf"
PREF_XLSX_URL = "https://github.com/vengeanceaiUSC/econtest/releases/download/exam-prep-download/Assumptions_Preferences_Problems.xlsx"
IT_PDF_URL = "https://github.com/vengeanceaiUSC/econtest/releases/download/exam-prep-download/Intertemporal_Consumption_Problems.pdf"
IT_XLSX_URL = "https://github.com/vengeanceaiUSC/econtest/releases/download/exam-prep-download/Intertemporal_Consumption_Problems.xlsx"

SKIP_GREEN = {"Labor-Leisure", "Diversification"}

HEADER_FILL = PatternFill("solid", fgColor="1F4E79")
CH4_FILL = PatternFill("solid", fgColor="D6E4F0")
CH9_FILL = PatternFill("solid", fgColor="E2EFDA")
GREEN_FILL = PatternFill("solid", fgColor="C6EFCE")
HIGHLIGHT_FILL = PatternFill("solid", fgColor="FFF2CC")
HEADER_FONT = Font(bold=True, color="FFFFFF", size=11)
BOLD = Font(bold=True)
CHECK_FONT = Font(bold=True, size=14, color="006100")
LINK_FONT = Font(color="0563C1", underline="single", size=10)
WRAP = Alignment(wrap_text=True, vertical="center")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
thin = Side(style="thin", color="AAAAAA")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)


def set_external_link(cell, url, label):
    cell.value = label
    cell.hyperlink = url
    cell.font = LINK_FONT


def set_sheet_link(cell, sheet_name, label, anchor="A1"):
    cell.value = label
    cell.hyperlink = Hyperlink(ref=cell.coordinate, location=f"'{sheet_name}'!{anchor}")
    cell.font = LINK_FONT


def add_material_links(ws, row, row_fill, sheet_name, pdf_url, pdf_label):
    set_external_link(ws.cell(row=row, column=6), pdf_url, f"Download {pdf_label} PDF")
    ws.cell(row=row, column=6).fill = row_fill
    ws.cell(row=row, column=6).border = BORDER
    set_sheet_link(ws.cell(row=row, column=5), sheet_name, f"View in '{sheet_name}' tab")
    ws.cell(row=row, column=5).fill = row_fill
    ws.cell(row=row, column=5).border = BORDER


PDF_LINKS = [
    ("Assumptions & Preferences", PREF_PDF_URL, PREF_XLSX_URL, "Preferences PDF"),
    ("Intertemporal Consumption", IT_PDF_URL, IT_XLSX_URL, "Intertemporal PDF"),
    ("Labor-Leisure", PDF_URL, LL_XLSX_URL, "Labor-Leisure PDF"),
    ("Diversification & Variance", DIV_PDF_URL, DIV_XLSX_URL, "Diversification PDF"),
    ("Marginal Utility Guide", MU_PDF_URL, MU_XLSX_URL, "Marginal Utility PDF"),
]

wb = Workbook()
links = wb.active
links.title = "PDF LINKS"
links["A1"] = "CLICK THESE LINKS TO OPEN PDFs"
links["A1"].font = Font(bold=True, size=16, color="1F4E79")
links.merge_cells("A1:D1")
links["A2"] = "If a link does not open, copy the URL from column C into your browser."
links["A2"].font = Font(italic=True, size=10, color="666666")
links.merge_cells("A2:D2")
for c, h in enumerate(["Topic", "Open PDF (click)", "Copy URL if link fails", "Workbook tab"], 1):
    cell = links.cell(row=4, column=c, value=h)
    cell.font = HEADER_FONT
    cell.fill = HEADER_FILL
    cell.border = BORDER
for i, (topic, pdf_url, xlsx_url, tab) in enumerate(PDF_LINKS, 5):
    links.cell(row=i, column=1, value=topic).font = BOLD
    set_external_link(links.cell(row=i, column=2), pdf_url, f"OPEN {topic} PDF")
    links.cell(row=i, column=3, value=pdf_url).font = Font(size=9)
    set_sheet_link(links.cell(row=i, column=4), tab, f"Go to {tab}")
    for c in range(1, 5):
        links.cell(row=i, column=c).border = BORDER
        links.cell(row=i, column=c).alignment = WRAP
links.column_dimensions["A"].width = 28
links.column_dimensions["B"].width = 30
links.column_dimensions["C"].width = 70
links.column_dimensions["D"].width = 22

ws = wb.create_sheet("Topic Checklist", 1)

ws["A1"] = "ECON 351 — Exam Topic Tracker"
ws["A1"].font = Font(bold=True, size=14)
ws.merge_cells("A1:F1")
ws["A2"] = "Tip: Use the 'PDF LINKS' tab (first tab) for all study PDFs."
ws["A2"].font = Font(italic=True, size=10, color="C00000")
ws.merge_cells("A2:F2")

headers = ["Chapter", "Category", "Questions on Test", "Status", "Notes", "Practice Materials"]
for c, h in enumerate(headers, 1):
    cell = ws.cell(row=4, column=c, value=h)
    cell.font = HEADER_FONT
    cell.fill = HEADER_FILL
    cell.alignment = CENTER
    cell.border = BORDER

row = 5
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
    materials = ""
    if cat in {"Labor-Leisure", "Diversification", "Risk Attitudes", "Assumptions / Preferences", "Intertemporal Consumption"}:
        notes = "View in workbook tab (col E) or download PDF (col F)"
        materials = "Click Download PDF"

    base_fill = CH4_FILL if ch == 4 else CH9_FILL
    if cat in {"Assumptions / Preferences", "Intertemporal Consumption"}:
        row_fill = HIGHLIGHT_FILL
    else:
        row_fill = GREEN_FILL if done else base_fill

    values = [f"Ch. {ch}", cat, count, status, notes, materials]
    for c, val in enumerate(values, 1):
        cell = ws.cell(row=row, column=c, value=val)
        cell.fill = row_fill
        cell.border = BORDER
        cell.alignment = WRAP if c != 4 else CENTER
        if c == 4 and done:
            cell.font = CHECK_FONT

    if cat == "Labor-Leisure":
        add_material_links(ws, row, row_fill, "Labor-Leisure PDF", PDF_URL, "Labor-Leisure")
    elif cat == "Diversification":
        add_material_links(ws, row, row_fill, "Diversification PDF", DIV_PDF_URL, "Diversification")
    elif cat == "Risk Attitudes":
        add_material_links(ws, row, row_fill, "Marginal Utility PDF", MU_PDF_URL, "Marginal Utility")
    elif cat == "Assumptions / Preferences":
        add_material_links(ws, row, row_fill, "Preferences PDF", PREF_PDF_URL, "Preferences")
    elif cat == "Intertemporal Consumption":
        add_material_links(ws, row, row_fill, "Intertemporal PDF", IT_PDF_URL, "Intertemporal")

    row += 1

# Totals
ws.cell(row=row, column=2, value="Ch. 4 Total").font = BOLD
ws.cell(row=row, column=3, value=ch4_total).font = BOLD
for c in range(1, 7):
    ws.cell(row=row, column=c).border = BORDER
    ws.cell(row=row, column=c).fill = CH4_FILL
row += 1

ws.cell(row=row, column=2, value="Ch. 9 Total").font = BOLD
ws.cell(row=row, column=3, value=ch9_total).font = BOLD
for c in range(1, 7):
    ws.cell(row=row, column=c).border = BORDER
    ws.cell(row=row, column=c).fill = CH9_FILL
row += 1

ws.cell(row=row, column=2, value="GRAND TOTAL").font = BOLD
ws.cell(row=row, column=3, value=24).font = BOLD
for c in range(1, 7):
    ws.cell(row=row, column=c).border = BORDER
    ws.cell(row=row, column=c).fill = PatternFill("solid", fgColor="FFF2CC")

row += 2
ws.cell(row=row, column=1, value="Legend:").font = BOLD
row += 1
ws.cell(row=row, column=1, value="Green = reviewed / done").fill = GREEN_FILL
row += 1
ws.cell(row=row, column=1, value="Not green = still need practice").fill = CH4_FILL

ws.column_dimensions["A"].width = 10
ws.column_dimensions["B"].width = 32
ws.column_dimensions["C"].width = 16
ws.column_dimensions["D"].width = 12
ws.column_dimensions["E"].width = 28
ws.column_dimensions["F"].width = 28
ws.freeze_panes = "A5"

if not os.path.exists(PDF_PATH):
    subprocess.run(["python3", "/workspace/create_labor_leisure_pdf.py"], check=True)
if not os.path.exists(DIV_PDF_PATH):
    subprocess.run(["python3", "/workspace/create_diversification_pdf.py"], check=True)
if not os.path.exists(MU_PDF_PATH):
    subprocess.run(["python3", "/workspace/create_marginal_utility_pdf.py"], check=True)
if not os.path.exists(PREF_PDF_PATH):
    subprocess.run(["python3", "/workspace/create_preferences_pdf.py"], check=True)
if not os.path.exists(IT_PDF_PATH):
    subprocess.run(["python3", "/workspace/create_intertemporal_pdf.py"], check=True)

add_pdf_pages_sheet(wb, PDF_PATH, sheet_name="Labor-Leisure PDF", header="Labor-Leisure Problems (screenshot pages)")
add_pdf_pages_sheet(wb, DIV_PDF_PATH, sheet_name="Diversification PDF", header="Diversification & Variance Problems (screenshot pages)")
add_pdf_pages_sheet(wb, MU_PDF_PATH, sheet_name="Marginal Utility PDF", header="Marginal Utility Guide (full PDF pages)")
add_pdf_pages_sheet(wb, PREF_PDF_PATH, sheet_name="Preferences PDF", header="Assumptions & Preferences Problems (screenshot pages)")
add_pdf_pages_sheet(wb, IT_PDF_PATH, sheet_name="Intertemporal PDF", header="Intertemporal Consumption Problems (screenshot pages)")
wb.save(OUT)
package_pdf_in_xlsx(OUT, PDF_PATH, internal_name="Labor_Leisure_Problems.pdf")
package_pdf_in_xlsx(OUT, DIV_PDF_PATH, internal_name="Diversification_Variance_Problems.pdf")
package_pdf_in_xlsx(OUT, MU_PDF_PATH, internal_name="Marginal_Utility_Guide.pdf")
package_pdf_in_xlsx(OUT, PREF_PDF_PATH, internal_name="Assumptions_Preferences_Problems.pdf")
package_pdf_in_xlsx(OUT, IT_PDF_PATH, internal_name="Intertemporal_Consumption_Problems.pdf")
print(f"Saved: {OUT} (with embedded study PDFs)")
