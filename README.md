# AI Decoded — Interactive AI Quiz Game

**Course:** DSC401-6 — Artificial Intelligence  
**Coverage:** Units I and II

## Overview
AI Decoded is an interactive quiz game built with Python and Streamlit. Its question bank contains 50 questions covering foundational AI concepts, intelligent and rational agents, environments, problem formulation, state-space search, search algorithms, heuristic search, constraint satisfaction problems, and Means–End Analysis.

## Question bank
- 50 questions in `questions.json`
- Unit I: 24 questions
- Unit II: 26 questions
- Formats represented: MCQ, True/False, Assertion–Reason, Fill in the Blanks, Match the Following, Scenario, and Problem-solving
- Every question includes options, a correct answer, and an explanation

## Features
The application should be tested against the final `app.py` before submission. Features intended for the project include randomized questions/options, difficulty selection, a timer, hints, immediate feedback, progress indication, score calculation, answer review, and a leaderboard.

## Requirements
Install dependencies:
```bash
python -m pip install -r requirements.txt
```

## Run
Place `app.py`, `questions.json`, `leaderboard.json` (if used by the application), and `requirements.txt` in the same project folder. Then run:
```bash
python -m streamlit run app.py
```

## Submission checklist
- [ ] Confirm the final `app.py` runs with this `questions.json`.
- [ ] Capture screenshots from the actual running app.
- [ ] Check all 50 questions and answers.
- [ ] Confirm the question selection and scoring behaviour.
- [ ] Add the real screenshots to the project report.
