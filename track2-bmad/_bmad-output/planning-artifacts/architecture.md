---
stepsCompleted: ["step-01-init", "step-02-context", "step-03-starter", "step-04-decisions", "step-05-patterns", "step-06-structure", "step-07-validation", "step-08-complete"]
workflowStatus: "complete"
completionDate: "2026-02-17"
inputDocuments:
  - /Users/or.shohat/Documents/Git/WSC/speckit-bmad/track2-bmad/_bmad-output/planning-artifacts/prd.md
workflowType: 'architecture'
project_name: 'AI Highlight Selector (Track2 - BMAD)'
user_name: 'Or'
date: '2026-02-17'
---

# Architecture Decision Document - AI Highlight Selector (Track2 - BMAD)

**Author:** Or  
**Date:** 2026-02-17  
**Project:** AI Highlight Selector - Track2 BMAD Implementation

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

---

## 1. Project Context Analysis

### 1.1 Requirements Overview

The AI Highlight Selector is a **Python library + CLI tool** designed to algorithmically curate sports highlights from game event data. The PRD defines **33 functional requirements** organized across 7 capability areas:

**Event Processing & Scoring (FR-001 to FR-007)**
- Accept game events with structured data (type, timestamp, player, team, importance, tags)
- Accept optional user preferences (favorite player/team)
- Calculate multi-factor scores combining base importance (25-100 points), personalization boosts (+30 player, +15 team), and context tags (clutch, buzzer-beater, etc.)

**Highlight Selection & Ranking (FR-008 to FR-013)**
- Select 5-8 highlights from scored events
- Force-include all critical importance events
- Apply deterministic tie-breaking (quarter → importance → event ID)
- Balance personalization with game narrative (50% favorite player when sufficient events exist)

**Explanation Generation (FR-014 to FR-016)**
- Generate 1-2 sentence explanations in fan-friendly language
- Reference scoring factors transparently
- Avoid technical jargon

**Edge Case Handling (FR-017 to FR-021)**
- Gracefully handle empty lists, null preferences, missing fields
- Validate player/team names with helpful error messages listing available options
- Use sensible defaults for malformed data

**CLI Interface (FR-022 to FR-027)**
- Command-line flags: `--player`, `--team`, `--only`
- Pretty formatted output with visual hierarchy
- Helpful validation errors

**Programmatic API (FR-028 to FR-030)**
- Public `select_highlights()` function
- Type-safe models (GameEvent, UserPreference, Highlight, ScoreBreakdown)
- JSON serialization support

**Deterministic Behavior (FR-031 to FR-033)**
- 100% reproducible output for identical inputs
- No randomness anywhere in the system

### 1.2 Technical Constraints

The **25 non-functional requirements** establish critical architectural constraints:

**Performance Constraints (NFR-001 to NFR-004)**
- **<100ms** for 15 events (typical game)
- **<1s** for 1000 events (stress test)
- **O(n log n)** algorithm complexity (sorting-dominated)
- Consistent performance regardless of content/preferences

**Quality & Determinism (NFR-005 to NFR-013)**
- **100% deterministic** behavior (no random elements)
- **≥88% test coverage** across all modules
- **Type hints** on all public APIs (mypy strict mode)
- **Google-style docstrings** on all public functions
- **Black formatting** (PEP 8 compliance)
- Comprehensive edge case handling without crashes

**Maintainability & Dependencies (NFR-014 to NFR-018)**
- **Pure function design** for core business logic (scoring, selection, explanation)
- **Strict separation of concerns** (models / logic / interface layers)
- **Zero runtime dependencies** (Python stdlib only)
- Documented dev dependencies (pytest, black, mypy)

**Usability & Portability (NFR-019 to NFR-025)**
- Helpful, actionable CLI error messages
- Simple API requiring minimal documentation
- Python 3.10+ compatibility
- Cross-platform support (Linux, macOS, Windows)

### 1.3 Project Scale & Complexity

**Classification:** Developer tool, general domain, **low complexity**

