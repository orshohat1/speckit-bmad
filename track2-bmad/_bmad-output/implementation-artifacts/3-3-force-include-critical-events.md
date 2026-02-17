# Story 3.3: Force-Include Critical Events

Status: review

## Story

As a developer,
I want selection logic that always includes critical importance events,
So that game-defining moments are never omitted regardless of personalization.

## Acceptance Criteria

**Given** I have a list of scored events including some with "critical" importance
**When** I call select_highlights(events, preferences)
**Then** all critical importance events are included in the output

**And** critical events are included even if the total exceeds the normal 5-8 range

**And** critical events maintain their score-based ranking position

**And** this rule is enforced before the 5-8 count logic

**And** the function is implemented in selector.py

**And** the function includes type hints and a docstring

**Requirements Fulfilled:** FR-009, FR-013, NFR-014

## Tasks / Subtasks

- [ ] Task 1: Implement core functionality (AC: all)
  - [ ] Subtask 1.1: Create necessary files/modules
  - [ ] Subtask 1.2: Implement main logic
  - [ ] Subtask 1.3: Add type hints and docstrings

- [ ] Task 2: Write comprehensive tests (AC: all)
  - [ ] Subtask 2.1: Write unit tests
  - [ ] Subtask 2.2: Write integration tests (if needed)
  - [ ] Subtask 2.3: Validate test coverage

- [ ] Task 3: Code quality validation (AC: all)
  - [ ] Subtask 3.1: Run mypy strict mode
  - [ ] Subtask 3.2: Run black formatter
  - [ ] Subtask 3.3: Verify all acceptance criteria met

## Dev Notes

### Epic Context

This story is part of **Epic 3: Highlight Selection and Ranking**.

### Architecture Requirements

**Technology Stack:**
- Python 3.10+ (required for modern type hints)
- Standard library ONLY (NFR-016) - no external runtime dependencies
- Development dependencies: pytest, black, mypy (dev-time only)

**Code Quality Standards:**
1. Type hints on all functions (NFR-010, NFR-013)
2. Google-style docstrings (NFR-011)
3. Black formatting (NFR-012)
4. Pure functions for business logic (NFR-014)
5. ≥88% test coverage (NFR-009)

### Project Structure

```
track2-bmad/
├── highlight_selector/          # Main package
│   ├── __init__.py
│   ├── models.py                # Data models (Epic 1)
│   ├── selector.py              # Core logic (Epics 2-4)
│   └── cli.py                   # CLI interface (Epic 5)
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── conftest.py
│   └── test_*.py
├── run.py                       # CLI entry point
└── README.md
```

### References

- [Source: epics.md#Epic 3 → Story 3.3]
- [Source: architecture.md]
- [Source: prd.md]

## Dev Agent Record

### Implementation Plan

1. Analyze acceptance criteria and requirements
2. Implement functionality following architecture patterns
3. Write comprehensive tests
4. Validate quality standards (mypy, black, coverage)

### Debug Log References

(To be filled during implementation)

### Completion Notes List

(To be filled when tasks are completed)

### File List

**New Files:**
(To be filled during implementation)

**Modified Files:**
(To be filled during implementation)

## Change Log

- 2026-02-17: Story created from Epic 3, Story 3.3 (SM Agent - Batch Generation)
