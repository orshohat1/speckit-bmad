# Implementation Plan: AI Highlight Selector

**Branch**: `001-highlight-selector` | **Date**: 2026-02-17 | **Spec**: [spec.md](spec.md)  
**Input**: Feature specification from `specs/001-highlight-selector/spec.md`

## Summary

The AI Highlight Selector is a Python library that processes game event lists and returns 5-8 curated highlights based on event importance and user preferences (favorite player/team). Each highlight includes a human-readable explanation. The system implements deterministic scoring with explicit tie-breaking rules, operates on structured data contracts (JSON), and maintains strict separation between data models, scoring logic, selection logic, and explanation generation.

**Technical Approach**:
- Single Python package with pure functions for testability
- Standard library only (except pytest for testing - documented exception below)
- Dataclasses for type-safe data modeling 
- Deterministic scoring algorithm with configurable boosts
- Template-based explanation generation

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: None (stdlib only per Constitution Article VII)  
**Storage**: N/A (stateless processing)  
**Testing**: pytest (documented exception - see Complexity Tracking)  
**Target Platform**: Cross-platform (Linux, macOS, Windows)  
**Project Type**: single (Python library with CLI interface)  
**Performance Goals**: <100ms for 15 events, <1s for 1000 events (SC-001, SC-005)  
**Constraints**: Deterministic output (Constitution Article V), stdlib-only runtime (Constitution Article VII), 100% test coverage for edge cases  
**Scale/Scope**: Single feature, 3 modules (models, core logic, CLI), ~300-400 LOC estimated

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Article I — Simplicity First ✅ PASS

- [x] Using ≤ 1 module? → **Yes.** Single Python package (`highlight_selector/`)
- [x] No future-proofing? → **Yes.** Only implementing specified features (5 user stories, 15 FRs)
- [x] All functions trace to user story? → **Yes.** See Traceability Matrix below

### Article II — Testability Mandate ✅ PASS

- [x] Pure functions for business logic? → **Yes.** All scoring and selection functions are stateless
- [x] Every scoring rule has test? → **Yes.** 18 acceptance scenarios map to test cases
- [x] Edge cases covered? → **Yes.** 7 edge cases identified in spec (US-5)

### Article III — Explainability Requirement ✅ PASS

- [x] Every output includes explanation? → **Yes.** `Highlight` dataclass includes `explanation` field
- [x] Explanations reference scoring factors? → **Yes.** Template system includes importance, player/team preference, clutch timing
- [x] Non-technical language? → **Yes.** SC-007 mandates 1-2 sentences with no jargon

### Article IV — Data-Driven Design ✅ PASS

- [x] Input/output schemas defined? → **Yes.** 4 dataclasses defined (see Data Model section)
- [x] All data through typed models? → **Yes.** Using `@dataclass` with type hints
- [x] JSON interchange format? → **Yes.** CLI accepts/returns JSON

### Article V — Deterministic Behavior ✅ PASS

- [x] Identical inputs → identical outputs? → **Yes.** FR-009, SC-004 mandate determinism
- [x] No randomness in algorithm? → **Yes.** Pure scoring formulas only
- [x] Explicit tie-breaking rules? → **Yes.** Three-level tie-breaking (quarter → importance → event_id)

### Article VI — Separation of Concerns ✅ PASS

- [x] Data models separated? → **Yes.** `models.py`
- [x] Scoring logic separated? → **Yes.** `score_event()` function in `selector.py`
- [x] Selection logic separated? → **Yes.** `rank_and_filter()` function in `selector.py`
- [x] Explanation generation separated? → **Yes.** `generate_explanation()` function in `selector.py`

### Article VII — Python Best Practices ⚠️ PARTIAL (see Complexity Tracking)

- [x] Type hints on all signatures? → **Yes.** All functions will use type hints
- [x] Docstrings on public functions? → **Yes.** Google-style docstrings
- [x] PEP 8 compliance? → **Yes.** Will use `black` formatter (stdlib-compatible)
- [⚠️] No external dependencies? → **EXCEPTION.** Using `pytest` for testing (see Complexity Tracking)

## Project Structure

### Documentation (this feature)