**Scale Indicators:**
- Estimated **400-600 lines** of production code
- **3-4 modules** (models, selector, cli, tests)
- **99 tests** (validated from Track1 reference implementation)
- **Single developer** project
- **3-4 week** implementation timeline

**Complexity Indicators:**
- **Simple algorithm:** Multi-factor scoring + sorting + top-k selection
- **No external systems:** Self-contained processing with file I/O only
- **Clear domain:** Sports highlight curation with well-defined rules
- **Reference implementation available:** Track1 SpecKit provides validation

### 1.4 Cross-Cutting Concerns

These concerns span multiple architectural components and must be addressed system-wide:

| Concern | Architectural Impact |
|---------|---------------------|
| **Type Safety** | All modules need type hints; mypy strict mode compliance required; affects API design and internal contracts |
| **Determin** | Must be enforced in scoring calculation, selection algorithm, tie-breaking, and explanation generation; no randomness allowed anywhere |
| **Error Handling** | Consistent validation strategy across all layers (models, logic, CLI); helpful messages without stack traces for user-facing errors |
| **Testing** | All modules need comprehensive unit + integration tests; performance benchmarks required; edge case coverage mandatory |
| **Documentation** | Public API docstrings required; README with quick start; data-model.md for schemas; quickstart.md for step-by-step guide |
| **Performance** | Algorithm efficiency critical in scoring (O(n)) and selection (O(n log n)); no heavy libraries allowed due to stdlib-only constraint |
| **Separation of Concerns** | Clean boundaries between data models, business logic, and interface layers; pure functions for core logic |
| **Pure Functions** | Core business logic (scoring, selection, explanation) must be stateless for testability and determinism |

---

## 2. Technology Starter Selection

### 2.1 Language & Runtime Environment

**Selected: Python 3.10+ (stdlib only)**

**Rationale:**
- NFR-016 mandates **zero runtime dependencies** - only Python standard library allowed
- NFR-023 requires Python 3.10+ for modern type hints (PEP 604 union syntax `str | None`)
- NFR-024 requires cross-platform compatibility (Linux, macOS, Windows) - stdlib guarantees this
- User's Track1 implementation validated this approach successfully

**Alternatives Rejected:**
- Python with external libraries (numpy, pandas) → Violates NFR-016
- Other languages → Requires rewriting validated Track1 reference implementation

### 2.2 Development Dependencies

**Testing: pytest + pytest-cov**

**Rationale:**
- Industry-standard testing with fixtures, parametrization, and better assertions
- Track1 validated 99 tests with 88% coverage using pytest
- Development-only dependency (not runtime) - preserves production security posture
- Supports 33 FRs + 25 NFRs efficiently with readable test code

**Code Quality: black + mypy**

**Rationale:**
- NFR-012 mandates black formatting (PEP 8 compliance)
- NFR-010, NFR-013 mandate type hints with mypy strict mode validation
- Both are development-time tools, no runtime impact

### 2.3 Data Serialization

**Selected: Python dataclasses + json module (stdlib)**

**Rationale:**
- NFR-016 requires stdlib-only solution
- Python 3.10+ `@dataclass` provides clean type-safe models
- Standard `json` module handles serialization/deserialization
- FR-030 requires JSON interchange format support

**Alternatives Rejected:**
- Pydantic → External dependency, violates NFR-016
- Marshmallow → External dependency, violates NFR-016

### 2.4 Project Structure

**Selected: Single Python Package ("highlight_selector/")**

**Rationale:**
- Low complexity project (~500 LOC) fits single package scope
- NFR-015 requires strict separation of concerns achieved via module organization:
  - `models.py` - Data models only
  - `selector.py` - Core business logic
  - `cli.py` - Command-line interface
- Track1 validated this structure successfully

---

## 3. Key Architecture Decisions

### 3.1 Pure Function Design for Core Logic

**Decision:** All scoring, selection, and explanation functions are stateless pure functions

**Rationale:**
- NFR-014 mandates pure functions for testability
- NFR-005 requires 100% deterministic behavior (pure functions guarantee this)
- Enables comprehensive unit testing without mocks or fixtures
- Simplifies reasoning about correctness

