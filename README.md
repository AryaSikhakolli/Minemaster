# Explainable AI Minesweeper

A local web application implementing Minesweeper with an explainable AI solver.

## Features
- Easy / Medium / Hard / Expert presets
- Custom mine count
- Stopwatch
- Three hints per game
- Manual flagging
- Incorrect-flag cleaning
- Progressive AI solving
- Human-readable explanations
- Efficiency score
- Constraint reasoning, subset inference, backtracking enumeration and probability ranking

## Run

Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## AI concepts

1. Constraint Satisfaction Problem (CSP)
2. Knowledge representation
3. Logical inference / constraint propagation
4. Subset reasoning
5. State-space search
6. Backtracking / exhaustive frontier enumeration
7. Probability estimation
8. Heuristic best-move selection
9. Explainable AI (XAI)

## Important implementation note

The solver reasons only from information available in the current board state. It does not read hidden mine locations when making decisions. The game engine stores mines because it must evaluate the game, but the solver uses revealed numbers, flags and unopened cells as its knowledge base.
