# Spec Kit vs BMAD — AI-Assisted Development Comparison

> **Goal:** Demonstrate a structured AI-assisted development process using both **Spec Kit** and **BMAD Method**, building the same feature from a shared specification to compare workflows, outputs, and developer experience.

## What Is This?

This repo implements the **same feature twice** — an AI Highlight Selector — using two distinct AI-assisted development methodologies:

| | **Track 1 — Spec Kit** | **Track 2 — BMAD Method** |
|---|---|---|
| **Approach** | Specification-driven with structured tasks | Multi-agent branching workflow |
| **Planning** | spec → plan → tasks (82 tasks) | PRD → architecture → epics → stories (50 stories) |
| **Agents** | Single-agent with prompt templates | Multi-persona agents (PM, Architect, Dev, SM, etc.) |
| **Tests** | 99 tests, 88% coverage | 106 tests, 85% coverage |
| **Result** | ✅ Complete | ✅ Complete |

Both tracks consume the **same shared inputs** (`feature_overview.md` + `sample_data.json`) and produce a working CLI that selects, scores, and explains NBA game highlights.

## The Feature

| Input | Output |
|---|---|
| Game events (JSON) | Ranked & filtered highlights (5–8) |
| User preference (player / team) | Human-readable explanation per highlight |

**Scoring algorithm:** base score by importance (`critical` 100, `high` 75, `medium` 50, `low` 25) + player boost (+30) + team boost (+15) + context tags (`clutch` +20, `game_winner` +25, `buzzer_beater` +15, …).

**Constraints:** deterministic, explainable, zero runtime dependencies, Python 3.9+.

## Repository Structure

```
speckit-bmad/
├── shared/                          # Shared inputs for both tracks
│   ├── feature_overview.md          # Feature description & scope
│   └── sample_data.json             # 15 NBA Finals game events
│
├── track1-speckit/                  # Spec Kit implementation
│   ├── run.py                       # CLI entry point
│   ├── highlight_selector/          # Core Python package
│   │   ├── models.py                #   GameEvent, UserPreference, ScoreBreakdown, Highlight
│   │   ├── selector.py              #   Scoring, ranking, selection, explanations
│   │   └── cli.py                   #   JSON stdin → stdout interface
│   ├── tests/                       # 99 tests, 88% coverage
│   └── specs/001-highlight-selector/# Spec, plan, tasks, contracts
│       ├── spec.md
│       ├── plan.md
│       └── tasks.md                 # 82/82 tasks completed
│
├── track2-bmad/                     # BMAD implementation
│   ├── demo.py                      # Interactive demo script
│   ├── highlight_selector/          # Core Python package
│   │   ├── models.py                #   GameEvent, UserPreference, ScoreBreakdown, Highlight
│   │   ├── selector.py              #   Scoring, ranking, selection, explanations
│   │   └── cli.py                   #   CLI with argparse interface
│   ├── tests/                       # 106 tests, 85% coverage
│   └── _bmad-output/               # BMAD planning & implementation artifacts
│       ├── analysis/                #   Brainstorming sessions
│       ├── planning-artifacts/      #   PRD, architecture, epics
│       └── implementation-artifacts/#   50 story files + sprint status
│
└── .github/
    ├── agents/                      # Spec Kit agent definitions
    └── prompts/                     # Spec Kit prompt templates
```

## Quick Start

### Track 1 — Spec Kit

```bash
cd track1-speckit
python3 -m venv .venv && source .venv/bin/activate
pip install pytest pytest-cov black mypy

python run.py --player "LeBron James"
python run.py --team "Celtics" --only
python run.py   # no preference — top highlights by score
```

See [track1-speckit/README.md](track1-speckit/README.md) for full details.

### Track 2 — BMAD

```bash
cd track2-bmad
python3 -m venv venv && source venv/bin/activate
pip install pytest pytest-cov black mypy

python3 -m highlight_selector.cli ../shared/sample_data.json --player "LeBron James"
python3 -m highlight_selector.cli ../shared/sample_data.json --team "Lakers" --only
python3 demo.py   # interactive demo with multiple scenarios
```

See [track2-bmad/README.md](track2-bmad/README.md) for full details.

## Key Takeaways

Both methodologies successfully delivered a complete, tested, production-ready feature from the same starting point. The comparison highlights how different AI-assisted workflows approach planning, decomposition, implementation, and quality assurance — providing insight into which approach may suit different team sizes, project complexities, and developer preferences.

## Dev Dependencies

- **Runtime**: None (Python standard library only)
- **Development**: pytest, pytest-cov, black, mypy