**Implementation:**
```python
def score_event(event: GameEvent, preferences: UserPreference) -> ScoreBreakdown:
    """Pure function: same inputs always produce same output"""
    # No side effects, no state mutation
    pass

def select_highlights(
    events: list[GameEvent], 
    preferences: UserPreference,
    max_count: int = 8,
    min_count: int = 5
) -> list[Highlight]:
    """Pure function: deterministic selection"""
    pass
```

### 3.2 Explicit Tie-Breaking for Determinism

**Decision:** Three-level tie-breaking when events have identical scores

**Rationale:**
- NFR-005 mandates 100% deterministic behavior
- FR-011 requires explicit tie-breaking rules
- Sorting alone on score would be non-deterministic for ties

**Implementation:**
```python
def sort_key(scored_event: tuple[GameEvent, ScoreBreakdown]) -> tuple:
    event, breakdown = scored_event
    return (
        -breakdown.total_score,              # Primary: highest score
        -event.quarter,                       # Secondary: later quarter
        -importance_to_rank(event.importance), # Tertiary: higher importance
        event.id                              # Final: alphabetical ID
    )
```

### 3.3 Template-Based Explanation Generation

**Decision:** Use template strings with variable substitution for explanations

**Rationale:**
- NFR-007 requires 100% of highlights have explanations
- NFR-008 mandates 1-2 sentences without technical jargon
- FR-015 requires explanations to reference scoring factors
- Templates ensure consistency and quality

**Implementation:**
```python
def generate_explanation(event: GameEvent, breakdown: ScoreBreakdown, preferences: UserPreference) -> str:
    """Generate fan-friendly explanation from scoring factors"""
    parts = []
    
    if event.importance == "critical":
        parts.append(f"This critical {event.type} by {event.player}")
    elif breakdown.player_boost > 0:
        parts.append(f"Selected for your favorite player {event.player}")
    
    # Add contextual factors from tags and context_boosts
    # Combine into 1-2 sentences
    return " ".join(parts) + "."
```

### 3.4 Force-Include Critical Events

**Decision:** All events with `importance="critical"` are always included in output

**Rationale:**
- FR-009 mandates force-inclusion of critical events
- Critical events represent game-defining moments (game winners, championship clinchers)
- User preference should not override objective importance

**Implementation:**
```python
# Step 1: Separate critical from non-critical
critical_events = [e for e in scored_events if e.event.importance == "critical"]
other_events = [e for e in scored_events if e.event.importance != "critical"]

# Step 2: Sort non-critical by score
other_events.sort(key=sort_key)

# Step 3: Select from non-critical to reach target count (5-8)
remaining_slots = max(min_count - len(critical_events), 0)
selected_other = other_events[:remaining_slots]

# Step 4: Combine and rank
final_highlights = critical_events + selected_other
final_highlights.sort(key=sort_key)
```

### 3.5 Lenient Input Validation with Defaults

**Decision:** Apply sensible defaults for missing/malformed event data

**Rationale:**
- FR-019 requires unknown importance levels default to "low"
- FR-020 requires handling events with missing optional fields
- NFR-006 requires handling malformed data without crashes
- User specified "lenient validation" approach in PRD clarifications

**Default Rules:**
- `importance` → `"low"` if unknown/missing
- `quarter` → `1` if missing
- `player` → `"Unknown"` if missing
- `team` → `"Unknown"` if missing
- `tags` → `[]` if missing
- `description` → `""` if missing

### 3.6 CLI Validation with Helpful Messages

**Decision:** Validate player/team names and provide actionable error messages

**Rationale:**
- FR-021 requires validation with helpful error messages listing available options
- FR-027 requires validation errors for player/team not found
- NFR-019 mandates helpful, actionable CLI error messages
- Improves user experience for typos and data mismatches

**Implementation:**
```python
def validate_preferences(events: list[GameEvent], preferences: UserPreference) -> None:
    """Validate preferences against available events"""
    if preferences.favorite_player:
        available_players = {e.player for e in events}
        if preferences.favorite_player not in available_players:
            print(f"⚠️  Player '{preferences.favorite_player}' not found in game data.")
            print(f"   Available players: {', '.join(sorted(available_players))}")
            sys.exit(1)
    # Similar for favorite_team
```