```text
specs/001-highlight-selector/
├── spec.md                      # ✅ Complete feature specification
├── plan.md                      # 📝 This file (implementation plan)
├── checklists/
│   └── requirements.md          # ✅ Specification validation checklist
└── [to be created by implementation]
    ├── data-model.md            # Detailed entity schemas
    ├── quickstart.md            # Usage examples and testing instructions
    └── contracts/
        └── input-output.json    # JSON schema examples
```

### Source Code (repository root)

```text
highlight_selector/              # Single package (Constitution Article I)
├── __init__.py                  # Package exports
├── models.py                    # Data model definitions (Article VI)
├── selector.py                  # Core logic: scoring, selection, explanation
└── cli.py                       # Command-line interface

tests/                           # Test organization (Article II)
├── __init__.py
├── test_models.py               # Data model validation tests
├── test_scoring.py              # Scoring algorithm tests (pure functions)
├── test_selection.py            # Selection and ranking tests
├── test_explanations.py         # Explanation generation tests
├── test_edge_cases.py           # US-5 edge case coverage
└── test_integration.py          # End-to-end integration tests

shared/                          # ✅ Already exists
├── sample_data.json             # 15 NBA Finals events for testing
└── feature_overview.md          # Project documentation

pyproject.toml                   # Python project metadata (minimal)
README.md                        # Setup and usage instructions
```

**Structure Decision**: Selected **Option 1: Single project** structure. The `highlight_selector/` package contains all core logic as separate modules to maintain separation of concerns (Constitution Article VI) while staying within the "maximum 1 module" constraint interpreted as "1 logical package" per user clarification. Tests are organized by concern (models, scoring, selection, explanations, edge cases, integration) to enable independent validation of each component.

## Complexity Tracking

> **Constitution Article VII Violation: External Dependency**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| **pytest** (testing framework) | • Industry-standard testing ergonomics (fixtures, parametrization, assertions)<br>• Better test discovery and reporting<br>• Supports 18 acceptance scenarios + edge cases efficiently<br>• Type-aware assertions align with Article VII type hint requirement | **unittest** (stdlib): Verbose boilerplate, limited parametrization support, less readable test code. Given 25+ test cases across 7 test modules, unittest would add ~40% more LOC with minimal benefit. pytest is **development-only** dependency (not runtime), so Constitution Article VII intent (minimize supply-chain risk) is preserved. |

**Approval Rationale**: User explicitly approved pytest with documented exception. Runtime dependencies remain stdlib-only, maintaining production security posture.

---

## Architecture Overview

### System Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                     CLI Entry Point (cli.py)                     │
│                                                                  │
│  • Reads JSON from stdin or file                                │
│  • Validates input schema                                        │
│  • Calls select_highlights()                                     │
│  • Writes JSON to stdout                                         │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                  Core Logic (selector.py)                        │
│                                                                  │
│  select_highlights(events, prefs, max_count=8, min_count=5)     │
│    │                                                             │
│    ├──▶ score_event(event, prefs) → ScoredEvent                 │
│    │     • Calculate base score from importance                 │
│    │     • Apply player preference boost (+30)                  │
│    │     • Apply team preference boost (+15)                    │
│    │     • Apply contextual boosts (clutch, quarter, etc.)      │
│    │                                                             │
│    ├──▶ rank_and_filter(scored_events, max, min) → [Scored]    │
│    │     • Force-include all critical events                    │
│    │     • Sort by score descending                             │
│    │     • Apply tie-breaking: quarter → importance → id        │
│    │     • Select top 5-8 events                                │
│    │                                                             │
│    └──▶ generate_explanation(event, score_breakdown) → str      │
│          • Build explanation from scoring factors               │
│          • Use templates: importance + player/team + context    │
│          • Keep to 1-2 sentences, non-technical                 │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                   Data Models (models.py)                        │
│                                                                  │
│  @dataclass GameEvent                                            │
│    • id, type, timestamp, quarter, player, team                 │
│    • description, importance, tags                              │
│                                                                  │
│  @dataclass UserPreference                                       │
│    • favorite_player: str | None                                │
│    • favorite_team: str | None                                  │
│                                                                  │
│  @dataclass ScoreBreakdown                                       │
│    • base_score: int                                            │
│    • player_boost: int                                          │
│    • team_boost: int                                            │
│    • context_boosts: dict[str, int]                             │
│    • total_score: int                                           │
│                                                                  │
│  @dataclass Highlight                                            │
│    • event: GameEvent                                           │
│    • rank: int                                                  │
│    • score: int                                                 │
│    • explanation: str                                           │
└──────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Input JSON → Parse to Models → Score Events → Rank & Filter → Generate Explanations → Output JSON
```

**Key Design Principles**:
1. **Pure Functions**: All scoring and selection logic is stateless (Article II)
2. **Type Safety**: All data flows through typed dataclasses (Article VII)
3. **Determinism**: No randomness, explicit tie-breaking (Article V)
4. **Explainability**: Every output includes human-readable reasoning (Article III)

---

## Data Model Design

### Input: `GameEvent`

```python
@dataclass
class GameEvent:
    """Represents a single event in a game."""
    id: str                    # Unique identifier
    type: str                  # Event type: "dunk", "three_pointer", "block", etc.
    timestamp: str             # Game clock: "Q4 02:15"
    quarter: int               # Quarter number: 1-4
    player: str                # Player name: "Stephen Curry"
    team: str                  # Team name: "Golden State Warriors"
    description: str           # Human-readable description
    importance: str            # One of: "critical", "high", "medium", "low"
    tags: list[str]            # Categorical tags: ["clutch", "game_winner", etc.]
