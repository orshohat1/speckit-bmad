---
description: "Task list for AI Highlight Selector implementation"
---

# Tasks: AI Highlight Selector

**Input**: Design documents from `specs/001-highlight-selector/`  
**Prerequisites**: plan.md ✅, spec.md ✅

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Package**: `highlight_selector/` (single Python package)
- **Tests**: `tests/` (test modules)
- **Config**: Repository root (`pyproject.toml`, `README.md`)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create package directory structure: `highlight_selector/` and `tests/`
- [X] T002 Create `pyproject.toml` with Python 3.10+ requirement and pytest dependency
- [X] T003 [P] Create empty `highlight_selector/__init__.py` with package exports placeholder
- [X] T004 [P] Create empty `tests/__init__.py`
- [X] T005 [P] Create `tests/conftest.py` with pytest fixtures for sample data from `shared/sample_data.json`
- [X] T006 [P] Setup `.gitignore` for Python (if not exists): `__pycache__/`, `*.pyc`, `.pytest_cache/`, `*.egg-info/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data models that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 [P] Create `highlight_selector/models.py` with `GameEvent` dataclass (9 fields: id, type, timestamp, quarter, player, team, description, importance, tags)
- [X] T008 [P] Add `UserPreference` dataclass to `highlight_selector/models.py` (2 optional fields: favorite_player, favorite_team)
- [X] T009 [P] Add `ScoreBreakdown` dataclass to `highlight_selector/models.py` (5 fields: base_score, player_boost, team_boost, context_boosts dict, total_score)
- [X] T010 [P] Add `Highlight` dataclass to `highlight_selector/models.py` (4 fields: event, rank, score, explanation)
- [X] T011 Add JSON serialization helpers to `highlight_selector/models.py`: `to_dict()` and `from_dict()` methods for all dataclasses
- [X] T012 [P] Create `tests/test_models.py` with tests for dataclass creation, field validation, and JSON serialization
- [X] T013 Run model tests to verify dataclass structure

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Basic Highlight Selection (Priority: P1) + User Story 5 - Edge Cases (Priority: P1) 🎯 MVP

**Goal**: Implement core scoring and selection logic that processes event lists and returns 5-8 ranked highlights. Includes robust edge case handling for production readiness.

**Independent Test**: Provide 15 game events with varying importance levels → verify 5-8 highlights returned, ranked by score, with all critical events included. Test with empty lists, null values, and malformed data.

### Implementation for US-1 & US-5

- [X] T014 [P] [US1] Create `highlight_selector/selector.py` with stub functions: `select_highlights()`, `score_event()`, `rank_and_filter()`, `generate_explanation()`
- [X] T015 [US1] Implement base scoring in `score_event()` function: importance lookup dict (critical=100, high=75, medium=50, low=25)
- [X] T016 [US1] Add context boost logic to `score_event()`: check tags for "clutch", "highlight_reel", "game_winner", "buzzer_beater" and quarter==4
- [X] T017 [US1] Implement `rank_and_filter()` function: force-include critical events, sort by score descending, select 5-8 events
- [X] T018 [US1] Add three-level tie-breaking to `rank_and_filter()`: quarter descending → importance descending → event_id ascending
- [X] T019 [P] [US5] Add edge case handling to `score_event()`: default unknown importance to "low" (FR-012)
- [X] T020 [P] [US5] Add edge case handling to `select_highlights()`: handle empty event list, return empty highlights (FR-010)
- [X] T021 [P] [US5] Add edge case handling to `select_highlights()`: handle null preferences, treat as no preference (FR-011)
- [X] T022 [US1] Implement `select_highlights()` orchestration: score all events → rank/filter → return scored events list
- [X] T023 [P] [US1] Create `tests/test_scoring.py` with tests for base importance scoring (4 test cases: critical, high, medium, low)
- [X] T024 [P] [US1] Add tests to `tests/test_scoring.py` for context boosts (5 test cases: clutch, highlight_reel, game_winner, buzzer_beater, fourth_quarter)
- [X] T025 [P] [US1] Create `tests/test_selection.py` with tests for ranking (score descending), critical inclusion (FR-006), and count constraints (5-8 highlights per FR-005)
- [X] T026 [P] [US1] Add tie-breaking tests to `tests/test_selection.py` (3 test cases: by quarter, by importance, by event_id)
- [X] T027 [P] [US5] Create `tests/test_edge_cases.py` with tests for empty event list (FR-010)
- [X] T028 [P] [US5] Add tests to `tests/test_edge_cases.py` for null preferences (FR-011, 2 cases: null player, null team)
- [X] T029 [P] [US5] Add tests to `tests/test_edge_cases.py` for unknown importance default (FR-012)
- [X] T030 [P] [US5] Add tests to `tests/test_edge_cases.py` for fewer than 5 events total
- [X] T031 [US1] Add determinism test to `tests/test_selection.py`: verify identical inputs produce identical outputs (FR-009, SC-004)
- [X] T032 [US1] Run basic selection tests and edge case tests to verify MVP functionality

**Checkpoint**: At this point, User Story 1 (Basic Selection) and User Story 5 (Edge Cases) should be fully functional as MVP. System returns 5-8 highlights with scoring and robust error handling.

---

## Phase 4: User Story 4 - Highlight Explanations (Priority: P2)

**Goal**: Generate human-readable 1-2 sentence explanations for each highlight that reference scoring factors in non-technical language.

**Independent Test**: Run MVP system and verify every highlight includes an explanation field with 1-2 sentences that reference importance level, contextual factors, and is fan-friendly (no jargon).

### Implementation for US-4

- [X] T033 [US4] Implement `generate_explanation()` function in `highlight_selector/selector.py`: build explanation from importance context
- [X] T034 [US4] Add importance-based templates to `generate_explanation()`: "This critical {event_type}...", "A high-impact {event_type}..."
- [X] T035 [US4] Add contextual templates to `generate_explanation()`: game_winner → "sealed the victory", clutch+Q4 → "in a clutch fourth-quarter moment"
- [X] T036 [US4] Add explanation length constraint: concatenate parts and limit to 1-2 sentences
- [X] T037 [US4] Update `select_highlights()` to call `generate_explanation()` for each selected event and create `Highlight` objects
- [X] T038 [P] [US4] Create `tests/test_explanations.py` with test for explanation presence (100% of highlights have non-empty explanation per SC-002)
- [X] T039 [P] [US4] Add test to `tests/test_explanations.py` for explanation length (1-2 sentences per SC-007)
- [X] T040 [P] [US4] Add test to `tests/test_explanations.py` for scoring factor references (importance, context)
- [X] T041 [P] [US4] Add test to `tests/test_explanations.py` for non-technical language (no jargon per SC-007)
- [X] T042 [US4] Run explanation tests to verify all highlights include quality explanations

**Checkpoint**: At this point, User Stories 1, 4, and 5 work together. System returns highlights with human-readable explanations.

---

## Phase 5: User Story 2 - Player-Based Personalization (Priority: P2)

**Goal**: Boost events featuring the user's favorite player so at least 50% of highlights feature that player (when sufficient events exist).

**Independent Test**: Provide 15 events where 8 involve a favorite player → verify at least 50% of returned highlights (4+ out of 7) feature that player, while critical non-player events still included.

### Implementation for US-2

- [X] T043 [US2] Add player preference boost to `score_event()` in `highlight_selector/selector.py`: +30 points if `event.player == prefs.favorite_player`
- [X] T044 [US2] Update explanation templates in `generate_explanation()`: add player preference context ("Selected for your favorite player {player}...")
- [X] T045 [P] [US2] Create `tests/test_scoring.py` test for player boost application (+30 points when player matches)
- [X] T046 [P] [US2] Add test to `tests/test_selection.py` for 50% player involvement (FR-014, SC-003)
- [X] T047 [P] [US2] Add test to `tests/test_selection.py` for critical non-player events still included (game narrative maintained)
- [X] T048 [P] [US2] Add test to `tests/test_edge_cases.py` for no events with favorite player (fallback to basic selection)
- [X] T049 [P] [US2] Add test to `tests/test_explanations.py` for player preference mention in explanation
- [X] T050 [US2] Run player personalization tests to verify boost and selection logic

**Checkpoint**: At this point, User Stories 1, 2, 4, and 5 work together. System personalizes highlights based on favorite player.

---

## Phase 6: User Story 3 - Team-Based Personalization (Priority: P3)

**Goal**: Boost events from the user's favorite team while maintaining game narrative by including significant opponent plays.

**Independent Test**: Provide events split between two teams with favorite_team set → verify highlights weighted toward favorite team but include critical opponent plays for context.

### Implementation for US-3

- [X] T051 [US3] Add team preference boost to `score_event()` in `highlight_selector/selector.py`: +15 points if `event.team == prefs.favorite_team`
- [X] T052 [US3] Update explanation templates in `generate_explanation()`: add team preference context ("This {event_type} by your favorite team, the {team}...")
- [X] T053 [P] [US3] Add test to `tests/test_scoring.py` for team boost application (+15 points when team matches)
- [X] T054 [P] [US3] Add test to `tests/test_selection.py` for team weighting (more highlights from favorite team)
- [X] T055 [P] [US3] Add test to `tests/test_selection.py` for opponent play inclusion (FR-015, critical opponent moments included for narrative)
- [X] T056 [P] [US3] Add test to `tests/test_edge_cases.py` for both player and team preferences set (player takes precedence)
- [X] T057 [P] [US3] Add test to `tests/test_explanations.py` for team preference mention in explanation
- [X] T058 [US3] Run team personalization tests to verify boost and narrative balance

**Checkpoint**: All user stories (1, 2, 3, 4, 5) now work independently and together. Complete personalization feature set.

---

## Phase 7: CLI Interface & Integration

**Goal**: Provide command-line interface for JSON input/output (stdin → stdout) with end-to-end integration tests.

**Independent Test**: Run CLI with JSON input from `shared/sample_data.json` → verify JSON output with 5-8 highlights, explanations, metadata.

### Implementation for CLI

- [X] T059 [P] Create `highlight_selector/cli.py` with JSON input parsing from stdin
- [X] T060 Add CLI JSON output formatting: highlights list + metadata (total_events, selected_count, preferences)
- [X] T061 Add CLI error handling: graceful error messages for invalid JSON, missing fields
- [X] T062 Update `highlight_selector/__init__.py` with proper package exports: `select_highlights`, `GameEvent`, `UserPreference`, `Highlight`
- [X] T063 [P] Create `tests/test_integration.py` with end-to-end test: JSON input → `select_highlights()` → JSON output
- [X] T064 [P] Add integration test to `tests/test_integration.py` for all 5 user stories working together
- [X] T065 [P] Add integration test to `tests/test_integration.py` using `shared/sample_data.json` as fixture
- [X] T066 Run integration tests to verify end-to-end flow

**Checkpoint**: Complete system with CLI interface. All user stories integrated and testable via CLI.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Performance validation, documentation, and code quality

### Performance Validation

- [X] T067 [P] Add performance benchmark to `tests/test_integration.py`: verify <100ms for 15 events (SC-001)
- [X] T068 [P] Add performance benchmark to `tests/test_integration.py`: verify <1s for 1000 events (SC-005)
- [X] T069 Run performance benchmarks and optimize if needed

### Code Quality

- [X] T070 [P] Run `black` formatter on all Python files in `highlight_selector/` and `tests/`
- [X] T071 [P] Run `mypy --strict` type checker on `highlight_selector/` package
- [X] T072 [P] Run `pytest --cov=highlight_selector` to measure test coverage (target: 100% for core logic)
- [X] T073 Fix any type hints, formatting, or coverage gaps

### Documentation

- [X] T074 [P] Create `specs/001-highlight-selector/data-model.md` with detailed dataclass schemas, field descriptions, and JSON examples
- [X] T075 [P] Create `specs/001-highlight-selector/quickstart.md` with usage examples (CLI + Python API), installation instructions, and testing guide
- [X] T076 [P] Create `specs/001-highlight-selector/contracts/` directory
- [X] T077 Create `specs/001-highlight-selector/contracts/input-output.json` with sample JSON input/output schemas
- [X] T078 Update root `README.md` with project overview, setup instructions, usage examples, and constitution compliance summary

### Final Validation

- [X] T079 Run complete test suite: `pytest tests/ -v` - verify all tests pass
- [X] T080 Validate all 15 functional requirements (FR-001 to FR-015) have corresponding test coverage
- [X] T081 Validate all 8 success criteria (SC-001 to SC-008) are measured and passed
- [X] T082 Run quickstart.md examples manually to verify documentation accuracy

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - Phase 3: US-1 + US-5 (P1 stories) - MVP, can start after Foundational
  - Phase 4: US-4 (P2) - Can start after Phase 3 or in parallel if staffed
  - Phase 5: US-2 (P2) - Can start after Phase 3 or in parallel if staffed
  - Phase 6: US-3 (P3) - Can start after Phase 3 or in parallel if staffed
- **CLI (Phase 7)**: Can start after Phase 3 (MVP) is complete
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 + 5 (P1)**: Can start after Foundational - No dependencies on other stories (MVP)
- **User Story 4 (P2)**: Needs US-1 scoring/selection logic - Can integrate immediately after Phase 3
- **User Story 2 (P2)**: Needs US-1 scoring logic - Can extend `score_event()` independently
- **User Story 3 (P3)**: Needs US-1 scoring logic - Can extend `score_event()` independently

### Within Each User Story

- Tests can be written in parallel with implementation (TDD approach)
- Core functions before orchestration
- Unit tests before integration tests

### Parallel Opportunities

Within Phase 2 (Foundational):
- T007, T008, T009, T010 (all dataclass creation) - parallel
- T012 (test creation) - parallel with T007-T010

Within Phase 3 (MVP):
- T014 (create stubs) first, then:
- T015-T018 (scoring & selection logic) - can be done in sequence but different functions
- T019, T020, T021 (edge cases) - parallel with each other
- T023, T024, T025, T026, T027, T028, T029, T030 (all tests) - parallel test creation

Within Phase 4 (Explanations):
- T038-T041 (all tests) - parallel

Within Phase 5 (Player):
- T045-T049 (all tests) - parallel

Within Phase 6 (Team):
- T053-T057 (all tests) - parallel

Within Phase 7 (CLI):
- T059, T062 (CLI creation) - can be parallel
- T063, T064, T065 (integration tests) - parallel

Within Phase 8 (Polish):
- T067, T068 (benchmarks) - parallel
- T070, T071, T072 (code quality) - parallel
- T074, T075, T076, T077, T078 (documentation) - all parallel

---

## Implementation Strategy

### MVP First (Phase 3 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T013) ⚠️ CRITICAL GATE
3. Complete Phase 3: User Story 1 + 5 (T014-T032)
4. **STOP and VALIDATE**: Run tests, verify 5-8 highlights with edge case handling
5. Deploy/demo MVP if ready

### Incremental Delivery

1. Setup + Foundational (T001-T013) → Foundation ready
2. Add US-1 + US-5 (T014-T032) → Test independently → MVP! 🎯
3. Add US-4 (T033-T042) → Explanations working → Demo
4. Add US-2 (T043-T050) → Player personalization → Demo
5. Add US-3 (T051-T058) → Full personalization → Demo
6. Add CLI (T059-T066) → End-to-end integration → Demo
7. Polish (T067-T082) → Production ready → Ship! 🚀

Each phase adds measurable value without breaking previous functionality.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T013)
2. Once Foundational is done:
   - **Developer A**: Phase 3 - US-1 + US-5 (T014-T032) - MVP critical path
   - **Developer B**: Phase 4 - US-4 (T033-T042) - Can start tests in parallel
   - **Developer C**: Phase 5 - US-2 (T043-T050) - Can start tests in parallel
3. After initial integration:
   - **Developer A**: Phase 7 - CLI (T059-T066)
   - **Developer B**: Phase 6 - US-3 (T051-T058)
   - **Developer C**: Phase 8 - Documentation (T074-T078)
4. Team completes Phase 8 - Performance & Code Quality (T067-T073, T079-T082)

---

## Summary

**Total Tasks**: 82  
**MVP Tasks (Phase 1-3)**: 32 (T001-T032)  
**Full Feature Tasks (Phase 1-6)**: 58 (T001-T058)  
**Complete Implementation**: 82 (all phases)

**User Story Breakdown**:
- US-1 (Basic Selection): 19 tasks (T014-T032 includes implementation + tests)
- US-5 (Edge Cases): Integrated with US-1 (T019-T021, T027-T030)
- US-4 (Explanations): 10 tasks (T033-T042)
- US-2 (Player Personalization): 8 tasks (T043-T050)
- US-3 (Team Personalization): 8 tasks (T051-T058)
- CLI & Integration: 8 tasks (T059-T066)
- Polish: 16 tasks (T067-T082)

**Estimated Timeline**: 
- MVP (Phases 1-3): 1-2 days
- Full Feature (Phases 1-6): 2-3 days
- Production Ready (All phases): 3-4 days

(Assuming 4-6 hours of focused work per day, single developer)

---

## Notes

- ✅ All tasks follow checklist format with task ID, [P] for parallel, [Story] for user story mapping
- ✅ All tasks include specific file paths
- ✅ Tasks organized by user story for independent development and testing
- ✅ MVP clearly identified (Phase 3 - US-1 + US-5)
- ✅ Incremental delivery strategy enables demo after each phase
- ✅ Parallel opportunities identified for team collaboration
- ✅ Constitution compliance maintained throughout (testability, simplicity, explainability)