---

## 4. Design Patterns & Principles

### 4.1 Layered Architecture

**Pattern:** Three-layer separation (Models / Logic / Interface)

**Layers:**
1. **Data Models Layer** (`models.py`)
   - Dataclass definitions: `GameEvent`, `UserPreference`, `ScoreBreakdown`, `Highlight`
   - JSON serialization helpers
   - No business logic

2. **Business Logic Layer** (`selector.py`)
   - Pure functions: `score_event()`, `select_highlights()`, `generate_explanation()`
   - No I/O, no side effects
   - Fully testable in isolation

3. **Interface Layer** (`cli.py`)
   - Command-line argument parsing
   - File I/O (read JSON, write results)
   - Calls business logic layer
   - Error handling and validation

**Benefits:**
- Clear separation of concerns (NFR-015)
- Each layer independently testable
- Pure functions in business logic (NFR-014)

### 4.2 Template Method Pattern (for Explanations)

**Pattern:** Template-based text generation with variable substitution

**Implementation:**
- Base templates for common scenarios
- Variable substitution based on `ScoreBreakdown` factors
- Ensures consistent, fan-friendly language (NFR-008)

### 4.3 Strategy Pattern (for Scoring)

**Pattern:** Composable scoring strategy with base + modifiers

**Implementation:**
```python
# Base strategy: importance scoring
base_score = importance_to_score(event.importance)

# Modifier strategies: personalization
player_boost = 30 if matches_favorite_player else 0
team_boost = 15 if matches_favorite_team else 0

# Modifier strategies: contextual
context_boosts = calculate_context_boosts(event.tags, event.quarter)

# Combine all strategies
total_score = base_score + player_boost + team_boost + sum(context_boosts.values())
```

**Benefits:**
- Clear scoring transparency (Article III: Explainability)
- Easy to test each scoring component independently
- Modular - can add new modifiers without changing core algorithm

### 4.4 Immutable Data Pattern

**Pattern:** All dataclasses are immutable (frozen)

**Implementation:**
```python
@dataclass(frozen=True)
class GameEvent:
    """Immutable event data"""
    # fields...
```

**Benefits:**
- Supports pure function design (NFR-014)
- Prevents accidental state mutation
- Thread-safe by design
- Easier to reason about correctness

---

## 5. System Structure & Component Design

### 5.1 System Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                     CLI Entry Point (cli.py)                     │
│                                                                  │
│  • Parse command-line arguments (--player, --team, --only)      │
│  • Read JSON from stdin or file                                 │
│  • Validate player/team against event data                      │
│  • Call select_highlights() from business logic                 │
│  • Format and print results                                     │
└──────────────────────┬───────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│              Business Logic Layer (selector.py)                  │
│                                                                  │
│  select_highlights(events, prefs, max=8, min=5) → [Highlight]   │
│    │                                                             │
│    ├──▶ score_event(event, prefs) → ScoreBreakdown              │
│    │     • Calculate base score from importance (25-100)        │
│    │     • Apply player preference boost (+30)                  │
│    │     • Apply team preference boost (+15)                    │
│    │     • Apply contextual boosts (tags + quarter)             │
│    │                                                             │
│    ├──▶ select_and_rank(scored_events, max, min) → [Scored]    │
│    │     • Force-include all critical events                    │
│    │     • Sort by score with tie-breaking                      │
│    │     • Select top 5-8 events                                │
│    │                                                             │
│    └──▶ generate_explanation(event, breakdown, prefs) → str     │
│          • Build explanation from scoring factors               │
│          • Use templates: importance + player/team + context    │
│          • Keep to 1-2 sentences, non-technical                 │
└──────────────────────┬─────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│                   Data Models Layer (models.py)                  │
│                                                                  │
│  @dataclass(frozen=True) GameEvent                               │
│    • id, type, timestamp, quarter, player, team                 │
│    • description, importance, tags                              │
│                                                                  │
│  @dataclass(frozen=True) UserPreference                          │
│    • favorite_player: str | None                                │
│    • favorite_team: str | None                                  │
│                                                                  │
│  @dataclass(frozen=True) ScoreBreakdown                          │
│    • base_score, player_boost, team_boost                       │
│    • context_boosts: dict[str, int]                             │
│    • total_score (computed property)                            │
│                                                                  │
│  @dataclass(frozen=True) Highlight                               │
│    • event: GameEvent                                           │
│    • rank, score, explanation                                   │
└──────────────────────────────────────────────────────────────────┘
```

### 5.2 Data Flow

```
Input JSON 
   → Parse to GameEvent models
   → Score each event (base + personalization + context)
   → Select & rank highlights (force-include critical, sort, top-k)
   → Generate explanations for each
   → Format output
   → Output JSON / Pretty CLI display
