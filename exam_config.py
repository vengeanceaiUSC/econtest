"""Shared exam structure and practice-test definitions."""

# Teacher's midterm format — counts per category (must sum to 24)
EXAM_STRUCTURE = [
    # Chapter 4 — 12 questions
    {"ch": 4, "category": "Consumer Problems", "count": 2},
    {"ch": 4, "category": "Labor-Leisure", "count": 2},
    {"ch": 4, "category": "Intertemporal Consumption", "count": 2},
    {"ch": 4, "category": "Elasticity / Types of Goods", "count": 3},
    {"ch": 4, "category": "Budget Line", "count": 1},
    {"ch": 4, "category": "Assumptions / Preferences", "count": 2},
    # Chapter 9 — 12 questions
    {"ch": 9, "category": "Insurance Problems", "count": 5},
    {"ch": 9, "category": "Risk Attitudes", "count": 4},
    {"ch": 9, "category": "Certainty Equivalent & Risk Premium", "count": 2},
    {"ch": 9, "category": "Diversification", "count": 1},
]

# Each practice test = 24 bank IDs in exact exam order (Ch.4 block then Ch.9 block)
PRACTICE_TESTS = [
    {
        "num": 1,
        "name": "Practice_Test_1",
        "title": "Practice Test 1",
        "ids": [
            # Ch. 4 (12)
            "Q014", "Q015",           # consumer (2)
            "Q021", "Q022",           # labor-leisure (2)
            "Q025", "Q027",           # intertemporal (2)
            "Q028", "Q032", "Q031",   # elasticity (3)
            "Q008",                   # budget line (1)
            "Q002", "Q005",           # preferences (2)
            # Ch. 9 (12)
            "Q047", "Q048", "Q050", "Q052", "Q053",  # insurance (5)
            "Q039", "Q040", "Q042", "Q045",           # risk attitudes (4)
            "Q035", "Q036",           # CE & RP (2)
            "Q054",                   # diversification (1)
        ],
    },
    {
        "num": 2,
        "name": "Practice_Test_2",
        "title": "Practice Test 2",
        "ids": [
            "Q016", "Q018",
            "Q021", "Q022",
            "Q023", "Q026",
            "Q029", "Q033", "Q030",
            "Q009",
            "Q001", "Q007",
            "Q049", "Q051", "Q047", "Q052", "Q053",
            "Q041", "Q043", "Q044", "Q046",
            "Q037", "Q038",
            "Q055",
        ],
    },
    {
        "num": 3,
        "name": "Practice_Test_3",
        "title": "Practice Test 3",
        "ids": [
            "Q017", "Q019",
            "Q021", "Q022",
            "Q024", "Q027",
            "Q028", "Q034", "Q032",
            "Q010",
            "Q003", "Q004",
            "Q048", "Q050", "Q049", "Q051", "Q053",
            "Q039", "Q041", "Q042", "Q046",
            "Q035", "Q037",
            "Q054",
        ],
    },
]


def validate_exam_structure():
    ch4 = sum(s["count"] for s in EXAM_STRUCTURE if s["ch"] == 4)
    ch9 = sum(s["count"] for s in EXAM_STRUCTURE if s["ch"] == 9)
    total = ch4 + ch9
    assert ch4 == 12 and ch9 == 12 and total == 24
    return total


def validate_practice_test(test):
    assert len(test["ids"]) == 24
    idx = 0
    for section in EXAM_STRUCTURE:
        n = section["count"]
        idx += n
    assert idx == 24