```

**Validation Rules**:
- `importance` defaults to `"low"` if unknown (FR-012)
- Missing required fields → skip event or apply defaults (lenient validation per user clarification)
- `quarter` range: 1-4 (regulation); may extend for overtime if needed

### Input: `UserPreference`

```python
@dataclass
class UserPreference:
    """User's personalization settings."""
    favorite_player: str | None = None  # Optional player name
    favorite_team: str | None = None    # Optional team name
```

**Validation Rules**:
- Both fields optional (FR-011)
- `None` treated as "no preference"

### Internal: `ScoreBreakdown`

```python
@dataclass
class ScoreBreakdown:
    """Detailed scoring components for explainability."""
    base_score: int                     # From importance level
    player_boost: int                   # 0 or 30
    team_boost: int                     # 0 or 15
    context_boosts: dict[str, int]      # {"clutch": 20, "fourth_quarter": 10, ...}
    total_score: int                    # Sum of all components
```

**Purpose**: Enables transparent explanation generation (Article III)

### Output: `Highlight`

```python
@dataclass
class Highlight:
    """A selected highlight with explanation."""
    event: GameEvent           # Full event data
    rank: int                  # Position in output (1 = best)
    score: int                 # Final calculated score
    explanation: str           # Human-readable 1-2 sentence explanation
```

**JSON Output Format**:
```json
{
  "highlights": [
    {
      "event": { /* full GameEvent */ },
      "rank": 1,
      "score": 145,
      "explanation": "This critical game-winning shot by Stephen Curry sealed the championship in the final seconds."
    }
  ],
  "metadata": {
    "total_events": 15,
    "selected_count": 7,
    "preferences": { "favorite_player": "Stephen Curry", "favorite_team": null }
  }
}
```

---

## Scoring Algorithm Design

### Base Score by Importance

| Importance Level | Base Score | Rationale |
|------------------|------------|-----------|
| `critical` | **100** | Game-changing moments (game winners, championship clinchers) |
| `high` | **75** | Significant plays (momentum shifts, clutch 3-pointers) |
| `medium` | **50** | Notable moments (dunks, blocks, assists) |
| `low` | **25** | Routine plays (standard baskets, fouls) |

### Score Modifiers

| Modifier | Points | Condition | Specification Reference |
|----------|--------|-----------|------------------------|
| **Favorite player** | **+30** | `event.player == preference.favorite_player` | FR-004, US-2 |
| **Favorite team** | **+15** | `event.team == preference.favorite_team` | FR-004, US-3 |
| **Clutch moment** | **+20** | `"clutch" in event.tags` | Contextual boost |
| **Highlight reel quality** | **+15** | `"highlight_reel" in event.tags` | Contextual boost |
| **Fourth quarter** | **+10** | `event.quarter == 4` | Late-game drama |
| **Game winner** | **+25** | `"game_winner" in event.tags` | Decisive moment |
| **Buzzer beater** | **+20** | `"buzzer_beater" in event.tags` | Dramatic timing |

**Formula**:
```
total_score = base_score 
            + player_boost 
            + team_boost 
            + sum(context_boosts)