```

### 5.3 Module Organization

```
highlight_selector/
├── __init__.py                  # Package exports (public API)
├── models.py                    # Data models (4 dataclasses)
├── selector.py                  # Business logic (pure functions)
└── cli.py                       # Command-line interface

tests/
├── __init__.py
├── conftest.py                  # Shared fixtures (sample events)
├── test_models.py               # Model validation tests
├── test_scoring.py              # Scoring algorithm tests
├── test_selection.py            # Selection & ranking tests
├── test_explanations.py         # Explanation generation tests
├── test_edge_cases.py           # Edge case handling tests
└── test_integration.py          # End-to-end integration tests
```

### 5.4 Public API Surface

**Core Function:**
```python
def select_highlights(
    events: list[GameEvent],
    preferences: UserPreference | None = None,
    max_count: int = 8,
    min_count: int = 5
) -> list[Highlight]:
    """
    Select 5-8 highlights from game events based on importance and preferences.
    
    Args:
        events: List of game events to process
        preferences: Optional user preferences (favorite player/team)
        max_count: Maximum highlights to return (default 8)
        min_count: Minimum highlights to return (default 5)
    
    Returns:
        List of Highlight objects ranked by score (best first)
    
    Raises:
        ValueError: If events list is invalid
    """
```

**Data Models:**
- `GameEvent` - Input event model
- `UserPreference` - Input preferences model
- `ScoreBreakdown` - Scoring transparency model
- `Highlight` - Output highlight model

**CLI Command:**
```bash
python -m highlight_selector.cli [OPTIONS]

Options:
  --player TEXT    Favorite player name
  --team TEXT      Favorite team name
  --only           Show only favorite player/team highlights
  --input FILE     Input JSON file (default: stdin)
  --output FILE    Output JSON file (default: stdout)
  --help           Show this message and exit
```

### 5.5 Component Responsibilities

| Component | Responsibilities | Dependencies | Tests |
|-----------|-----------------|--------------|-------|
| **models.py** | Define dataclasses, JSON serialization, validation defaults | stdlib (`dataclasses`, `json`) | `test_models.py` - Field validation, JSON round-trip |
| **selector.py** | Scoring algorithm, selection logic, explanation generation | `models.py` | `test_scoring.py`, `test_selection.py`, `test_explanations.py` |
| **cli.py** | Argument parsing, file I/O, validation, formatting | `models.py`, `selector.py`, stdlib (`argparse`, `json`, `sys`) | `test_integration.py` - End-to-end CLI tests |

---

## 6. Algorithm Specifications

### 6.1 Scoring Algorithm

**Complexity:** O(n) where n = number of events

**Base Scoring Table:**

| Importance | Base Score |
|-----------|------------|
| `critical` | 100 |
| `high` | 75 |
| `medium` | 50 |
| `low` | 25 |
| unknown | 25 (default) |

**Personalization Modifiers:**

| Modifier | Points | Condition |
|----------|--------|-----------|
| Favorite Player | +30 | `event.player == preferences.favorite_player` |
| Favorite Team | +15 | `event.team == preferences.favorite_team` |

**Contextual Modifiers (from tags):**

| Tag | Points | Rationale |
|-----|--------|-----------|
| `game_winner` | +25 | Decisive moment |
| `clutch` | +20 | High-pressure situation |
| `buzzer_beater` | +20 | Dramatic timing |
| `highlight_reel` | +15 | Visual appeal |
| Fourth Quarter | +10 | Late-game drama (when `quarter == 4`) |

**Formula:**
```
total_score = base_score 
            + player_boost 
            + team_boost 
            + sum(context_boosts from tags)
            + quarter_boost (if Q4)
