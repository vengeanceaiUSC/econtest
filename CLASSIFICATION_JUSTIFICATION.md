# ECON 351 Exam Prep — Classification Justification

This document explains how every question in **Exam Prep.xlsx** was categorized and how the **24-question practice set** was assembled from the uploaded materials.

## Sources parsed

| File | Chapter | Questions extracted |
|------|---------|---------------------|
| `Homework_1__Chapter_4__9bce.pdf` | 4 | Exercises 1–5 (preferences, consumer optimum, elasticity, intertemporal) |
| `Homework_2__Chapter_9__b189.pdf` | 9 | Exercises 1–3 (CE/RP, fair bets, insurance) |
| `SampleQuestionsChapter04ConsumerTheory_a895.pdf` | 4 | Q1–Q42 (MC + multi-step) |
| `SampleQuestionsChapter09Uncertainty_4bdd.pdf` | 9 | Q1–Q24 (investments, risk, insurance, diversification) |
| `Mock_Midterm_1_129f.pdf` | 4 & 9 | Mixed exam items |

**Total question bank:** 55 tagged items in the `Question Bank` sheet.

---

## Classification rules

Each problem was tagged by **what skill it tests**, not merely which PDF it came from.

### Chapter 4

| Category | Identification criteria | Example signals in problem text |
|----------|------------------------|-----------------------------------|
| **Consumer Problems** | Solve interior or corner optimum: MRS = price ratio, substitute into budget, find q₁*, q₂* | Cobb-Douglas utility, "optimal bundle", "maximize utility" |
| **Labor-Leisure** | Trade-off between leisure ℓ and consumption c with wage w, time constraint T = L + ℓ, budget c = wL + V | "hours", "wage", "leisure", "work" |
| **Intertemporal Consumption** | Two periods, interest rate r, discounting future income/consumption | c₁, c₂, "borrow/save", PV, "interest rate" |
| **Elasticity / Types of Goods** | Compute Ep, EI, Exy **or** infer normal/inferior, substitutes/complements | "elasticity", demand function signs, "shifts left/right" |
| **Budget Line** | How BL shifts/rotates when prices or income change (slope, intercepts) | "budget line will", "parallel shift", "become flatter/steeper" |
| **Assumptions / Preferences** | Completeness, transitivity, IC shape, perfect substitutes/complements, MRS from IC | "violate assumption", indifference curve type, "cannot decide" |

### Chapter 9

| Category | Identification criteria | Example signals in problem text |
|----------|------------------------|-----------------------------------|
| **Insurance** | Max premium, fair premium, partial/full insurance, E[u] with vs without insurance | "insure", "premium P", "copay", "expected loss" |
| **Risk Attitudes** | Classify risk averse/neutral/loving; accept/reject bets; utility/MU functional form or graphs | u(I)=I^a, MU(I) graph, "fair bet", "accept or reject" |
| **Certainty Equivalent & Risk Premium** | Explicitly compute CE (u(CE)=E[u]) and/or RP = E[x] − CE | "certainty equivalent", "risk premium" as primary task |
| **Diversification** | Correlation between assets, portfolio variance, who bears more risk | "positively/negatively correlated", "riskier portfolio" |

### Boundary decisions

| Situation | Rule applied |
|-----------|--------------|
| Tom HW Ex 3 has parts (a) max P, (b) fair P, (c) RP | Parts (a) and (b) → **Insurance**; part (c) could be either — RP from insurance context stays with insurance workflow |
| Jackie HW Ex 1 asks CE and RP | → **Certainty Equivalent & Risk Premium** (primary task is CE/RP, not premium) |
| Cuban minimum sell price P | If framed as "price to sell risky asset" → **CE & RP** (P = certainty equivalent); if framed as bet threshold → **Risk Attitudes** |
| Mock Q22–23 (investment E[u] and RP) | Split: E[u] setup is CE/RP family; used in practice set under CE & RP via HW/Sample equivalents |

---

## 24-question practice set mapping