```

**Example Calculation**:
```python
Event: Stephen Curry three-pointer, Q4, importance="high", tags=["clutch", "highlight_reel"]
Preference: favorite_player="Stephen Curry"

base_score = 75 (high importance)
player_boost = 30 (favorite player match)
team_boost = 0 (no team preference)
context_boosts = {"clutch": 20, "highlight_reel": 15, "fourth_quarter": 10}

total_score = 75 + 30 + 0 + 45 = 150
```

### Selection Rules

1. **Force-include critical events**: All `importance="critical"` events MUST be in output (FR-006)
2. **Apply personalization**: Boost events matching user preferences (FR-014, FR-015)
3. **Sort by score**: Descending order (highest first) (FR-007)
4. **Apply count constraints**: Select 5-8 events unless fewer than 5 total (FR-005)
5. **Maintain narrative**: Include significant opponent plays if needed (FR-015)

### Tie-Breaking Rules (Deterministic)

When two events have identical `total_score`:

1. **Higher quarter wins** → Later events more dramatic (Q4 > Q3 > Q2 > Q1)
2. **Higher importance wins** → critical > high > medium > low
3. **Alphabetical event ID** → Deterministic fallback (FR-013, SC-004)

**Implementation**:
```python
def sort_key(event: ScoredEvent) -> tuple:
    return (
        -event.score,                    # Descending score
        -event.event.quarter,            # Descending quarter
        -importance_rank(event.event.importance),  # Descending importance
        event.event.id                   # Ascending ID (alphabetical)
    )
```

---

## Explanation Generation Design

### Template System

Each explanation combines:
1. **Importance context** (why it's a highlight)
2. **Personalization context** (if applicable)
3. **Situational context** (clutch, timing, etc.)

### Template Patterns

| Scenario | Template | Example |
|----------|----------|---------|
| Critical + Player pref | `"This {importance} {event_type} by {player} {context}"` | "This critical game-winning shot by Stephen Curry sealed the championship." |
| High + No pref | `"A {importance} {event_type} {context}"` | "A high-impact three-pointer that shifted momentum in the fourth quarter." |
| Medium + Team pref | `"This {event_type} by your favorite team, the {team}, {context}"` | "This dunk by your favorite team, the Warriors, energized the crowd." |
| Any + Multiple factors | Combine contexts | "Selected for your favorite player LeBron James in a clutch moment." |

### Explanation Constraints (SC-007)

- **Length**: 1-2 sentences maximum
- **Language**: Non-technical, fan-friendly
- **Content**: Must reference specific scoring factors
- **Tone**: Descriptive and engaging

### Implementation Approach

```python
def generate_explanation(event: GameEvent, breakdown: ScoreBreakdown) -> str:
    parts = []
    
    # Importance context
    if event.importance == "critical":
        parts.append(f"This critical {event.type}")
    elif breakdown.player_boost > 0:
        parts.append(f"Selected for your favorite player {event.player}")
    
    # Contextual factors
    if "game_winner" in event.tags:
        parts.append("sealed the victory")
    elif "clutch" in event.tags and event.quarter == 4:
        parts.append("in a clutch fourth-quarter moment")
    
    # Combine into 1-2 sentences
    return " ".join(parts) + "."