```

### 6.2 Selection Algorithm

**Complexity:** O(n log n) due to sorting

**Steps:**
1. **Score all events** - O(n)
2. **Separate critical from non-critical** - O(n)
3. **Sort non-critical by score with tie-breaking** - O(n log n)
4. **Force-include all critical events**
5. **Fill remaining slots from sorted non-critical** (up to max_count)
6. **Ensure minimum count** (adjust if needed)
7. **Final sort of selected highlights** - O(k log k) where k ≤ 8
8. **Assign ranks** (1 = best)

**Tie-Breaking Rules:**
```python
sort_key = (
    -total_score,     # Descending score (highest first)
    -quarter,         # Descending quarter (later first)
    -importance_rank, # Descending importance (critical > high > medium > low)
    event_id          # Ascending ID (alphabetical)
)
```

### 6.3 Explanation Generation Algorithm

**Complexity:** O(1) per event

**Template Selection Logic:**
```
if importance == "critical":
    start with "This critical {type} by {player}"
elif player_boost > 0:
    start with "Selected for your favorite player {player}"
elif team_boost > 0:
    start with "This {type} by your favorite team, the {team}"
else:
    start with "A {importance} {type}"

# Add contextual phrases based on tags
if "game_winner" in tags:
    add "sealed the victory"
elif "clutch" in tags and quarter == 4:
    add "in a clutch fourth-quarter moment"
elif "buzzer_beater" in tags:
    add "with perfect timing at the buzzer"

