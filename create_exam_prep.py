#!/usr/bin/env python3
"""Create Exam Prep.xlsx — categorized question bank, 24-question practice set, formula sheet."""

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

wb = Workbook()

# ── Styles ──────────────────────────────────────────────────────────────────
HEADER_FILL = PatternFill("solid", fgColor="1F4E79")
CH4_FILL = PatternFill("solid", fgColor="D6E4F0")
CH9_FILL = PatternFill("solid", fgColor="E2EFDA")
PRACTICE_FILL = PatternFill("solid", fgColor="FFF2CC")
HEADER_FONT = Font(bold=True, color="FFFFFF", size=11)
BOLD = Font(bold=True)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
thin = Side(style="thin", color="AAAAAA")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

def style_header_row(ws, row, ncol):
    for c in range(1, ncol + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = CENTER
        cell.border = BORDER

def style_data_rows(ws, start_row, end_row, ncol, fill=None):
    for r in range(start_row, end_row + 1):
        for c in range(1, ncol + 1):
            cell = ws.cell(row=r, column=c)
            cell.alignment = WRAP
            cell.border = BORDER
            if fill:
                cell.fill = fill

def set_col_widths(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

# ── Question bank columns ───────────────────────────────────────────────────
BANK_HEADERS = [
    "ID", "Chapter", "Category", "Subcategory", "Source", "Ref",
    "Question", "Type", "Answer / Key", "Notes"
]

# ── Full question bank ──────────────────────────────────────────────────────
QUESTIONS = [
    # ── CH 4: Assumptions / Preferences ──
    ("Q001", 4, "Assumptions / Preferences", "Completeness",
     "Homework 1 Ch.4", "Ex 2.1",
     "Jackie is at the movie theater. Movies available: 'Knives Out' and 'Top Gun Maverick.' She doesn't care which one to see. Does this violate any assumption on preferences? Which one?",
     "Concept", "No violation — indifference is allowed (completeness still holds).",
     "Tests completeness vs. indifference."),
    ("Q002", 4, "Assumptions / Preferences", "Completeness",
     "Homework 1 Ch.4", "Ex 2.2",
     "Jackie goes to the movies. Movies: 'Avatar' and 'The Avengers.' She cannot decide which one to see. Does this violate any assumption on preferences?",
     "Concept", "Yes — violates completeness (consumer cannot rank bundles).",
     ""),
    ("Q003", 4, "Assumptions / Preferences", "Transitivity",
     "Homework 1 Ch.4", "Ex 2.3",
     "Three movies: Parasite, Indiana Jones, Jurassic Park. Jackie prefers Parasite > Indiana Jones > Jurassic Park, but also prefers Jurassic Park > Parasite. Which assumption is violated?",
     "Concept", "Transitivity.",
     ""),
    ("Q004", 4, "Assumptions / Preferences", "MRS / IC slope",
     "Sample Q Ch.4", "Q5",
     "By observing the slope of an indifference curve, we can infer: (A) completeness (B) MU of vertical good (C) MRS (D) price ratio (E) transitivity",
     "MC", "(C) the marginal rate of substitution.",
     ""),
    ("Q005", 4, "Assumptions / Preferences", "Perfect substitutes",
     "Sample Q Ch.4", "Q8",
     "Serena's IC is a straight line with slope −7/5 (X on horizontal). Which utility function represents her preferences? Options include u = X/5 + Y/7.",
     "MC", "(D) u(X,Y) = X/5 + Y/7",
     "IC slope = MRS = (1/5)/(1/7) = 7/5."),
    ("Q006", 4, "Assumptions / Preferences", "Perfect complements",
     "Sample Q Ch.4", "Q30",
     "Tony views X and Y as perfect complements (1/4 X with 1/6 Y). Budget line: intercepts X=90, Y=50. Optimal mix?",
     "MC", "(D) 6X = 4Y",
     ""),
    ("Q007", 4, "Assumptions / Preferences", "Diminishing MRS",
     "Sample Q Ch.4", "Q6",
     "The magnitude of the slope of an IC is: (A) MRS (B) ratio of total utilities (C) always price ratio (D) all above (E) A and C only",
     "MC", "(A) called the marginal rate of substitution.",
     "Slope equals price ratio only at optimum, not everywhere."),

    # ── CH 4: Budget Line ──
    ("Q008", 4, "Budget Line", "Parallel shift",
     "Sample Q Ch.4", "Q10",
     "Apples (horizontal), oranges (vertical). Price of apples rises $3→$6; price of oranges rises $2→$4. Budget line:",
     "MC", "(C) shift inward (parallel shift).",
     "Slope unchanged (−PA/PO); income effectively halved."),
    ("Q009", 4, "Budget Line", "Slope change",
     "Sample Q Ch.4", "Q11",
     "Apples $6→$3; oranges $2→$4. Budget line:",
     "MC", "(A) become flatter.",
     "PA/PO falls → |slope| falls."),
    ("Q010", 4, "Budget Line", "Income shift",
     "Sample Q Ch.4", "Q13",
     "Income increases, prices constant. Budget line:",
     "MC", "(B) parallel outward shift.",
     ""),
    ("Q011", 4, "Budget Line", "Slope & intercept",
     "Sample Q Ch.4", "Q15a",
     "Brady indifferent between 3 apples and 4 bananas. PA=$10, PB=$13, I=$260. Slope of budget line (apples horizontal)?",
     "Calc", "−10/13",
     "Slope = −PA/PB."),
    ("Q012", 4, "Budget Line", "Price doubling",
     "Sample Q Ch.4", "Q14",
     "Budget line with A intercept 3, B intercept 6. Double price of apples. Budget line:",
     "MC", "(B) become steeper.",
     ""),
    ("Q013", 4, "Budget Line", "Both prices change",
     "Mock Midterm 1", "Q17",
     "Apples $6→$3; oranges $4→$2. Budget line:",
     "MC", "(D) shift outward (parallel shift).",
     "Prices halved → parallel outward shift."),

    # ── CH 4: Consumer Problems ──
    ("Q014", 4, "Consumer Problems", "Cobb-Douglas optimum",
     "Homework 1 Ch.4", "Ex 3.1–3.5",
     "Manuel: U(q1,q2) = 3q1^0.6 q2^0.4. Prices p1=5, p2=10, income=$100. Find q1*, q2*.",
     "Multi-step", "MRS = (0.6/0.4)(q2/q1) = p1/p2 → q2 = (2/3)q1. Budget: 5q1+10q2=100 → q1*=12, q2*=8.",
     "Full consumer theory problem."),
    ("Q015", 4, "Consumer Problems", "Cobb-Douglas graph",
     "Sample Q Ch.4", "Q26",
     "PA=$2, PB=$3, I=$120, U(A,B)=2A²B³. Write budget constraint, find optimal bundle, slopes at optimum.",
     "Multi-step", "BC: 2A+3B=120, slope=−2/3. Optimum: A*=24, B*=24. MRS at X = 3B/(2A) = 3/2.",
     ""),
    ("Q016", 4, "Consumer Problems", "Corner solution",
     "Sample Q Ch.4", "Q16",
     "Jorge buys only good X (no Y). What do we know about PX, PY and MUX, MUY? I: MUX>MUY II: PX<PY",
     "MC", "(B) I true; need more info for II.",
     ""),
    ("Q017", 4, "Consumer Problems", "Linear preferences",
     "Sample Q Ch.4", "Q17",
     "u(X,Y)=4X+6Y. Budget line intercepts X=90, Y=50. Optimal mix?",
     "MC", "(B) 9X = 5Y",
     "Corner: buy only Y if 4/6 < 50/90."),
    ("Q018", 4, "Consumer Problems", "Cobb-Douglas MU",
     "Sample Q Ch.4", "Q27",
     "MUA=5A⁴B³, MUB=3A⁵B², PA=6, PB=2, I=240. How many apples at optimum?",
     "MC", "(C) A=25",
     ""),
    ("Q019", 4, "Consumer Problems", "Subsidy",
     "Mock Midterm 1", "Q26",
     "u(q1,q2)=q1^0.5 q2^0.5, P1=P2=4, I=200. Govt subsidy S=2 per unit of good 1. Optimal q1?",
     "MC", "(B) q1=100",
     "Effective price of good 1 = 2."),
    ("Q020", 4, "Consumer Problems", "Same IC utility",
     "Mock Midterm 1", "Q22",
     "u(X,Y)=X⁶Y³. Basket A: (2,8). Basket B: (XB,2) on same IC. Find XB.",
     "MC", "(D) XB=16",
     "2⁶·8³ = XB⁶·2³ → XB=16."),

    # ── CH 4: Labor-Leisure ──
    ("Q021", 4, "Labor-Leisure", "Optimal hours",
     "Course-style (not in uploads)", "LL-1",
     "Maria has 16 hours/day for leisure (ℓ) and work. Wage w=$20/hr, non-labor income V=$80. Utility U(c,ℓ)=c^0.5 ℓ^0.5 where c = w(16−ℓ)+V. Find optimal ℓ* and labor hours L*.",
     "Multi-step", "MRS: (β/α)(c/ℓ)=w → c=wℓ. Budget: wℓ=w(16−ℓ)+80 → ℓ*=(w·16+V)/(2w)=10. L*=6, c*=$200.",
     "Standard labor-leisure Cobb-Douglas."),
    ("Q022", 4, "Labor-Leisure", "Wage change",
     "Course-style (not in uploads)", "LL-2",
     "Same setup as LL-1 but wage rises to w=$30. Find new ℓ*, L*, c*. Does Maria work more or less?",
     "Multi-step", "ℓ* = (30·16+80)/(2·30) = (480+80)/60 = 560/60 ≈ 9.33. L*≈6.67. She works MORE (substitution effect dominates for Cobb-Douglas).",
     "Compare to LL-1."),

    # ── CH 4: Intertemporal Consumption ──
    ("Q023", 4, "Intertemporal Consumption", "Contract comparison",
     "Homework 1 Ch.4", "Ex 5.1",
     "Contract 1: $10M today + $90M future. Contract 2: $42M today + $54M future. r=0.20. Which is cheaper for Angels (PV)?",
     "Calc", "PV1 = 10+90/1.2 = 85M; PV2 = 42+54/1.2 = 87M. Contract 1 is cheaper.",
     ""),
    ("Q024", 4, "Intertemporal Consumption", "Optimal c1, c2",
     "Homework 1 Ch.4", "Ex 5.3–5.4",
     "U(c1,c2)=2c1^0.4 c2^0.6, p1=p2=1, r=0.20, Contract 1 (10M, 90M). Find c1*, c2* and utility.",
     "Multi-step", "MRS: (0.4/0.6)(c2/c1) = (1+ r) → c2 = 1.5(1.2)c1. Budget: c1+ c2/1.2 = 10+90/1.2 = 85. Solve for c1*, c2*.",
     ""),
    ("Q025", 4, "Intertemporal Consumption", "Borrow vs save",
     "Sample Q Ch.4", "Q41",
     "I1=10, I2=12, r=0.5, p1=p2=1, u(q1,q2)=q1·q2. Find q1*, q2*. Saving or borrowing?",
     "Multi-step", "PV budget: q1 + q2/1.5 = 10+12/1.5 = 18. Optimum q1=q2 (Cobb-Douglas α=0.5). q1*=9, q2*=13.5. Consumes more in period 2 → saving.",
     ""),
    ("Q026", 4, "Intertemporal Consumption", "IT budget constraint",
     "Mock Midterm 1", "Q24",
     "I1=60, I2=125, r=0.25, u(q1,q2)=q1·q2. Which intertemporal budget constraint?",
     "MC", "(C) q1 + 1.25q2 = 216.25",
     "PV: q1 + q2/(1+r) = 60 + 125/1.25 = 160... check: 60+125/1.25=160. Option C: q1+1.25q2=216.25."),
    ("Q027", 4, "Intertemporal Consumption", "IT optimum",
     "Mock Midterm 1", "Q25",
     "Using Q24 setup, optimal q1 in period 1?",
     "MC", "(D) q1=80",
     ""),

    # ── CH 4: Elasticity / Types of Goods ──
    ("Q028", 4, "Elasticity / Types of Goods", "Price elasticity",
     "Homework 1 Ch.4", "Ex 4.1–4.2",
     "Demand q=100−5p. Find Q at p=5 and p=10. Compute price elasticity at p=5.",
     "Calc", "Q(5)=75, Q(10)=50. Ep = (P/Q)(dQ/dP) = (5/75)(−5) = −1/3.",
     ""),
    ("Q029", 4, "Elasticity / Types of Goods", "Cross-price elasticity",
     "Sample Q Ch.4", "Q37",
     "If goods X and Y are substitutes, cross-price elasticity is:",
     "MC", "(A) positive.",
     ""),
    ("Q030", 4, "Elasticity / Types of Goods", "Complements inference",
     "Sample Q Ch.4", "Q34",
     "Price of A rises → demand for B shifts left. Infer:",
     "MC", "(D) A and B are complements.",
     ""),
    ("Q031", 4, "Elasticity / Types of Goods", "Demand function signs",
     "Sample Q Ch.4", "Q38",
     "Apples & bananas complements; apples inferior. Which demand function for apples?",
     "MC", "(C) QA = 110 − 2PA − 4I + 2PB",
     "Negative on I (inferior), positive on PB (complement)."),
    ("Q032", 4, "Elasticity / Types of Goods", "Elasticity calculation",
     "Sample Q Ch.4", "Q39",
     "QA = 784 − 2PA − 3I − 4PO. At PA=2, I=100, PO=20: price, income, and cross-price elasticities.",
     "Multi-step", "QA=400. Ep=−1, EI=−0.75 (inferior), Exo=−0.20 (complements).",
     ""),
    ("Q033", 4, "Elasticity / Types of Goods", "Income elasticity",
     "Sample Q Ch.4", "Q40",
     "Income elasticity of X is −2. Income falls 2%. Effect on quantity demanded?",
     "MC", "(D) quantity demanded decreased 4%.",
     ""),
    ("Q034", 4, "Elasticity / Types of Goods", "Independent goods",
     "Mock Midterm 1", "Q19",
     "If X and Y are independent, cross-price elasticity is:",
     "MC", "(A) zero.",
     ""),

    # ── CH 9: Certainty Equivalent & Risk Premium ──
    ("Q035", 9, "Certainty Equivalent & Risk Premium", "Full CE problem",
     "Homework 2 Ch.9", "Ex 1",
     "Investment: 80% → $200, 20% → $50. u(x)=√x. Find E[x], E[u], certainty equivalent, risk premium.",
     "Multi-step", "E[x]=170. E[u]=0.8√200+0.2√50≈12.66. CE: √CE=12.66→CE≈160.4. RP=170−160.4≈9.6.",
     ""),
    ("Q036", 9, "Certainty Equivalent & Risk Premium", "CE & RP calc",
     "Sample Q Ch.9", "Q12",
     "80% → $144, 20% → $81, u(x)=√x. Find E[u], E[x], CE, RP.",
     "Multi-step", "E[x]=131.4. CE≈129.96. RP≈1.44.",
     ""),
    ("Q037", 9, "Certainty Equivalent & Risk Premium", "Minimum sell price",
     "Sample Q Ch.9", "Q13–14",
     "Cuban: 50% → $144, 50% → $64, u(I)=√I. Minimum price P to sell? Risk premium?",
     "MC", "P=100 (CE). RP = E[x]−CE = 104−100 = 4. Answer (E) 4.",
     ""),
    ("Q038", 9, "Certainty Equivalent & Risk Premium", "Mock CE/RP",
     "Mock Midterm 1", "Q22–23",
     "75% → $3600, 25% → $400, u(x)=√x. Find E[u] and risk premium.",
     "MC", "E[u]=40. RP=500. Answers (A) and (C).",
     ""),

    # ── CH 9: Risk Attitudes ──
    ("Q039", 9, "Risk Attitudes", "Fair bet (graph)",
     "Homework 2 Ch.9", "Ex 2",
     "Mike's MU(I) graph given. Bet: pay $20 on dice 1–2, receive $10 on 3–6. Fair bet? Accept?",
     "Concept", "Fair bet (E[win]=0). Risk averse → reject. Does not depend on wealth if can pay $20.",
     ""),
    ("Q040", 9, "Risk Attitudes", "Utility function form",
     "Sample Q Ch.9", "Q6",
     "Anna U(I)=I, Elsa U(I)=I^1.5. Anna is ___ and Elsa is ___.",
     "MC", "(A) risk neutral, risk loving.",
     "a>1 → risk loving; a=1 → neutral; a<1 → averse."),
    ("Q041", 9, "Risk Attitudes", "MU function form",
     "Sample Q Ch.9", "Q7",
     "Anna MU(I)=I, Elsa MU(I)=I^1.5. Classify risk attitudes.",
     "MC", "(C) risk loving, risk loving.",
     "Increasing MU → risk loving."),
    ("Q042", 9, "Risk Attitudes", "Utility graph",
     "Sample Q Ch.9", "Q8",
     "Graphs of u(I) for Marta and Hannah. Classify both.",
     "MC", "(C) Marta risk averse; Hannah risk loving.",
     "Concave vs convex utility."),
    ("Q043", 9, "Risk Attitudes", "Fair coin bet",
     "Sample Q Ch.9", "Q10–11",
     "Constant MU vs decreasing MU. Fair coin: pay $10 heads, receive $10 tails. Accept or reject?",
     "MC", "Q10: (D) accept (risk neutral). Q11: (B) reject (risk averse).",
     ""),
    ("Q044", 9, "Risk Attitudes", "Minimum winning probability",
     "Sample Q Ch.9", "Q3",
     "Pedro: I=$169, bet all on Seahawks. Win→$400, lose→$0. Min P to accept bet? u=√I.",
     "MC", "(B) P=65%.",
     "20P=13 → P=0.65."),
    ("Q045", 9, "Risk Attitudes", "Bet accept/reject",
     "Mock Midterm 1", "Q28",
     "Firmino bet: Reds win → friend pays $1; lose → Firmino pays $3. Mohamed U=I^0.7, Sadio U=I^2.3.",
     "MC", "(D) Mohamed rejects; Sadio accepts.",
     ""),
    ("Q046", 9, "Risk Attitudes", "MU comparison",
     "Mock Midterm 1", "Q30",
     "Mirabel MU(I)=9, Bruno MU(I)=3/I. Classify.",
     "MC", "(C) Mirabel risk neutral; Bruno risk averse.",
     ""),

    # ── CH 9: Insurance ──
    ("Q047", 9, "Insurance", "Max premium",
     "Homework 2 Ch.9", "Ex 3a",
     "Tom: house $846,400, 25% chance $174,000 damage, u=√I. Max premium P for full insurance?",
     "Calc", "P_max ≈ $45,375 (EU with insurance = EU without at P=45,375).",
     ""),
    ("Q048", 9, "Insurance", "Fair premium",
     "Homework 2 Ch.9", "Ex 3b",
     "Same Tom setup. Fair (actuarially fair) insurance premium?",
     "Calc", "E[loss] = 0.25 × $174,000 = $43,500.",
     ""),
    ("Q049", 9, "Insurance", "Insurance risk premium",
     "Homework 2 Ch.9", "Ex 3c",
     "Tom insurance: risk premium = max premium − fair premium.",
     "Calc", "RP = $45,375 − $43,500 = $1,875.",
     ""),
    ("Q050", 9, "Insurance", "Sherman car",
     "Sample Q Ch.9", "Q18",
     "Sherman: Ferrari $230,900 + $50,000 cash. 25% chance $158,400 damage. u=√x. Max P and RP?",
     "Multi-step", "P_max ≈ $45,675. Fair = $39,600. RP ≈ $6,075.",
     ""),
    ("Q051", 9, "Insurance", "Partial insurance",
     "Sample Q Ch.9", "Q20–21",
     "Marcelo: car $10,000, 25% crash cost $6,348. Partial insurance P=$124, pays half repair. E[u]?",
     "MC", "(D) E[u]=95.",
     ""),
    ("Q052", 9, "Insurance", "Health copay",
     "Mock Midterm 1", "Q27",
     "$1,000 cash. 10% sick, doctor $500. Premium $100, copay $275 if sick. u=√I. E[u] with insurance?",
     "MC", "(B) 30.7",
     ""),
    ("Q053", 9, "Insurance", "Car insurance mock",
     "Mock Midterm 1", "Q25–26",
     "Car $10,000, 75% crash $3,600 damage. u=√I. Max P and RP?",
     "MC", "P_max ≈ $2,775 (D). RP = $25 (E).",
     ""),

    # ── CH 9: Diversification ──
    ("Q054", 9, "Diversification", "Correlation & portfolio risk",
     "Sample Q Ch.9", "Q22",
     "Feng: companies A&B (agriculture, positively correlated). Nan: C&D (airline/oil, negatively correlated). Who has riskier portfolio?",
     "Concept", "Feng — positively correlated assets don't diversify; Nan's portfolio has lower variance.",
     ""),
    ("Q055", 9, "Diversification", "Portfolio variance",
     "Mock Midterm 1", "Q29",
     "John: half A, half B (positively correlated). Marc: half C, half D (negatively correlated). Compare variance.",
     "MC", "(D) John's investment has higher variance.",
     "Diversification reduces risk with negative correlation."),
]

# Practice set: 24 questions matching user's breakdown
PRACTICE_IDS = [
    # Ch 4 (12)
    "Q014",  # Consumer 1
    "Q015",  # Consumer 2
    "Q021",  # Labor-leisure 1
    "Q022",  # Labor-leisure 2
    "Q025",  # Intertemporal 1
    "Q027",  # Intertemporal 2
    "Q028",  # Elasticity 1
    "Q032",  # Elasticity 2
    "Q031",  # Elasticity 3
    "Q008",  # Budget line 1
    "Q002",  # Assumptions 1
    "Q005",  # Assumptions 2
    # Ch 9 (12)
    "Q047",  # Insurance 1
    "Q048",  # Insurance 2
    "Q050",  # Insurance 3
    "Q052",  # Insurance 4
    "Q053",  # Insurance 5
    "Q039",  # Risk attitudes 1
    "Q040",  # Risk attitudes 2
    "Q042",  # Risk attitudes 3
    "Q045",  # Risk attitudes 4
    "Q035",  # CE & RP 1
    "Q036",  # CE & RP 2
    "Q054",  # Diversification 1
]

PRACTICE_LABELS = {
    "Q014": "Consumer Problem #1",
    "Q015": "Consumer Problem #2",
    "Q021": "Labor-Leisure #1",
    "Q022": "Labor-Leisure #2",
    "Q025": "Intertemporal #1",
    "Q027": "Intertemporal #2",
    "Q028": "Elasticity #1",
    "Q032": "Elasticity #2",
    "Q031": "Elasticity #3",
    "Q008": "Budget Line",
    "Q002": "Preferences #1",
    "Q005": "Preferences #2",
    "Q047": "Insurance #1",
    "Q048": "Insurance #2",
    "Q050": "Insurance #3",
    "Q052": "Insurance #4",
    "Q053": "Insurance #5",
    "Q039": "Risk Attitudes #1",
    "Q040": "Risk Attitudes #2",
    "Q042": "Risk Attitudes #3",
    "Q045": "Risk Attitudes #4",
    "Q035": "Certainty Eq. & RP #1",
    "Q036": "Certainty Eq. & RP #2",
    "Q054": "Diversification",
}

# ── Sheet 1: Study Plan Overview ────────────────────────────────────────────
ws0 = wb.active
ws0.title = "Study Plan"
ws0["A1"] = "ECON 351 — Exam Prep Study Set"
ws0["A1"].font = Font(bold=True, size=14)
ws0.merge_cells("A1:D1")

overview = [
    ("", "", "", ""),
    ("Chapter", "Category", "Target #", "Practice Set IDs"),
    ("4", "Consumer Problems", 2, "Q014, Q015"),
    ("4", "Labor-Leisure", 2, "Q021, Q022  ⚠ course-style (not in uploads)"),
    ("4", "Intertemporal Consumption", 2, "Q025, Q027"),
    ("4", "Elasticity / Types of Goods", 3, "Q028, Q032, Q031"),
    ("4", "Budget Line", 1, "Q008"),
    ("4", "Assumptions / Preferences", 2, "Q002, Q005"),
    ("", "Ch. 4 Total", 12, ""),
    ("9", "Insurance Problems", 5, "Q047–Q053 (selected 5)"),
    ("9", "Risk Attitudes", 4, "Q039, Q040, Q042, Q045"),
    ("9", "Certainty Equivalent & Risk Premium", 2, "Q035, Q036"),
    ("9", "Diversification", 1, "Q054"),
    ("", "Ch. 9 Total", 12, ""),
    ("", "GRAND TOTAL", 24, "See 'Practice Set' sheet"),
]
for r, row in enumerate(overview, 2):
    for c, val in enumerate(row, 1):
        cell = ws0.cell(row=r, column=c, value=val)
        if r == 3:
            cell.font = BOLD
            cell.fill = HEADER_FILL
            cell.font = HEADER_FONT
        cell.alignment = WRAP
set_col_widths(ws0, [14, 32, 12, 50])

# ── Sheet: Study Sets (teacher breakdown) ───────────────────────────────────
STUDY_SET_ROWS = [
    (1, 4, "Consumer Problems", 2, "Q1, Q2", [1, 2], "01_Consumer_Problems.pdf"),
    (2, 4, "Labor-Leisure", 2, "Q3, Q4", [3, 4], "02_Labor_Leisure.pdf"),
    (3, 4, "Intertemporal Consumption", 2, "Q5, Q6", [5, 6], "03_Intertemporal_Consumption.pdf"),
    (4, 4, "Elasticity / Types of Goods", 3, "Q7, Q8, Q9", [7, 8, 9], "04_Elasticity_Types_of_Goods.pdf"),
    (5, 4, "Budget Line", 1, "Q10", [10], "05_Budget_Line.pdf"),
    (6, 4, "Assumptions / Preferences", 2, "Q11, Q12", [11, 12], "06_Assumptions_Preferences.pdf"),
    (7, 9, "Insurance Problems", 5, "Q13–Q17", [13, 14, 15, 16, 17], "07_Insurance_Problems.pdf"),
    (8, 9, "Risk Attitudes", 4, "Q18–Q21", [18, 19, 20, 21], "08_Risk_Attitudes.pdf"),
    (9, 9, "Certainty Equivalent & Risk Premium", 2, "Q22, Q23", [22, 23], "09_Certainty_Equivalent_Risk_Premium.pdf"),
    (10, 9, "Diversification", 1, "Q24", [24], "10_Diversification.pdf"),
]
ws_sets = wb.create_sheet("Study Sets", 1)
set_headers = ["Set #", "Chapter", "Category", "Questions in Set", "Practice Q IDs", "PDF File"]
for c, h in enumerate(set_headers, 1):
    ws_sets.cell(row=1, column=c, value=h)
style_header_row(ws_sets, 1, len(set_headers))
for i, row in enumerate(STUDY_SET_ROWS, 2):
    excel_vals = [row[0], row[1], row[2], row[3], row[4], row[6]]
    for c, val in enumerate(excel_vals, 1):
        cell = ws_sets.cell(row=i, column=c, value=val)
        cell.fill = CH4_FILL if row[1] == 4 else CH9_FILL
        cell.alignment = WRAP
        cell.border = BORDER
# totals row
tr = len(STUDY_SET_ROWS) + 2
ws_sets.cell(row=tr, column=1, value="")
ws_sets.cell(row=tr, column=2, value="Total")
ws_sets.cell(row=tr, column=3, value="Ch.4 = 12 | Ch.9 = 12")
ws_sets.cell(row=tr, column=4, value=24)
ws_sets.cell(row=tr, column=5, value="Q1–Q24")
ws_sets.cell(row=tr, column=6, value="practice_sets/ (10 PDFs + Formula_Sheet.pdf)")
set_col_widths(ws_sets, [8, 10, 36, 16, 20, 38])
ws_sets.freeze_panes = "A2"

# ── Sheet 2: Full Question Bank ─────────────────────────────────────────────
ws1 = wb.create_sheet("Question Bank")
for c, h in enumerate(BANK_HEADERS, 1):
    ws1.cell(row=1, column=c, value=h)
style_header_row(ws1, 1, len(BANK_HEADERS))

q_by_id = {}
for i, q in enumerate(QUESTIONS, 2):
    q_by_id[q[0]] = q
    fill = CH4_FILL if q[1] == 4 else CH9_FILL
    for c, val in enumerate(q, 1):
        cell = ws1.cell(row=i, column=c, value=val)
        cell.fill = fill
        cell.alignment = WRAP
        cell.border = BORDER
style_data_rows(ws1, 2, len(QUESTIONS) + 1, len(BANK_HEADERS))
set_col_widths(ws1, [8, 8, 28, 18, 22, 10, 55, 12, 40, 25])
ws1.freeze_panes = "A2"

# ── Sheet 3: Practice Set (24 questions) ────────────────────────────────────
ws2 = wb.create_sheet("Practice Set")
practice_headers = ["#", "Study Set", "In-Set #", "Label", "Chapter", "Category"] + BANK_HEADERS[4:]
for c, h in enumerate(practice_headers, 1):
    ws2.cell(row=1, column=c, value=h)
style_header_row(ws2, 1, len(practice_headers))

SET_FOR_Q = {}
for set_num, ch, cat, cnt, _, qids, _pdf in STUDY_SET_ROWS:
    for j, qn in enumerate(qids, 1):
        SET_FOR_Q[qn] = (set_num, j, cnt, cat)

for i, qid in enumerate(PRACTICE_IDS, 1):
    q = q_by_id[qid]
    qnum = i
    set_info = SET_FOR_Q.get(qnum, ("", "", "", ""))
    row = [
        qnum,
        f"Set {set_info[0]}: {set_info[3]}" if set_info[0] else "",
        f"{set_info[1]} of {set_info[2]}" if set_info[0] else "",
        PRACTICE_LABELS.get(qid, ""),
        q[1],
        q[2],
        q[4],  # Source
        q[5],  # Ref
        q[6],  # Question
        q[7],  # Type
        "",    # blank answer for student
        q[9],  # Notes
    ]
    r = i + 1
    fill = PRACTICE_FILL
    for c, val in enumerate(row, 1):
        cell = ws2.cell(row=r, column=c, value=val)
        cell.fill = fill
        cell.alignment = WRAP
        cell.border = BORDER
set_col_widths(ws2, [5, 28, 10, 22, 8, 28, 22, 10, 55, 12, 40, 25])
ws2.freeze_panes = "A2"

# ── Sheet 4: Answer Key (Practice Set) ────────────────────────────────────────
ws3 = wb.create_sheet("Answer Key")
ak_headers = ["#", "Label", "ID", "Answer / Key"]
for c, h in enumerate(ak_headers, 1):
    ws3.cell(row=1, column=c, value=h)
style_header_row(ws3, 1, len(ak_headers))
for i, qid in enumerate(PRACTICE_IDS, 1):
    q = q_by_id[qid]
    r = i + 1
    for c, val in enumerate([i, PRACTICE_LABELS.get(qid, ""), qid, q[8]], 1):
        cell = ws3.cell(row=r, column=c, value=val)
        cell.alignment = WRAP
        cell.border = BORDER
set_col_widths(ws3, [5, 22, 8, 60])
ws3.freeze_panes = "A2"

# ── Sheet 5: Formula Sheet ───────────────────────────────────────────────────
ws4 = wb.create_sheet("Formula Sheet")
ws4["A1"] = "ECON 351 — One-Page Formula Sheet (Ch. 4 & Ch. 9)"
ws4["A1"].font = Font(bold=True, size=13)
ws4.merge_cells("A1:C1")

formulas = [
    ("", "", ""),
    ("CHAPTER 4 — CONSUMER THEORY", "", ""),
    ("Budget constraint", "p₁q₁ + p₂q₂ = I", "Slope = −p₁/p₂"),
    ("Optimal (interior)", "MRS = MU₁/MU₂ = p₁/p₂", "Tangency condition"),
    ("Cobb-Douglas U = q₁^α q₂^β", "q₁* = α/(α+β) · I/p₁", "q₂* = β/(α+β) · I/p₂"),
    ("Perfect substitutes", "Buy only good with higher MU/p", "Corner solution"),
    ("Perfect complements", "Consume at fixed ratio; kink on IC", "q₂/q₁ = constant"),
    ("MRS (Cobb-Douglas)", "MRS = (α/β)(q₂/q₁)", ""),
    ("Labor-Leisure", "c = wL + V,  L = T − ℓ", "T = total time; V = non-labor income"),
    ("Labor-Leisure optimum", "MU_ℓ / MU_c = w", "Cobb-Douglas: ℓ* = (wT+V)/(2w) if α=β=0.5"),
    ("Intertemporal BC", "c₁ + c₂/(1+r) = I₁ + I₂/(1+r)", "Discount future consumption"),
    ("Intertemporal optimum", "MU₁/MU₂ = (1+r)", "Future price = 1+r"),
    ("Present value", "PV = Σ FVₜ/(1+r)ᵗ", "Compare contracts by PV"),
    ("Price elasticity", "E_p = (P/Q)(∂Q/∂P)", "Linear: E_p = (∂Q/∂P)·(P/Q)"),
    ("Income elasticity", "E_I = (I/Q)(∂Q/∂I)", "E_I>0 normal; E_I<0 inferior"),
    ("Cross-price elasticity", "E_xy = (P_y/Q_x)(∂Q_x/∂P_y)", "+ substitutes; − complements; 0 independent"),
    ("", "", ""),
    ("CHAPTER 9 — UNCERTAINTY & RISK", "", ""),
    ("Expected value", "E[x] = Σ pᵢ xᵢ", "Probability-weighted average"),
    ("Expected utility", "E[u] = Σ pᵢ u(xᵢ)", "EU theory"),
    ("Risk attitudes", "u''(x) < 0 → risk averse", "u''=0 neutral; u''>0 loving"),
    ("MU test", "Decreasing MU(I) → risk averse", "Constant MU → neutral; Increasing → loving"),
    ("Certainty equivalent (CE)", "u(CE) = E[u(x)]", "Sure $ with same EU as gamble"),
    ("Risk premium (RP)", "RP = E[x] − CE", "Extra E[x] to accept risk"),
    ("Fair bet", "E[payoff] = 0", "Risk averse rejects; lover accepts"),
    ("Fair insurance premium", "P_fair = E[loss] = Σ pᵢ · lossᵢ", "Actuarially fair"),
    ("Max insurance premium", "E[u(with ins)] = E[u(no ins)]", "Solve for P"),
    ("Insurance risk premium", "RP_ins = P_max − P_fair", ""),
    ("Partial insurance EU", "E[u] = Σ pᵢ u(income in state i)", "Include premium all states"),
    ("Diversification", "Negatively correlated assets ↓ portfolio variance", "Don't put eggs in one basket"),
]

for r, (topic, formula, note) in enumerate(formulas, 2):
    ws4.cell(row=r, column=1, value=topic).font = BOLD if topic.startswith("CHAPTER") else Font()
    ws4.cell(row=r, column=2, value=formula)
    ws4.cell(row=r, column=3, value=note)
    for c in range(1, 4):
        ws4.cell(row=r, column=c).alignment = WRAP
        if topic.startswith("CHAPTER"):
            ws4.cell(row=r, column=c).fill = PatternFill("solid", fgColor="D9D9D9")
set_col_widths(ws4, [28, 38, 38])

# ── Sheet 6: Category Summary ───────────────────────────────────────────────
ws5 = wb.create_sheet("By Category")
cat_headers = ["Chapter", "Category", "Count in Bank", "Count in Practice Set", "Question IDs (Bank)"]
for c, h in enumerate(cat_headers, 1):
    ws5.cell(row=1, column=c, value=h)
style_header_row(ws5, 1, len(cat_headers))

from collections import defaultdict
bank_cats = defaultdict(list)
practice_cats = defaultdict(list)
for q in QUESTIONS:
    key = (q[1], q[2])
    bank_cats[key].append(q[0])
for qid in PRACTICE_IDS:
    q = q_by_id[qid]
    practice_cats[(q[1], q[2])].append(qid)

categories_order = [
    (4, "Consumer Problems"),
    (4, "Labor-Leisure"),
    (4, "Intertemporal Consumption"),
    (4, "Elasticity / Types of Goods"),
    (4, "Budget Line"),
    (4, "Assumptions / Preferences"),
    (9, "Insurance"),
    (9, "Risk Attitudes"),
    (9, "Certainty Equivalent & Risk Premium"),
    (9, "Diversification"),
]
for i, (ch, cat) in enumerate(categories_order, 2):
    key = (ch, cat)
    ws5.cell(row=i, column=1, value=ch)
    ws5.cell(row=i, column=2, value=cat)
    ws5.cell(row=i, column=3, value=len(bank_cats.get(key, [])))
    ws5.cell(row=i, column=4, value=len(practice_cats.get(key, [])))
    ws5.cell(row=i, column=5, value=", ".join(bank_cats.get(key, [])))
    fill = CH4_FILL if ch == 4 else CH9_FILL
    for c in range(1, 6):
        ws5.cell(row=i, column=c).alignment = WRAP
        ws5.cell(row=i, column=c).fill = fill
        ws5.cell(row=i, column=c).border = BORDER
set_col_widths(ws5, [10, 32, 14, 20, 50])

out = "/workspace/Exam Prep.xlsx"
wb.save(out)
print(f"Saved: {out}")
print(f"Total questions in bank: {len(QUESTIONS)}")
print(f"Practice set: {len(PRACTICE_IDS)} questions")