```

---

## Traceability Matrix

| User Story | Functional Requirements | Implementation Components | Test Coverage |
|------------|------------------------|---------------------------|---------------|
| **US-1: Basic Selection** | FR-001, FR-003, FR-005, FR-006, FR-007 | `select_highlights()`, `score_event()`, `rank_and_filter()` | `test_basic_selection_returns_5_to_8_highlights`, `test_critical_events_always_included`, `test_events_ranked_by_score` |
| **US-2: Player Personalization** | FR-004, FR-014 | `score_event()` with `player_boost` | `test_player_preference_boost_applied`, `test_50_percent_player_involvement`, `test_player_boost_value` |
| **US-3: Team Personalization** | FR-004, FR-015 | `score_event()` with `team_boost` | `test_team_preference_boost_applied`, `test_opponent_plays_included_for_narrative` |
| **US-4: Explanations** | FR-008 | `generate_explanation()` | `test_every_highlight_has_explanation`, `test_explanation_length_1_to_2_sentences`, `test_explanation_references_scoring_factors`, `test_no_technical_jargon` |
| **US-5: Edge Cases** | FR-010, FR-011, FR-012 | Input validation, default handling | `test_empty_event_list`, `test_null_favorite_player`, `test_null_favorite_team`, `test_unknown_importance_defaults_to_low`, `test_missing_fields_handled_gracefully` |
| **Constitution: Determinism** | FR-009, FR-013 | Tie-breaking logic in `rank_and_filter()` | `test_identical_inputs_produce_identical_outputs`, `test_tie_breaking_by_quarter`, `test_tie_breaking_by_importance`, `test_tie_breaking_by_id` |

**Coverage Goals**:
- **Unit tests**: 100% coverage of pure functions (`score_event`, `rank_and_filter`, `generate_explanation`)
- **Integration tests**: End-to-end JSON input → JSON output with all 5 user stories
- **Edge case tests**: All 7 edge cases from specification

---

## Implementation Phases

### Phase 0: Setup & Foundation
- Initialize Python package structure
- Create `pyproject.toml` with project metadata
- Setup pytest configuration
- Create sample data fixtures from `shared/sample_data.json`

### Phase 1: Data Models (Article IV)
- Implement `models.py` with all 4 dataclasses
- Add JSON serialization/deserialization helpers
- Write unit tests for model validation

### Phase 2: Scoring Logic (Article II + V)
- Implement `score_event()` with base scoring + modifiers
- Write unit tests for each scoring rule
- Verify deterministic behavior

### Phase 3: Selection Logic (Article VI)
- Implement `rank_and_filter()` with tie-breaking
- Write unit tests for selection constraints (5-8 highlights, critical events)
- Integration tests with scoring

### Phase 4: Explanation Generation (Article III)
- Implement `generate_explanation()` with template system
- Write unit tests for explanation quality (length, content, tone)
- Verify all highlights have explanations

### Phase 5: CLI Interface
- Implement `cli.py` for JSON I/O
- Add error handling and user-friendly messages
- Write integration tests for end-to-end flow

### Phase 6: Edge Case Hardening (US-5)
- Implement all edge case handlers
- Write dedicated test suite for `test_edge_cases.py`
- Verify SC-006 (zero crashes)

### Phase 7: Performance Validation
- Benchmark against SC-001 (<100ms for 15 events)
- Benchmark against SC-005 (<1s for 1000 events)
- Optimize if needed

### Phase 8: Documentation
- Create `data-model.md` with schema details
- Create `quickstart.md` with usage examples
- Create `contracts/input-output.json` with examples
- Update main `README.md`

---

## Verification Checklist

Before declaring implementation complete:

- [ ] All 15 functional requirements (FR-001 to FR-015) verified
- [ ] All 8 success criteria (SC-001 to SC-008) measured and passed
- [ ] All 18 acceptance scenarios from 5 user stories have passing tests
- [ ] All 7 constitution principles validated (with pytest exception documented)
- [ ] All 7 edge cases handled gracefully
- [ ] Performance benchmarks meet targets (<100ms, <1s)
- [ ] 100% test coverage for core logic (scoring, selection, explanation)
- [ ] Documentation complete (data-model, quickstart, contracts)
- [ ] Code formatted with `black`, linted with `pylint` or `flake8`
- [ ] Type hints validated with `mypy` (strict mode)

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Scoring algorithm produces unexpected results | Medium | High | Comprehensive test suite with 18 acceptance scenarios + traceability matrix |
| Performance targets not met (SC-001, SC-005) | Low | Medium | Algorithm is O(n log n) due to sorting; benchmarking in Phase 7 with optimization if needed |
| Explanation quality varies | Medium | Medium | Template system with examples; manual review of test outputs |
| Edge cases not fully covered | Low | High | Dedicated edge case test suite (US-5); 7 identified cases |
| pytest exception causes production issues | Very Low | Low | pytest is dev-only dependency; production uses stdlib only |

**Overall Risk Level**: **LOW** - Clear requirements, simple algorithm, comprehensive test coverage planned

---

**Version**: 1.0.0 | **Author**: Planning Agent | **Status**: ✅ READY FOR IMPLEMENTATION