# Combine into 1-2 sentences
```

---

## 7. Quality Attributes & NFR Mapping

### 7.1 Performance

| NFR | Target | Architecture Support |
|-----|--------|---------------------|
| NFR-001 | <100ms for 15 events | O(n log n) algorithm, no heavy libraries, pure Python stdlib |
| NFR-002 | <1s for 1000 events | Efficient sorting, minimal object creation |
| NFR-003 | O(n log n) complexity | Sorting dominates; scoring is O(n) |
| NFR-004 | Consistent performance | Pure functions, no I/O in core logic, deterministic execution |

### 7.2 Determinism & Reliability

| NFR | Requirement | Architecture Support |
|-----|------------|---------------------|
| NFR-005 | 100% deterministic | Pure functions, explicit tie-breaking, no randomness |
| NFR-006 | No crashes on edge cases | Lenient validation, sensible defaults, comprehensive error handling |

### 7.3 Explainability & Quality

| NFR | Requirement | Architecture Support |
|-----|------------|---------------------|
| NFR-007 | 100% of highlights have explanations | `generate_explanation()` called for every selected highlight |
| NFR-008 | 1-2 sentences, no jargon | Template-based generation with fan-friendly language |
| NFR-009 | ≥88% test coverage | Comprehensive test suite across 7 test modules |
| NFR-010 | Type hints on all public APIs | Full type annotations, mypy strict mode |
| NFR-011 | Google-style docstrings | Enforced on all public functions |
| NFR-012 | Black formatting | Pre-commit hook / CI validation |
| NFR-013 | Mypy strict mode | Type checking in CI pipeline |

### 7.4 Maintainability

| NFR | Requirement | Architecture Support |
|-----|------------|---------------------|
| NFR-014 | Pure functions for core logic | All scoring/selection/explanation functions are stateless |
| NFR-015 | Strict separation of concerns | Three-layer architecture (Models / Logic / Interface) |
| NFR-016 | Zero runtime dependencies | Python stdlib only (pytest is dev-only) |
| NFR-017 | Documented dev dependencies | `pyproject.toml` with clear rationale |
| NFR-018 | Single responsibility principle | Each function has one clear purpose |

### 7.5 Usability & Portability

| NFR | Requirement | Architecture Support |
|-----|------------|---------------------|
| NFR-019 | Helpful CLI error messages | Validation with available options listed |
| NFR-020 | Formatted CLI output | Pretty-print with visual hierarchy |
| NFR-021 | Simple API | Single `select_highlights()` function, minimal config |
| NFR-022 | Working code examples | README + quickstart.md with examples |
| NFR-023 | Python 3.10+ | Modern type hints (PEP 604: `str | None`) |
| NFR-024 | Cross-platform | Stdlib-only guarantees portability |
| NFR-025 | No OS-specific features | Stdlib file I/O only, no OS calls |

---

## 8. Validation & Traceability

### 8.1 Requirements Coverage

**Functional Requirements → Architecture Mapping:**

| FR Group | FRs | Architecture Component | Validation |
|----------|-----|----------------------|------------|
| Event Processing & Scoring | FR-001 to FR-007 | `score_event()` in selector.py | Unit tests verify all scoring rules |
| Highlight Selection & Ranking | FR-008 to FR-013 | `select_and_rank()` in selector.py | Unit tests for selection constraints + tie-breaking |
| Explanation Generation | FR-014 to FR-016 | `generate_explanation()` in selector.py | Unit tests for template quality |
| Edge Case Handling | FR-017 to FR-021 | Validation logic in models.py + cli.py | Dedicated edge case test suite |
| CLI Interface | FR-022 to FR-027 | cli.py with argparse | Integration tests for CLI flows |
| Programmatic API | FR-028 to FR-030 | Public API in __init__.py | API usage tests |
| Deterministic Behavior | FR-031 to FR-033 | Pure functions + tie-breaking | Determinism tests (identical inputs) |

### 8.2 Cross-Cutting Concerns → Implementation

| Concern | Implementation Strategy | Validation Method |
|---------|------------------------|-------------------|
| **Type Safety** | Type hints on all functions, mypy strict mode | CI: mypy --strict |
| **Determinism** | Pure functions, explicit tie-breaking, no randomness | Test: identical inputs produce identical outputs |
| **Error Handling** | Lenient defaults, helpful CLI messages | Edge case test suite |
| **Testing** | 99 tests across 7 modules, pytest fixtures | CI: pytest with coverage report (≥88%) |
| **Documentation** | Docstrings, README, quickstart.md, data-model.md | Manual review + doc generation |
| **Performance** | O(n log n) algorithm, no heavy processing | Benchmarks: <100ms (15 events), <1s (1000 events) |
| **Separation** | Three layers (Models / Logic / Interface) | Architecture review + import analysis |
| **Pure Functions** | Stateless core logic | Unit tests without mocks/fixtures |

### 8.3 Architecture Principles Verification

| Principle | Architecture Decision | Verification Method |
|-----------|----------------------|---------------------|
| **Simplicity First** | Single package, 3 modules, ~500 LOC | LOC count, complexity metrics |
| **Testability** | Pure functions, no side effects | 99 unit tests, no mocks needed |
| **Explainability** | Template-based explanations for 100% of highlights | Test coverage for generation |
| **Data-Driven** | 4 dataclasses with JSON serialization | Schema validation tests |
| **Determinism** | Explicit tie-breaking, no randomness | Determinism test suite |
| **Separation** | Models / Logic / Interface layers | Import dependency graph |
| **No Dependencies** | Stdlib only (pytest is dev-only) | Dependency audit |

---

## 9. Risk Mitigation & Constraints

### 9.1 Technical Risks

| Risk | Probability | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| Scoring algorithm produces unexpected results | Medium | High | **Comprehensive test suite** with 25+ test cases; Track1 reference validates approach |
| Performance targets not met (<100ms, <1s) | Low | Medium | **O(n log n) algorithm** is efficient; early benchmarking; Track1 proves feasibility |
| Explanation quality varies | Medium | Medium | **Template system** ensures consistency; manual review in tests |
| Edge cases not fully covered | Low | High | **Dedicated edge case test module**; 7 identified scenarios |
| Type safety violations | Low | Low | **mypy strict mode** in CI catches issues early |

### 9.2 Architectural Constraints

| Constraint | Impact on Design | Mitigation |
|-----------|-----------------|------------|
| **Zero runtime dependencies** (NFR-016) | Cannot use external libraries (numpy, pandas, pydantic) | Use stdlib dataclasses + json; proven viable in Track1 |
| **100% determinism** (NFR-005) | No randomness, explicit tie-breaking everywhere | Pure functions + documented tie-breaking rules |
| **Performance targets** (NFR-001, NFR-002) | Algorithm must be efficient | O(n log n) with sorting, no heavy processing |
| **Type safety** (NFR-010, NFR-013) | All functions need type hints | Mypy strict mode enforced, Python 3.10+ features |
| **88% test coverage** (NFR-009) | High test effort required | 99 tests across 7 modules, pytest fixtures |

### 9.3 Assumptions & Dependencies

**Assumptions:**
1. Game event data follows defined schema (GameEvent model)
2. Importance levels are limited to: critical, high, medium, low
3. Maximum 1000 events per game (stress test boundary)
4. Python 3.10+ available in target environments
5. Sample data in Track1 represents typical usage patterns

**External Dependencies:**
- None (runtime) - stdlib only per NFR-016
- pytest, black, mypy (development) - documented and justified

**Reference Implementation:**
- Track1 SpecKit implementation provides validation and comparison baseline
- 99 tests with 88% coverage demonstrate feasibility
- ~500 LOC implementation proves scope is achievable

---

## 10. Implementation Roadmap

### Phase 0: Foundation
- Initialize package structure
- Setup pyproject.toml with metadata
- Configure pytest with coverage
- Create shared test fixtures

### Phase 1: Data Models
- Implement 4 dataclasses in models.py
- Add JSON serialization helpers
- Write model validation tests

### Phase 2: Scoring Logic
- Implement `score_event()` function
- Add personalization boosts
- Add contextual boosts
- Write comprehensive scoring tests

### Phase 3: Selection Logic
- Implement `select_and_rank()` function
- Add force-include logic for critical events
- Add tie-breaking rules
- Write selection constraint tests

### Phase 4: Explanation Generation
- Implement `generate_explanation()` function
- Create template system
- Write explanation quality tests

### Phase 5: CLI Interface
- Implement cli.py with argparse
- Add validation with helpful messages
- Add pretty-print formatting
- Write integration tests

### Phase 6: Edge Case Hardening
- Implement all edge case handlers
- Write dedicated edge case test suite
- Validate zero crashes requirement

### Phase 7: Performance & Quality
- Run performance benchmarks
- Validate test coverage ≥88%
- Run mypy strict mode
- Format with black

### Phase 8: Documentation
- Create data-model.md
- Create quickstart.md
- Create contract examples
- Update README.md

---

## 11. Architecture Decision Summary

**Core Philosophy:** Simple, testable, deterministic, explainable

**Key Decisions:**
1. ✅ Python stdlib-only (zero runtime dependencies)
2. ✅ Pure function design for all business logic
3. ✅ Three-layer architecture (Models / Logic / Interface)
4. ✅ Explicit tie-breaking for 100% determinism
5. ✅ Template-based explanation generation
6. ✅ Force-include critical events
7. ✅ Lenient validation with helpful error messages
8. ✅ Immutable dataclasses for all models

**Quality Gates:**
- ✅ ≥88% test coverage across all modules
- ✅ mypy strict mode passes
- ✅ black formatting passes
- ✅ Performance benchmarks pass (<100ms, <1s)
- ✅ Zero crashes on edge cases
- ✅ 100% deterministic behavior verified

**Success Metrics:**
- All 33 functional requirements implemented and tested
- All 25 non-functional requirements validated
- Direct comparison with Track1 shows BMAD methodology effectiveness
- Documentation complete and comprehensive

---

**Document Status:** ✅ COMPLETE  
**Date Completed:** 2026-02-17  
**Ready for:** Implementation Phase (Epic & Story Creation)

