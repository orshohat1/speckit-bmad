# Story 1.1: GameEvent Data Model

Status: review

## Story

As a developer,
I want a strongly-typed GameEvent model that represents a single game event,
So that I can reliably work with game event data throughout the system.

## Acceptance Criteria

**Given** I am creating a new GameEvent instance
**When** I provide all required fields (id, type, timestamp, quarter, player, team, description, importance, tags)
**Then** the GameEvent is created successfully with all fields accessible

**And** the model includes type hints for all fields (str, int, list, etc.)

**And** importance field accepts valid values: "critical", "high", "medium", "low"

**And** tags field is a list of strings (can be empty)

**And** the model is defined as a dataclass in models.py module

**And** all fields have appropriate default values where applicable (tags defaults to empty list)

**And** the model includes a docstring describing its purpose and fields

**Requirements Fulfilled:** FR-001, NFR-010, NFR-011

## Tasks / Subtasks

- [x] Create highlight_selector package structure (AC: setup)
  - [x] Create `highlight_selector/` directory
  - [x] Create `highlight_selector/__init__.py`
  - [x] Create `highlight_selector/models.py`
  
- [x] Implement GameEvent dataclass (AC: 1, 2, 3, 4, 5, 6, 7)
  - [x] Define @dataclass decorator
  - [x] Add all required fields with type hints (id: str, type: str, timestamp: str, quarter: int, player: str, team: str, description: str, importance: str, tags: list[str])
  - [x] Set default value for tags field (field(default_factory=list))
  - [x] Add comprehensive Google-style docstring explaining purpose and all fields
  
- [x] Write unit tests for GameEvent (AC: all)
  - [x] Test instantiation with all fields
  - [x] Test instantiation with empty tags (default)
  - [x] Test field accessibility
  - [x] Test type hints are present (mypy validation)
  - [x] Test all valid importance values ("critical", "high", "medium", "low")

## Dev Notes

### Epic Context

This story is the **first story in Epic 1: Data Models and Core Types**. This epic creates the foundational data structures for the entire system. The GameEvent model is the most fundamental piece - it represents the input data that flows through the entire selection pipeline.

**Epic 1 Overview:**
- Story 1.1: GameEvent (this story) - Input event model
- Story 1.2: UserPreference - Personalization settings
- Story 1.3: ScoreBreakdown - Scoring transparency
- Story 1.4: Highlight - Output model
- Story 1.5: JSON Serialization - Data interchange

### Architecture Requirements

**Technology Stack:**
- Python 3.10+ (required for modern type hints)
- Standard library ONLY (NFR-016) - no external runtime dependencies
- Development dependencies: pytest, black, mypy (dev-time only)

**Module Location:**
- Create `highlight_selector/` package in `track2-bmad/` directory
- Define GameEvent in `highlight_selector/models.py`
- This module will contain ALL data models (Stories 1.1-1.4)

**Code Quality Standards (CRITICAL):**
1. **Type Hints (NFR-010, NFR-013):**
   - All fields must have explicit type annotations
   - Use Python 3.10+ syntax: `list[str]` not `List[str]`
   - Must pass `mypy --strict` validation
   
2. **Docstrings (NFR-011):**
   - Google-style format required
   - Class docstring explaining purpose
   - Document all attributes with their types and meanings
   
3. **Formatting (NFR-012):**
   - Must pass `black` formatting (PEP 8 compliance)
   - Run `black highlight_selector/` before committing

4. **Data Classes:**
   - Use `@dataclass` decorator from dataclasses module
   - Leverages automatic __init__, __repr__, __eq__
   - Enables clean, type-safe model definitions

### Technical Implementation Details

**GameEvent Field Specifications:**

```python
@dataclass
class GameEvent:
    """Represents a single game event with metadata and importance scoring.
    
    A GameEvent captures a moment in the game that could potentially be
    selected as a highlight. It includes timing information, player/team
    attribution, importance level, and optional context tags.
    
    Attributes:
        id: Unique identifier for the event (e.g., "event_001")
        type: Type of play (e.g., "dunk", "three_pointer", "block")
        timestamp: Game clock time when event occurred (e.g., "Q4 2:45")
        quarter: Quarter number (1-4 for regulation, 5+ for overtime)
        player: Name of player who performed the action
        team: Name of the team (e.g., "Lakers", "Celtics")
        description: Human-readable description of what happened
        importance: Importance level - must be "critical", "high", "medium", or "low"
        tags: Optional context tags like "clutch", "buzzer_beater", "game_winner"
              Defaults to empty list if not provided.
    """
    id: str
    type: str
    timestamp: str
    quarter: int
    player: str
    team: str
    description: str
    importance: str  # "critical", "high", "medium", "low"
    tags: list[str] = field(default_factory=list)
```

**Importance Values (Critical for Scoring):**
- `"critical"` → 100 points (game-defining moments)
- `"high"` → 75 points (important plays)
- `"medium"` → 50 points (noteworthy moments)
- `"low"` → 25 points (standard plays)

These values are used by the scoring engine (Epic 2) but validated here.

**Tags (Context for Scoring Boosts):**
- Tags are optional metadata providing additional context
- Common tags from requirements:
  - `"clutch"` → +20 points
  - `"game_winner"` → +25 points
  - `"buzzer_beater"` → +15 points
  - `"highlight_reel"` → +15 points
  - `"fourth_quarter"` → +10 points
- Empty list is valid (no context boosts applied)