Target: **12 Ch.4 + 12 Ch.9** per user specification.

### Chapter 4 (12 questions)

| Practice # | Bank ID | Category | Source | Classification rationale |
|------------|---------|----------|--------|------------------------|
| 1 | Q014 | Consumer Problems | HW1 Ex 3.1–3.5 | Full Cobb-Douglas optimum: MRS, budget, q₁*, q₂* |
| 2 | Q015 | Consumer Problems | Sample Q26 | Multi-step consumer problem with graph and slopes |
| 3 | Q021 | Labor-Leisure | Course-style *(not in uploads)* | No labor-leisure in uploads; written to fill 2-question slot |
| 4 | Q022 | Labor-Leisure | Course-style *(not in uploads)* | Wage comparative statics (w $20→$30) |
| 5 | Q025 | Intertemporal | Sample Q41 | Two-period optimum, r=0.5, save/borrow |
| 6 | Q027 | Intertemporal | Mock Q25 | Exam-style intertemporal optimum (follows Q24 setup) |
| 7 | Q028 | Elasticity | HW1 Ex 4.1–4.2 | Direct price elasticity calculation |
| 8 | Q032 | Elasticity | Sample Q39 | Price, income, and cross-price elasticities |
| 9 | Q031 | Elasticity | Sample Q38 | Infer complements + inferior from demand function |
| 10 | Q008 | Budget Line | Sample Q10 | Both prices double → parallel inward shift |
| 11 | Q002 | Assumptions / Preferences | HW1 Ex 2.2 | Cannot decide → completeness violation |
| 12 | Q005 | Assumptions / Preferences | Sample Q8 | Straight-line IC → perfect substitutes |

### Chapter 9 (12 questions)

| Practice # | Bank ID | Category | Source | Classification rationale |
|------------|---------|----------|--------|------------------------|
| 13 | Q047 | Insurance | HW2 Ex 3a | Maximum willingness to pay for full insurance |
| 14 | Q048 | Insurance | HW2 Ex 3b | Fair premium = E[loss] |
| 15 | Q050 | Insurance | Sample Q18 | Full insurance, different asset (Ferrari + cash) |
| 16 | Q052 | Insurance | Mock Q27 | Health insurance with premium + copay |
| 17 | Q053 | Insurance | Mock Q25–26 | Car insurance max P and RP |
| 18 | Q039 | Risk Attitudes | HW2 Ex 2 | MU graph + dice bet; fair bet accept/reject |
| 19 | Q040 | Risk Attitudes | Sample Q6 | Classify from U(I)=I vs U(I)=I^1.5 |
| 20 | Q042 | Risk Attitudes | Sample Q8 | Classify from u(I) graph concavity |
| 21 | Q045 | Risk Attitudes | Mock Q28 | Accept/reject bet from utility exponents |
| 22 | Q035 | CE & RP | HW2 Ex 1 | Full CE + RP workflow (Jackie investment) |
| 23 | Q036 | CE & RP | Sample Q12 | Same CE/RP structure, different numbers |
| 24 | Q054 | Diversification | Sample Q22 | Feng (pos. correlated) vs Nan (neg. correlated) |

---

## Gaps and adjustments

1. **Labor-leisure:** Zero problems in uploaded PDFs. Two course-style problems (Maria, w=$20→$30, U(c,ℓ)=c^0.5 ℓ^0.5) were authored to meet the 2-question target. Flagged on the `Study Plan` sheet.

2. **Tom insurance split:** HW2 Ex 3 is one multi-part problem. Parts (a) and (b) were placed as separate practice slots (#13, #14) to reach 5 insurance questions without repeating identical full problems.

3. **Questions in bank but not in practice set:** The `Question Bank` sheet holds 55 questions. Remaining items are available for extra drill by category (see `By Category` sheet).

---

## Regenerating the workbook

```bash
python3 create_exam_prep.py
```

Outputs `Exam Prep.xlsx` with sheets: Study Plan, Question Bank, Practice Set, Answer Key, Formula Sheet, By Category.
