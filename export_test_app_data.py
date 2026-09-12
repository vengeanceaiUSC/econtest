#!/usr/bin/env python3
"""Export Practice Test 1 data for the interactive web app."""

import json
import os
import re
from create_exam_prep import QUESTIONS, PRACTICE_LABELS
from exam_config import EXAM_STRUCTURE, PRACTICE_TESTS

OUT = "/workspace/app/src/data/practice-test-1.json"

# MC options for questions where the bank text omits choices
MC_OPTIONS = {
    "Q008": [
        "(A) become steeper",
        "(B) become flatter",
        "(C) shift inward (parallel shift)",
        "(D) shift outward (parallel shift)",
        "(E) no change",
    ],
    "Q005": [
        "(A) u(X,Y) = X/7 + Y/5",
        "(B) u(X,Y) = 7X + 5Y",
        "(C) u(X,Y) = X^7 · Y^5",
        "(D) u(X,Y) = X/5 + Y/7",
        "(E) u(X,Y) = 5X + 7Y",
    ],
    "Q027": [
        "(A) q1=60",
        "(B) q1=70",
        "(C) q1=75",
        "(D) q1=80",
        "(E) q1=90",
    ],
    "Q031": [
        "(A) QA = 110 + 2PA − 4I − 2PB",
        "(B) QA = 110 − 2PA + 4I + 2PB",
        "(C) QA = 110 − 2PA − 4I + 2PB",
        "(D) QA = 110 + 2PA + 4I − 2PB",
        "(E) QA = 110 − 2PA − 4I − 2PB",
    ],
    "Q040": [
        "(A) risk neutral, risk loving",
        "(B) risk averse, risk neutral",
        "(C) risk loving, risk averse",
        "(D) risk averse, risk loving",
        "(E) both risk neutral",
    ],
    "Q042": [
        "(A) both risk averse",
        "(B) both risk loving",
        "(C) Marta risk averse; Hannah risk loving",
        "(D) Marta risk loving; Hannah risk averse",
        "(E) both risk neutral",
    ],
    "Q045": [
        "(A) both accept",
        "(B) both reject",
        "(C) Mohamed accepts; Sadio rejects",
        "(D) Mohamed rejects; Sadio accepts",
        "(E) cannot determine",
    ],
    "Q052": [
        "(A) 28.5",
        "(B) 30.7",
        "(C) 31.6",
        "(D) 32.0",
        "(E) 33.2",
    ],
    "Q053": [
        "(A) P_max ≈ $2,500; RP = $0",
        "(B) P_max ≈ $2,650; RP = $10",
        "(C) P_max ≈ $2,700; RP = $15",
        "(D) P_max ≈ $2,775; RP = $25",
        "(E) P_max ≈ $3,000; RP = $50",
    ],
    "Q002": [
        "No violation — indifference is allowed",
        "Yes — violates completeness",
        "Yes — violates transitivity",
        "Yes — violates monotonicity",
    ],
    "Q054": [
        "Feng (positively correlated portfolio)",
        "Nan (negatively correlated portfolio)",
        "Both equally risky",
        "Cannot determine",
    ],
}

SELF_GRADE_TYPES = {"Multi-step", "Calc", "Concept"}


def parse_mc_letter(answer: str):
    m = re.search(r"\(([A-E])\)", answer)
    return m.group(1) if m else None


def parse_options_from_text(text: str):
    opts = re.findall(r"\([A-E]\)[^;]+", text)
    return [o.strip().rstrip(".") for o in opts] if len(opts) >= 2 else None


def build_question(qnum: int, bank_id: str, section: dict):
    q = next(x for x in QUESTIONS if x[0] == bank_id)
    qtype = q[7]
    answer = q[8]
    mode = "self" if qtype in SELF_GRADE_TYPES else "mc"
    options = MC_OPTIONS.get(bank_id)
    if mode == "mc" and not options:
        options = parse_options_from_text(q[6])
    if mode == "mc" and not options:
        mode = "self"
    correct = parse_mc_letter(answer) if mode == "mc" else None
    correct_option = None
    if mode == "mc" and options:
        if bank_id == "Q002":
            correct_option = options[1]
        elif bank_id == "Q054":
            correct_option = options[0]
        elif correct:
            for opt in options:
                if opt.strip().startswith(f"({correct})"):
                    correct_option = opt
                    break
    return {
        "num": qnum,
        "bankId": bank_id,
        "label": PRACTICE_LABELS.get(bank_id, q[3]),
        "chapter": section["ch"],
        "category": section["category"],
        "source": f"{q[4]} · {q[5]}",
        "question": q[6],
        "mode": mode,
        "options": options or [],
        "correct": correct,
        "correctOption": correct_option,
        "answerKey": answer,
        "notes": q[9] or "",
        "type": qtype,
    }


def main():
    test = PRACTICE_TESTS[0]
    questions = []
    qnum = 0
    id_idx = 0
    for section in EXAM_STRUCTURE:
        for _ in range(section["count"]):
            qnum += 1
            bank_id = test["ids"][id_idx]
            id_idx += 1
            questions.append(build_question(qnum, bank_id, section))

    payload = {
        "title": test["title"],
        "totalQuestions": 24,
        "structure": EXAM_STRUCTURE,
        "questions": questions,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(payload, f, indent=2)
    mc = sum(1 for q in questions if q["mode"] == "mc")
    print(f"Exported {len(questions)} questions ({mc} MC, {len(questions)-mc} self-grade) -> {OUT}")


if __name__ == "__main__":
    main()