### Project Structure

**File Organization:**
```
track2-bmad/
├── highlight_selector/          # Main package
│   ├── __init__.py              # Package initialization
│   ├── models.py                # Data models (THIS STORY)
│   ├── selector.py              # Core logic (Epic 2-3)
│   └── cli.py                   # CLI interface (Epic 5)
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── conftest.py              # Pytest configuration
│   └── test_models.py           # Model tests (THIS STORY)
├── run.py                       # CLI entry point (Epic 5)
├── pyproject.toml               # Project metadata
└── README.md                    # Documentation (Epic 7)
```

### Testing Requirements

**Test Coverage (NFR-009):**
- Target ≥88% code coverage across all modules
- This story's tests must cover 100% of GameEvent code

**Test Structure:**
```python
# tests/test_models.py

def test_game_event_creation_with_all_fields():
    """Verify GameEvent instantiation with all fields provided."""
    # Test implementation
    
def test_game_event_default_tags():
    """Verify tags defaults to empty list when not provided."""
    # Test implementation
    
def test_game_event_field_access():
    """Verify all fields are accessible after creation."""
    # Test implementation
    
def test_game_event_importance_values():
    """Verify all valid importance levels work correctly."""
    for importance in ["critical", "high", "medium", "low"]:
        # Test each importance level
```

**Running Tests:**
```bash
# Run tests with coverage
pytest tests/test_models.py --cov=highlight_selector --cov-report=term-missing

# Type checking
mypy highlight_selector/ --strict

# Formatting
black highlight_selector/
```

### Sample Data Reference

The shared sample data (`shared/sample_data.json`) contains GameEvent examples:

```json
{
  "events": [
    {
      "id": "event_001",
      "type": "dunk",
      "timestamp": "Q4 2:45",
      "quarter": 4,
      "player": "LeBron James",
      "team": "Lakers",
      "description": "Powerful dunk in transition",
      "importance": "critical",
      "tags": ["clutch", "game_winner", "fourth_quarter", "highlight_reel"]
    }
  ]
}
```

Use this structure to validate your model design.

### Dependencies

**Required Imports:**
```python
from dataclasses import dataclass, field
```

**NO external runtime dependencies allowed** - stdlib only per NFR-016.

### Performance Considerations

**Memory Efficiency:**
- Dataclasses are memory-efficient (no overhead vs. regular classes)
- No performance concerns for this simple model

**Future Compatibility:**
- Story 1.5 will add `to_dict()` and `from_dict()` methods for JSON serialization
- Keep model simple and serialization-friendly (no complex nested objects yet)

### References

- [Source: epics.md#Epic 1: Data Models and Core Types → Story 1.1]
- [Source: architecture.md#2.3 Data Serialization]
- [Source: architecture.md#3.3 Data Model Layer]
- [Source: prd.md#Product Scope → Data Models]
- [Source: shared/sample_data.json]

### Success Criteria

This story is complete when:
1. ✅ `highlight_selector/models.py` exists with GameEvent dataclass
2. ✅ All fields have correct type hints
3. ✅ Tags field defaults to empty list
4. ✅ Google-style docstring is comprehensive
5. ✅ All tests pass with 100% coverage of GameEvent
6. ✅ `mypy --strict` passes with no errors
7. ✅ `black` formatting applied
8. ✅ Code follows architecture patterns

## Dev Agent Record

### Agent Model Used

Claude Sonnet 4.5 (Dev Agent - Amelia)

### Implementation Plan

1. ✅ Create package structure (`highlight_selector/` directory with `__init__.py`)
2. ✅ Implement GameEvent dataclass in `models.py` with all fields and type hints
3. ✅ Write comprehensive unit tests in `tests/test_models.py`
4. ✅ Validate with mypy strict mode
5. ✅ Format with black
6. ✅ Verify 100% test coverage

### Debug Log References

No debugging required. Implementation followed TDD red-green-refactor cycle successfully.

### Completion Notes List

- ✅ Created package structure: `highlight_selector/` with `__init__.py` and `models.py`
- ✅ Implemented GameEvent as @dataclass with all 9 fields (8 required + 1 default)
- ✅ All fields have explicit type hints using Python 3.10+ syntax: `list[str]`
- ✅ Tags field defaults to empty list via `field(default_factory=list)`
- ✅ Comprehensive Google-style docstring with all attributes documented
- ✅ Wrote 6 unit tests covering all acceptance criteria
- ✅ All tests pass (6/6)
- ✅ 100% code coverage on models.py (12/12 statements)
- ✅ Mypy strict mode passes with no errors
- ✅ Black formatting applied successfully

### File List

**New Files:**
- `highlight_selector/__init__.py` - Package initialization (empty)
- `highlight_selector/models.py` - GameEvent dataclass with full type hints and docstring
- `tests/__init__.py` - Test package initialization (empty)
- `tests/test_models.py` - 6 unit tests for GameEvent (100% coverage)

**Modified Files:**
(None - this is the first story)

## Change Log

- 2026-02-17: Story created from Epic 1, Story 1.1 (SM Agent - YOLO mode)
- 2026-02-17: Implementation completed (Dev Agent - Amelia)
  - Created package structure: highlight_selector/ and tests/
  - Implemented GameEvent dataclass with full type hints
  - Wrote 6 unit tests achieving 100% coverage
  - Passed mypy strict mode validation
  - Applied black formatting
  - Status: ready-for-dev → review
