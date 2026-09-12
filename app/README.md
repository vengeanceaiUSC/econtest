# ECON 351 — Interactive Practice Test 1

Clickable 24-question practice test that matches the midterm format and logs your mistakes.

## Run locally

```bash
cd app
npm install
npm run dev
```

Open http://localhost:5173

## Features

- **24 questions** in exam order (Ch. 4 → Ch. 9)
- **Multiple choice** — click an answer, instant feedback
- **Calculation / multi-step** — work on paper, then self-grade
- **Mistake log** — wrong answers saved automatically (persists in browser)
- **Question navigator** — jump to any question; green = right, red = wrong

## Regenerate question data

```bash
python3 export_test_app_data.py
```
