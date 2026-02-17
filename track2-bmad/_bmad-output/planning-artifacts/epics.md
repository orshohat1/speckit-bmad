---
stepsCompleted: ["step-01-init", "step-02-epic-structure", "step-03-all-stories-complete"]
workflowStatus: "complete"
completionDate: "2026-02-17"
inputDocuments:
  - /Users/or.shohat/Documents/Git/WSC/speckit-bmad/track2-bmad/_bmad-output/planning-artifacts/prd.md
  - /Users/or.shohat/Documents/Git/WSC/speckit-bmad/track2-bmad/_bmad-output/planning-artifacts/architecture.md
totalEpics: 7
totalStories: 41
---

# AI Highlight Selector (Track2 - BMAD) - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for AI Highlight Selector (Track2 - BMAD), decomposing the requirements from the PRD and Architecture into implementable stories.

## Requirements Inventory

### Functional Requirements

- **FR-001**: System can accept a list of game events as input, where each event contains event type, timestamp, quarter, player, team, importance level, and optional tags
- **FR-002**: System can accept optional user preferences specifying favorite player and/or favorite team
- **FR-003**: System can score each event based on its importance level (critical=100, high=75, medium=50, low=25)
- **FR-004**: System can apply scoring boosts to events involving the user's favorite player (+30 points) when preference is specified
- **FR-005**: System can apply scoring boosts to events involving the user's favorite team (+15 points) when preference is specified
- **FR-006**: System can apply context-based scoring boosts for tagged events (clutch +20, game_winner +25, buzzer_beater +15, highlight_reel +15, fourth_quarter +10)
- **FR-007**: System can calculate final scores for all events combining base score, personalization boosts, and context boosts
- **FR-008**: System can select 5-8 highlights from scored events based on final scores
- **FR-009**: System can force-include all critical importance events in the output regardless of personalization
- **FR-010**: System can rank highlights by final calculated score in descending order
- **FR-011**: System can apply deterministic tie-breaking when events have identical scores (quarter descending → importance descending → event ID ascending)
- **FR-012**: System can ensure at least 50% of returned highlights feature the favorite player when sufficient qualifying events exist (≥3 events)
- **FR-013**: System can include critical opponent plays for game narrative even when team preference is set
- **FR-014**: System can generate human-readable explanations (1-2 sentences) for each selected highlight
- **FR-015**: System can reference specific scoring factors in explanations (importance level, player preference, team preference, context tags)
- **FR-016**: System can produce explanations in natural, fan-friendly language without technical jargon
- **FR-017**: System can handle empty event lists gracefully by returning empty highlight list
- **FR-018**: System can treat null or missing user preferences as "no preference" and proceed with basic selection
- **FR-019**: System can default unknown importance levels to "low" importance
- **FR-020**: System can handle events with missing optional fields by using sensible defaults
- **FR-021**: System can validate player/team names against available events and provide helpful error messages listing available options
- **FR-022**: Users can specify favorite player via command-line flag (`--player "Name"`)
- **FR-023**: Users can specify favorite team via command-line flag (`--team "Name"`)
- **FR-024**: Users can filter output to show only favorite player/team highlights via `--only` flag
- **FR-025**: Users can run without preferences to get objective importance-based ranking
- **FR-026**: Users can see formatted output with rank, score, player, team, timing, description, and explanation for each highlight
- **FR-027**: Users can receive helpful validation errors when specified player/team is not found in game data
- **FR-028**: Developers can import and call `select_highlights()` function programmatically with events and preferences
- **FR-029**: Developers can access typed data models (GameEvent, UserPreference, ScoreBreakdown, Highlight) for integration
- **FR-030**: Developers can serialize/deserialize models to/from JSON for data interchange
- **FR-031**: System can produce identical output when given identical inputs (fully deterministic)
- **FR-032**: System can ensure all behavior is reproducible for testing and validation
- **FR-033**: System can execute without any random or non-deterministic elements

### Non-Functional Requirements

- **NFR-001**: System SHALL process a list of 15 game events and return highlights in under 100 milliseconds on standard hardware
- **NFR-002**: System SHALL handle up to 1000 game events and return highlights in under 1 second on standard hardware
- **NFR-003**: Scoring algorithm SHALL use O(n log n) time complexity or better (dominated by sorting operation)
- **NFR-004**: System SHALL maintain consistent performance regardless of specific event content or preference configurations
- **NFR-005**: System SHALL produce identical output when given identical inputs (100% deterministic behavior)
- **NFR-006**: System SHALL handle all edge cases (empty lists, null values, malformed data) without crashes or undefined behavior
- **NFR-007**: System SHALL include non-empty explanations for 100% of returned highlights
- **NFR-008**: System SHALL generate explanations of 1-2 sentences without technical jargon or implementation details
- **NFR-009**: Test suite SHALL achieve minimum 88% code coverage across all modules
- **NFR-010**: All public API functions SHALL include type hints for static type checking
- **NFR-011**: All public API functions SHALL include docstrings following Google style format
- **NFR-012**: Code SHALL pass black formatter validation (PEP 8 compliance)
- **NFR-013**: Code SHALL pass mypy strict mode type checking without errors
- **NFR-014**: Core business logic (scoring, selection, explanation) SHALL be implemented as pure functions for testability
- **NFR-015**: System SHALL maintain strict separation of concerns (models, logic, interface) across modules
- **NFR-016**: System SHALL have no external runtime dependencies (Python stdlib only)
- **NFR-017**: Development dependencies SHALL be clearly documented and justified in project documentation
- **NFR-018**: Code SHALL follow single responsibility principle with functions focused on one clear purpose
- **NFR-019**: CLI error messages SHALL be helpful and actionable (e.g., listing available options when validation fails)
- **NFR-020**: CLI output SHALL be formatted for readability with clear visual hierarchy
- **NFR-021**: API SHALL be simple enough for developers to integrate with minimal documentation reading
- **NFR-022**: Documentation SHALL include working code examples for common use cases
- **NFR-023**: System SHALL run on Python 3.10+ without modification
- **NFR-024**: System SHALL be cross-platform compatible (Linux, macOS, Windows)
- **NFR-025**: System SHALL not depend on operating system-specific features or paths

### Additional Requirements

- **Track2 Success**: Successfully complete the same feature as Track1 using BMAD methodology with clear traceability from requirements to implementation
- **Test Coverage**: Match or exceed Track1's 88% test coverage
- **Documentation**: Complete README, quickstart guide, and data model documentation
- **Sample Data**: Functional demo with provided sample_data.json

## FR Coverage Map

- **Epic 1 (Data Models and Core Types)**: FR-001, FR-002, FR-029, FR-030, NFR-010, NFR-011, NFR-023, NFR-024
- **Epic 2 (Event Scoring Engine)**: FR-003, FR-004, FR-005, FR-006, FR-007, NFR-003, NFR-014, NFR-018
- **Epic 3 (Highlight Selection and Ranking)**: FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-031, FR-032, FR-033, NFR-005, NFR-014
- **Epic 4 (Explanation Generation System)**: FR-014, FR-015, FR-016, NFR-007, NFR-008, NFR-014, NFR-018
- **Epic 5 (CLI Interface and User Experience)**: FR-022, FR-023, FR-024, FR-025, FR-026, FR-027, NFR-019, NFR-020, NFR-021
- **Epic 6 (Edge Case Handling and Validation)**: FR-017, FR-018, FR-019, FR-020, FR-021, NFR-006
- **Epic 7 (Testing, Performance, and Quality Assurance)**: FR-028, NFR-001, NFR-002, NFR-004, NFR-009, NFR-012, NFR-013, NFR-015, NFR-016, NFR-017, NFR-022, NFR-025

## Epic List

1. **Epic 1: Data Models and Core Types** - Create foundational data structures with type safety and JSON serialization support
2. **Epic 2: Event Scoring Engine** - Implement multi-factor scoring algorithm with importance, personalization, and context boosts
3. **Epic 3: Highlight Selection and Ranking** - Build selection logic with ranking, tie-breaking, and force-include rules
4. **Epic 4: Explanation Generation System** - Generate natural language explanations for highlight selections
5. **Epic 5: CLI Interface and User Experience** - Create command-line interface with preference flags and formatted output
6. **Epic 6: Edge Case Handling and Validation** - Implement robust error handling and input validation
7. **Epic 7: Testing, Performance, and Quality Assurance** - Build comprehensive test suite and ensure code quality standards

---

## Epic 1: Data Models and Core Types

Create the foundational data structures that represent game events, user preferences, scoring breakdowns, and highlights. These models form the contract between all system components and enable type-safe operations throughout the codebase.

### Story 1.1: GameEvent Data Model

As a developer,
I want a strongly-typed GameEvent model that represents a single game event,
So that I can reliably work with game event data throughout the system.

**Acceptance Criteria:**

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

---

### Story 1.2: UserPreference Data Model

As a developer,
I want a UserPreference model that captures user personalization settings,
So that I can apply scoring boosts based on user's favorite player and/or team.

**Acceptance Criteria:**

**Given** I am creating a new UserPreference instance
**When** I provide optional favorite_player and/or favorite_team
**Then** the UserPreference is created successfully

**And** both fields are optional (can be None)

**And** the model includes type hints using Optional[str] for both fields

**And** the model handles the case where neither preference is specified (both None)

**And** the model handles the case where only one preference is specified

**And** the model is defined as a dataclass in models.py module

**And** the model includes a docstring describing its purpose and use cases

**Requirements Fulfilled:** FR-002, NFR-010, NFR-011

---

### Story 1.3: ScoreBreakdown Data Model

As a developer,
I want a ScoreBreakdown model that transparently shows how a score was calculated,
So that I can generate accurate explanations and debug scoring logic.

**Acceptance Criteria:**

**Given** I am creating a new ScoreBreakdown instance
**When** I provide base_score, player_boost, team_boost, context_boosts, and total_score
**Then** the ScoreBreakdown is created successfully with all components documented

**And** all numeric fields are typed as int or float appropriately

**And** context_boosts is a dictionary mapping tag names to boost values

**And** total_score equals base_score + player_boost + team_boost + sum(context_boosts.values())

**And** the model is defined as a dataclass in models.py module

**And** the model includes a docstring explaining each score component

**Requirements Fulfilled:** FR-007, NFR-010, NFR-011

---

### Story 1.4: Highlight Output Model

As a developer,
I want a Highlight model that packages selected events with their metadata,
So that I can return structured output with rank, score, and explanation.

**Acceptance Criteria:**

**Given** I am creating a new Highlight instance
**When** I provide a GameEvent, rank, score, and explanation
**Then** the Highlight is created successfully with all fields accessible

**And** the model contains a reference to the full GameEvent object

**And** rank is an integer representing the highlight's position (1-8)

**And** score is a numeric value (int or float) showing the final calculated score

**And** explanation is a non-empty string (1-2 sentences)

**And** the model is defined as a dataclass in models.py module

**And** the model includes a docstring describing its structure and purpose

**Requirements Fulfilled:** FR-014, FR-029, NFR-010, NFR-011

---

### Story 1.5: JSON Serialization Support

As a developer,
I want all models to support JSON serialization and deserialization,
So that I can read input from JSON files and output results in JSON format.

**Acceptance Criteria:**

**Given** I have instances of GameEvent, UserPreference, ScoreBreakdown, and Highlight
**When** I call to_dict() on any model instance
**Then** I receive a dictionary representation suitable for JSON serialization

**And** nested objects (like GameEvent within Highlight) are also converted to dictionaries

**And** None values are preserved (not converted to "null" strings)

**Given** I have a dictionary representation of a model
**When** I call the model's from_dict() class method
**Then** I receive a properly typed instance of the model

**And** nested objects are properly reconstructed (e.g., Highlight.event becomes a GameEvent)

**And** missing optional fields default to None appropriately

**And** both methods are tested with the sample_data.json structure

**And** serialization/deserialization round-trip preserves all data (obj == Model.from_dict(obj.to_dict()))

**Requirements Fulfilled:** FR-030, NFR-023, NFR-024

---

## Epic 2: Event Scoring Engine

Implement the multi-factor scoring algorithm that calculates numeric scores for game events based on importance levels, personalization preferences, and contextual tags. This pure function-based engine forms the core selection logic.

### Story 2.1: Base Importance Scoring

As a developer,
I want a function that calculates base scores from event importance levels,
So that critical plays are scored higher than routine plays.

**Acceptance Criteria:**

**Given** I have a GameEvent with an importance level
**When** I call calculate_base_score(event)
**Then** I receive a numeric score based on the importance mapping

**And** "critical" importance returns 100 points

**And** "high" importance returns 75 points

**And** "medium" importance returns 50 points

**And** "low" importance returns 25 points

**And** unknown or missing importance defaults to "low" (25 points)

**And** the function is implemented as a pure function in selector.py

**And** the function includes type hints and a docstring

**And** the function is deterministic (same input always returns same output)

**Requirements Fulfilled:** FR-003, FR-019, NFR-014, NFR-018

---

### Story 2.2: Player Preference Boost

As a developer,
I want a function that adds score boosts for events featuring the user's favorite player,
So that highlights can be personalized to user preferences.

**Acceptance Criteria:**

**Given** I have a GameEvent and a UserPreference with a favorite_player
**When** I call calculate_player_boost(event, preference)
**Then** I receive +30 points if the event's player matches the favorite_player

**And** I receive 0 points if the event's player does not match

**And** I receive 0 points if no favorite_player is specified (None)

**And** player name matching is case-sensitive and exact

**And** the function is implemented as a pure function in selector.py

**And** the function includes type hints and a docstring

**And** the function handles None values gracefully without errors

**Requirements Fulfilled:** FR-004, NFR-014, NFR-018

---

### Story 2.3: Team Preference Boost

As a developer,
I want a function that adds score boosts for events involving the user's favorite team,
So that highlights can prioritize a specific team's plays.

**Acceptance Criteria:**

**Given** I have a GameEvent and a UserPreference with a favorite_team
**When** I call calculate_team_boost(event, preference)
**Then** I receive +15 points if the event's team matches the favorite_team

**And** I receive 0 points if the event's team does not match

**And** I receive 0 points if no favorite_team is specified (None)

**And** team name matching is case-sensitive and exact

**And** the function is implemented as a pure function in selector.py

**And** the function includes type hints and a docstring

**And** the function handles None values gracefully without errors

**Requirements Fulfilled:** FR-005, NFR-014, NFR-018

---

### Story 2.4: Context Tag Boosts

As a developer,
I want a function that calculates score boosts based on event context tags,
So that clutch moments and highlight-reel plays are prioritized.

**Acceptance Criteria:**

**Given** I have a GameEvent with context tags
**When** I call calculate_context_boosts(event)
**Then** I receive a dictionary mapping each tag to its boost value

**And** "clutch" tag adds +20 points

**And** "game_winner" tag adds +25 points

**And** "buzzer_beater" tag adds +15 points

**And** "highlight_reel" tag adds +15 points

**And** "fourth_quarter" tag adds +10 points

**And** unknown tags are ignored (no boost applied)

**And** events with no tags return an empty dictionary

**And** multiple tags accumulate (e.g., clutch + fourth_quarter = 30 total)

**And** the function is implemented as a pure function in selector.py

**And** the function includes type hints and a docstring

**Requirements Fulfilled:** FR-006, NFR-014, NFR-018

---

### Story 2.5: Total Score Calculation with Breakdown

As a developer,
I want a function that calculates the final score and returns a ScoreBreakdown,
So that I can understand how each scoring component contributed to the total.

**Acceptance Criteria:**

**Given** I have a GameEvent and optional UserPreference
**When** I call calculate_score(event, preference)
**Then** I receive a ScoreBreakdown with all components populated

**And** base_score is calculated from importance level

**And** player_boost is calculated based on favorite player match

**And** team_boost is calculated based on favorite team match

**And** context_boosts dictionary contains all applicable tag boosts

**And** total_score equals base_score + player_boost + team_boost + sum(context_boosts.values())

**And** the function correctly handles None preference (all boosts = 0)

**And** the function is implemented as a pure function in selector.py

**And** the function includes type hints and a docstring

**And** the function achieves O(n) complexity per event (where n = number of tags)

**Requirements Fulfilled:** FR-007, NFR-003, NFR-014, NFR-018

---

## Epic 3: Highlight Selection and Ranking

Build the selection logic that chooses the top 5-8 highlights from scored events, applies deterministic tie-breaking, and enforces business rules like force-including critical events and maintaining narrative balance.

### Story 3.1: Sort Events by Score

As a developer,
I want a function that sorts scored events in descending order,
So that the highest-scoring events are prioritized for selection.

**Acceptance Criteria:**

**Given** I have a list of GameEvents with calculated ScoreBreakdown objects
**When** I call sort_events_by_score(events, scores)
**Then** I receive events sorted by total_score in descending order

**And** the function uses stable sorting to preserve input order for equal scores

**And** the function is implemented as a pure function in selector.py

**And** the function includes type hints and a docstring

**And** the function achieves O(n log n) complexity through standard sorting

**And** the sorting is deterministic (same input always produces same output order)

**Requirements Fulfilled:** FR-010, FR-031, FR-032, FR-033, NFR-003, NFR-005

---

### Story 3.2: Deterministic Tie-Breaking

As a developer,
I want a tie-breaking function that resolves score ties consistently,
So that selection results are reproducible and deterministic.

**Acceptance Criteria:**

**Given** I have multiple events with identical total scores
**When** I apply the tie-breaking logic
**Then** events are ordered by quarter (descending: 4th > 3rd > 2nd > 1st)

**And** if quarters are equal, events are ordered by importance (descending: critical > high > medium > low)

**And** if both quarter and importance are equal, events are ordered by event ID (ascending: lexicographic)

**And** the tie-breaking is implemented as a comparison key function

**And** the function is deterministic and reproducible

**And** the function includes type hints and a docstring

**And** the function handles all edge cases (missing quarters, missing IDs)

**Requirements Fulfilled:** FR-011, FR-031, FR-032, FR-033, NFR-005

---

### Story 3.3: Force-Include Critical Events

As a developer,
I want selection logic that always includes critical importance events,
So that game-defining moments are never omitted regardless of personalization.

**Acceptance Criteria:**

**Given** I have a list of scored events including some with "critical" importance
**When** I call select_highlights(events, preferences)
**Then** all critical importance events are included in the output

**And** critical events are included even if the total exceeds the normal 5-8 range

**And** critical events maintain their score-based ranking position

**And** this rule is enforced before the 5-8 count logic

**And** the function is implemented in selector.py

**And** the function includes type hints and a docstring

**Requirements Fulfilled:** FR-009, FR-013, NFR-014

---

### Story 3.4: Select 5-8 Highlights

As a developer,
I want logic that selects between 5-8 top-scoring highlights,
So that users receive a curated list that's neither too short nor too long.

**Acceptance Criteria:**

**Given** I have a list of scored and sorted events
**When** I call select_highlights(events, preferences)
**Then** I receive between 5-8 highlights from the list

**And** if there are fewer than 5 total events, all events are returned

**And** if there are 5-8 events, all are returned

**And** if there are more than 8 events, the top 8 (by score) are returned

**And** critical events are always included (may push count above 8)

**And** the selection is deterministic

**And** the function is implemented in selector.py

**And** the function includes type hints and a docstring

**Requirements Fulfilled:** FR-008, FR-009, NFR-005

---

### Story 3.5: Favorite Player Representation Rule

As a developer,
I want logic that ensures at least 50% representation for the favorite player,
So that personalized selections adequately feature the user's preferred player.

**Acceptance Criteria:**

**Given** I have a UserPreference with a favorite_player
**When** I have at least 3 events featuring that player in the input
**Then** at least 50% of the returned highlights feature the favorite player

**And** this rule is applied after force-including critical events

**And** the rule only applies when sufficient qualifying events exist (≥3)

**And** the selection still respects score-based ranking within the constraint

**And** the function handles edge cases (no favorite player, insufficient events)

**And** the logic is implemented in selector.py as part of select_highlights()

**And** the function includes type hints and a docstring

**Requirements Fulfilled:** FR-012, NFR-014

---

### Story 3.6: Main Select Highlights Function

As a developer,
I want a main select_highlights() function that orchestrates all selection rules,
So that I have a single entry point that applies scoring, selection, and ranking.

**Acceptance Criteria:**

**Given** I provide a list of GameEvents and optional UserPreference
**When** I call select_highlights(events, preferences, max_count=8, min_count=5)
**Then** I receive a list of Highlight objects ranked and ready for output

**And** the function applies scoring to all events using calculate_score()

**And** the function sorts events with deterministic tie-breaking

**And** the function force-includes all critical events

**And** the function selects 5-8 highlights (or all if fewer than 5)

**And** the function applies the 50% favorite player rule when applicable

**And** the function assigns rank numbers (1 through N) to selected highlights

**And** the function is the main public API in selector.py

**And** the function is deterministic (same inputs = same outputs)

**And** the function includes comprehensive docstring with examples

**Requirements Fulfilled:** FR-028, FR-031, FR-032, FR-033, NFR-005, NFR-014, NFR-021

---

## Epic 4: Explanation Generation System

Generate natural language explanations for each selected highlight that clearly communicate why it was chosen, referencing scoring factors in fan-friendly language without technical jargon.

### Story 4.1: Explanation Template System

As a developer,
I want a template-based system for generating explanations,
So that all explanations follow a consistent structure and style.

**Acceptance Criteria:**

**Given** I need to generate an explanation for a highlight
**When** I use the template system
**Then** I have templates for different explanation scenarios

**And** templates support variable substitution (player name, team name, tags, etc.)

**And** templates are stored as constants or configuration in selector.py

**And** templates produce 1-2 sentence explanations

**And** templates use fan-friendly language (no technical jargon)

**And** the system is extensible for adding new templates

**And** the code includes documentation explaining the template structure

**Requirements Fulfilled:** FR-014, FR-016, NFR-007, NFR-008

---

### Story 4.2: Importance-Based Explanation Phrases

As a developer,
I want explanation phrases that describe event importance naturally,
So that users understand why an event's base importance contributed to its selection.

**Acceptance Criteria:**

**Given** I have a GameEvent with an importance level
**When** I generate an explanation phrase for importance
**Then** "critical" events use phrases like "game-defining", "crucial moment", "deciding play"

**And** "high" events use phrases like "important moment", "key play", "significant event"

**And** "medium" events use phrases like "noteworthy play", "solid moment"

**And** "low" events use phrases like "moment from the game"

**And** phrases are returned by a function get_importance_phrase(importance)

**And** the function is implemented in selector.py

**And** the function includes type hints and a docstring

**Requirements Fulfilled:** FR-015, FR-016, NFR-008

---

### Story 4.3: Personalization Explanation Phrases

As a developer,
I want explanation phrases that reference player and team preferences,
So that users understand how their preferences influenced selection.

**Acceptance Criteria:**

**Given** I have a ScoreBreakdown with player_boost > 0
**When** I generate explanation text
**Then** I include a phrase like "featuring your favorite player, {player_name}"

**And** the phrase is omitted if player_boost = 0

**Given** I have a ScoreBreakdown with team_boost > 0
**When** I generate explanation text
**Then** I include a phrase like "by your favorite team, the {team_name}"

**And** the phrase is omitted if team_boost = 0

**And** phrases are generated by helper functions in selector.py

**And** functions include type hints and docstrings

**Requirements Fulfilled:** FR-015, FR-016, NFR-008

---

### Story 4.4: Context Tag Explanation Phrases

As a developer,
I want explanation phrases that highlight contextual tags naturally,
So that users understand what made a moment special beyond base importance.

**Acceptance Criteria:**

**Given** I have context_boosts in a ScoreBreakdown
**When** I generate explanation text for tags
**Then** "game_winner" includes phrase like "sealed the victory"

**And** "buzzer_beater" includes phrase like "buzzer-beater"

**And** "clutch" includes phrase like "in a clutch moment"

**And** "fourth_quarter" includes phrase like "in a clutch fourth-quarter moment"

**And** "highlight_reel" includes phrase like "a highlight-reel play"

**And** multiple tags are combined naturally (comma-separated, avoiding repetition)

**And** phrases are generated by get_context_phrases(context_boosts) function

**And** the function is implemented in selector.py

**And** the function includes type hints and a docstring

**Requirements Fulfilled:** FR-015, FR-016, NFR-008

---

### Story 4.5: Complete Explanation Generation

As a developer,
I want a generate_explanation() function that composes full explanations,
So that every highlight has a clear, natural language explanation.

**Acceptance Criteria:**

**Given** I have a GameEvent, ScoreBreakdown, and UserPreference
**When** I call generate_explanation(event, score_breakdown, preference)
**Then** I receive a complete 1-2 sentence explanation

**And** the explanation includes the importance phrase

**And** the explanation includes the event description or type

**And** the explanation includes personalization phrases (if applicable)

**And** the explanation includes context tag phrases (if applicable)

**And** the explanation flows naturally with proper grammar and punctuation

**And** the explanation contains no technical terms (score, boost, algorithm, etc.)

**And** the function is deterministic (same inputs = same explanation)

**And** the function is implemented in selector.py

**And** the function includes comprehensive docstring with examples

**And** all generated explanations are non-empty strings

**Requirements Fulfilled:** FR-014, FR-015, FR-016, NFR-007, NFR-008, NFR-014, NFR-018

---

## Epic 5: CLI Interface and User Experience

Create a command-line interface that accepts preference flags, validates inputs, and outputs formatted highlights with helpful error messages and visual hierarchy.

### Story 5.1: Command-Line Argument Parsing

As a user,
I want to specify my preferences using command-line flags,
So that I can personalize highlight selection without editing code.

**Acceptance Criteria:**

**Given** I run the CLI script
**When** I provide --player "Player Name"
**Then** the system uses that player as the favorite_player preference

**And** I can provide --team "Team Name" to set favorite_team

**And** I can provide both --player and --team together

**And** I can provide neither flag for objective (no preference) mode

**And** I can provide --only flag to filter output to only favorite player/team

**And** the CLI uses argparse or similar library for argument parsing

**And** the CLI is implemented in cli.py module

**And** help text is available via --help flag with clear descriptions

**Requirements Fulfilled:** FR-022, FR-023, FR-024, FR-025, NFR-021

---

### Story 5.2: JSON Input Loading

As a user,
I want the CLI to load game events from a JSON file,
So that I can process different games without changing code.

**Acceptance Criteria:**

**Given** I have a JSON file with game events (e.g., sample_data.json)
**When** I run the CLI with that file as input
**Then** the system loads all events successfully

**And** the CLI reads from stdin by default (for piping: cat data.json | python cli.py)

**And** the CLI accepts a file path argument (python cli.py data.json)

**And** the CLI handles file not found errors with helpful messages

**And** the CLI validates JSON structure and reports parsing errors clearly

**And** the CLI uses GameEvent.from_dict() to deserialize events

**And** the implementation is in cli.py module

**Requirements Fulfilled:** FR-001, FR-030, NFR-019, NFR-023, NFR-024

---

### Story 5.3: Player and Team Validation

As a user,
I want the CLI to validate my player/team preferences against available data,
So that I receive helpful feedback when I make typos or invalid selections.

**Acceptance Criteria:**

**Given** I provide --player "Unknown Player"
**When** that player is not found in the game events
**Then** the CLI displays an error message listing all available players

**And** the error message uses a clear warning symbol (⚠️) or "WARNING:" prefix

**And** the error message suggests "Please re-run with a valid --player"

**Given** I provide --team "Unknown Team"
**When** that team is not found in the game events
**Then** the CLI displays an error message listing all available teams

**And** the validation happens after loading events but before processing

**And** the CLI exits with a non-zero exit code on validation failure

**And** the implementation is in cli.py module

**Requirements Fulfilled:** FR-021, FR-027, NFR-019

---

### Story 5.4: Formatted Highlight Output

As a user,
I want to see highlights in a clean, formatted display,
So that I can easily scan and understand the results.

**Acceptance Criteria:**

**Given** I have selected highlights from the CLI
**When** I view the output
**Then** each highlight shows rank, score, player, team, quarter, and description

**And** the explanation is displayed prominently for each highlight

**And** output uses visual hierarchy (bold, spacing, indentation) for readability

**And** rank is displayed as "#1", "#2", etc.

**And** score is displayed with appropriate precision (integer or 1 decimal)

**And** highlights are separated by blank lines or dividers

**And** the output fits comfortably in a standard 80-column terminal

**And** the formatting function is implemented in cli.py

**And** the output looks professional and polished

**Requirements Fulfilled:** FR-026, NFR-020, NFR-021

---

### Story 5.5: Main CLI Entry Point with run.py

As a user,
I want a simple run.py script that I can execute directly,
So that I can use the tool without complex commands.

**Acceptance Criteria:**

**Given** I am in the project directory
**When** I run `python run.py --player "Name"`
**Then** the script executes the CLI with sample data by default

**And** run.py loads shared/sample_data.json automatically

**And** run.py forwards all command-line arguments to the CLI

**And** run.py handles errors gracefully and prints helpful messages

**And** run.py exits with appropriate exit codes (0 for success, 1+ for errors)

**And** the script includes a shebang line for direct execution (chmod +x run.py)

**And** the script is documented with a docstring explaining usage

**And** users can run without arguments: `python run.py` for objective mode

**Requirements Fulfilled:** FR-022, FR-023, FR-024, FR-025, NFR-021, NFR-023, NFR-024

---

### Story 5.6: --only Flag Implementation

As a user,
I want an --only flag that filters output to my favorite player/team exclusively,
So that I can see only the highlights that match my preference.

**Acceptance Criteria:**

**Given** I provide --player "Name" --only
**When** the system processes events
**Then** only highlights featuring that player are included in output

**And** critical events from other players are excluded (--only overrides force-include)

**And** the 5-8 highlight count rule is relaxed (may return fewer than 5)

**Given** I provide --team "Name" --only
**When** the system processes events
**Then** only highlights from that team are included in output

**And** if both --player and --team are specified with --only, both filters apply (AND logic)

**And** the flag is implemented in cli.py

**And** appropriate filtering happens after initial selection but before output

**Requirements Fulfilled:** FR-024, NFR-021

---

## Epic 6: Edge Case Handling and Validation

Implement robust error handling and validation logic that gracefully manages empty lists, missing data, malformed inputs, and edge cases without crashes or undefined behavior.

### Story 6.1: Empty Event List Handling

As a developer,
I want the system to handle empty event lists gracefully,
So that users receive sensible output rather than crashes when no events are available.

**Acceptance Criteria:**

**Given** I provide an empty list of events to select_highlights()
**When** the function processes the input
**Then** it returns an empty list of highlights

**And** no exceptions are raised

**And** the behavior is deterministic

**And** the CLI displays a friendly message like "No events to process"

**And** appropriate handling is implemented in selector.py and cli.py

**And** unit tests verify this edge case

**Requirements Fulfilled:** FR-017, NFR-006

---

### Story 6.2: Null and Missing Preference Handling

As a developer,
I want the system to treat null or missing preferences as "no preference",
So that users can run the tool without specifying favorites.

**Acceptance Criteria:**

**Given** I call select_highlights() with preference=None
**When** the function processes events
**Then** it proceeds with scoring (all personalization boosts = 0)

**And** no exceptions are raised

**And** results are based purely on importance and context tags

**Given** I provide a UserPreference with favorite_player=None and favorite_team=None
**When** the function processes events
**Then** it behaves identically to preference=None

**And** the behavior is implemented in selector.py scoring functions

**And** unit tests verify this edge case

**Requirements Fulfilled:** FR-018, NFR-006

---

### Story 6.3: Unknown Importance Level Handling

As a developer,
I want the system to default unknown importance levels to "low",
So that malformed or incomplete data doesn't break processing.

**Acceptance Criteria:**

**Given** I have a GameEvent with importance = "unknown"
**When** I calculate the base score
**Then** the system defaults to "low" importance (25 points)

**And** a warning may be logged but processing continues

**Given** I have a GameEvent with importance = None
**When** I calculate the base score
**Then** the system defaults to "low" importance (25 points)

**And** the handling is implemented in calculate_base_score() function

**And** unit tests verify these edge cases

**Requirements Fulfilled:** FR-019, NFR-006

---

### Story 6.4: Missing Optional Field Handling

As a developer,
I want the system to handle events with missing optional fields gracefully,
So that incomplete data doesn't cause crashes.

**Acceptance Criteria:**

**Given** I have a GameEvent with missing tags field (None or empty)
**When** I process the event
**Then** context_boosts returns an empty dictionary

**And** no exceptions are raised

**Given** I have a GameEvent with missing description
**When** I generate an explanation
**Then** the system uses the event type or a default phrase

**And** no exceptions are raised

**And** the handling is implemented across selector.py functions

**And** unit tests verify these edge cases

**Requirements Fulfilled:** FR-020, NFR-006

---

### Story 6.5: Malformed Data Validation

As a developer,
I want input validation that catches malformed data early,
So that users receive clear error messages rather than cryptic exceptions.

**Acceptance Criteria:**

**Given** I provide invalid JSON to the CLI
**When** the CLI attempts to parse it
**Then** I receive a clear error message indicating the JSON is malformed

**And** the error message suggests checking the file format

**And** the CLI exits gracefully with a non-zero exit code

**Given** I provide a dictionary missing required GameEvent fields
**When** GameEvent.from_dict() is called
**Then** an appropriate exception is raised with a clear message

**And** the validation is implemented in models.py and cli.py

**And** unit tests verify validation behavior

**Requirements Fulfilled:** NFR-006, NFR-019

---

### Story 6.6: Zero or Insufficient Events Edge Cases

As a developer,
I want the system to handle scenarios with very few events appropriately,
So that rules like "5-8 highlights" don't break with small datasets.

**Acceptance Criteria:**

**Given** I provide only 1 event
**When** I call select_highlights()
**Then** I receive 1 highlight (all available)

**And** no exceptions are raised

**Given** I provide exactly 5 events
**When** I call select_highlights()
**Then** I receive all 5 highlights

**Given** I provide fewer than 3 events featuring the favorite player
**When** the 50% rule would apply
**Then** the rule is skipped (insufficient qualifying events)

**And** processing continues normally

**And** the handling is implemented in selector.py

**And** unit tests verify these edge cases

**Requirements Fulfilled:** FR-008, FR-012, NFR-006

---

## Epic 7: Testing, Performance, and Quality Assurance

Build a comprehensive test suite achieving 88%+ coverage, implement performance benchmarks, ensure code quality standards, and create complete documentation for the project.

### Story 7.1: Data Model Unit Tests

As a developer,
I want comprehensive unit tests for all data models,
So that serialization, deserialization, and validation work correctly.

**Acceptance Criteria:**

**Given** I have implemented all data models (GameEvent, UserPreference, ScoreBreakdown, Highlight)
**When** I run the test suite
**Then** test_models.py contains tests for model instantiation

**And** tests verify type hints are correct (can run mypy)

**And** tests verify to_dict() serialization works for all models

**And** tests verify from_dict() deserialization works for all models

**And** tests verify round-trip serialization (obj == Model.from_dict(obj.to_dict()))

**And** tests verify edge cases (None values, missing fields)

**And** tests are implemented in tests/test_models.py

**And** all tests pass successfully

**Requirements Fulfilled:** FR-029, FR-030, NFR-010, NFR-011

---

### Story 7.2: Scoring Engine Unit Tests

As a developer,
I want comprehensive unit tests for the scoring engine,
So that all scoring functions produce correct and deterministic results.

**Acceptance Criteria:**

**Given** I have implemented all scoring functions
**When** I run the test suite
**Then** test_scoring.py contains tests for calculate_base_score()

**And** tests verify importance level mappings (critical=100, high=75, medium=50, low=25)

**And** tests verify calculate_player_boost() with matching and non-matching players

**And** tests verify calculate_team_boost() with matching and non-matching teams

**And** tests verify calculate_context_boosts() for all defined tags

**And** tests verify calculate_score() returns correct ScoreBreakdown totals

**And** tests verify deterministic behavior (same inputs = same outputs)

**And** tests are implemented in tests/test_scoring.py

**And** all tests pass successfully

**Requirements Fulfilled:** FR-003, FR-004, FR-005, FR-006, FR-007, NFR-005

---

### Story 7.3: Selection and Ranking Unit Tests

As a developer,
I want comprehensive unit tests for selection and ranking logic,
So that highlight selection follows all business rules correctly.

**Acceptance Criteria:**

**Given** I have implemented select_highlights() and supporting functions
**When** I run the test suite
**Then** test_selection.py contains tests for sorting by score

**And** tests verify deterministic tie-breaking logic

**And** tests verify force-include of critical events

**And** tests verify 5-8 highlight selection range

**And** tests verify 50% favorite player representation rule

**And** tests verify selection with no preferences (objective mode)

**And** tests verify deterministic behavior across multiple runs

**And** tests are implemented in tests/test_selection.py

**And** all tests pass successfully

**Requirements Fulfilled:** FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, NFR-005

---

### Story 7.4: Explanation Generation Unit Tests

As a developer,
I want comprehensive unit tests for explanation generation,
So that all explanations are natural, complete, and accurate.

**Acceptance Criteria:**

**Given** I have implemented explanation generation functions
**When** I run the test suite
**Then** test_explanations.py contains tests for importance phrase generation

**And** tests verify personalization phrase generation

**And** tests verify context tag phrase generation

**And** tests verify complete explanation composition

**And** tests verify explanations are non-empty (100% coverage)

**And** tests verify explanation length (1-2 sentences)

**And** tests verify no technical jargon appears in explanations

**And** tests verify deterministic explanation generation

**And** tests are implemented in tests/test_explanations.py

**And** all tests pass successfully

**Requirements Fulfilled:** FR-014, FR-015, FR-016, NFR-007, NFR-008

---

### Story 7.5: Edge Case Integration Tests

As a developer,
I want integration tests that verify edge case handling end-to-end,
So that the system handles all error scenarios gracefully.

**Acceptance Criteria:**

**Given** I have implemented all edge case handling
**When** I run the test suite
**Then** test_edge_cases.py contains tests for empty event lists

**And** tests verify null/missing preference handling

**And** tests verify unknown importance level handling

**And** tests verify missing optional field handling

**And** tests verify insufficient event scenarios

**And** tests verify malformed data handling in JSON deserialization

**And** all tests verify no crashes occur (NFR-006)

**And** tests are implemented in tests/test_edge_cases.py

**And** all tests pass successfully

**Requirements Fulfilled:** FR-017, FR-018, FR-019, FR-020, NFR-006

---

### Story 7.6: End-to-End Integration Tests

As a developer,
I want integration tests that verify the complete workflow,
So that all components work together correctly from input to output.

**Acceptance Criteria:**

**Given** I have implemented the complete system
**When** I run integration tests
**Then** test_integration.py contains tests using sample_data.json

**And** tests verify complete workflow: load events → score → select → explain → output

**And** tests verify CLI argument parsing and execution

**And** tests verify --player, --team, and --only flags work correctly

**And** tests verify player/team validation with helpful error messages

**And** tests verify formatted output generation

**And** tests verify deterministic end-to-end behavior

**And** tests are implemented in tests/test_integration.py

**And** all tests pass successfully

**Requirements Fulfilled:** FR-028, FR-022, FR-023, FR-024, FR-025, FR-026, FR-027, NFR-005

---

### Story 7.7: Performance Benchmark Tests

As a developer,
I want performance benchmark tests that verify speed requirements,
So that I can confirm the system meets NFR-001 and NFR-002 targets.

**Acceptance Criteria:**

**Given** I have implemented the complete system
**When** I run performance tests
**Then** tests verify processing 15 events completes in <100ms

**And** tests verify processing 1000 events completes in <1s

**And** benchmarks measure actual execution time using time.perf_counter()

**And** benchmarks run multiple iterations for statistical confidence

**And** benchmarks are implemented in tests/test_integration.py or separate benchmark file

**And** all performance targets are met

**Requirements Fulfilled:** NFR-001, NFR-002, NFR-004

---

### Story 7.8: Test Coverage and Quality Gates

As a developer,
I want test coverage reporting and quality gates,
So that I can verify the project meets the 88%+ coverage target.

**Acceptance Criteria:**

**Given** I have implemented all tests
**When** I run pytest with coverage reporting
**Then** the test suite achieves ≥88% code coverage across all modules

**And** coverage includes models.py, selector.py, and cli.py

**And** coverage report identifies any untested code paths

**And** all tests pass without failures or errors

**And** test execution is fast (<5 seconds for full suite)

**And** coverage configuration is in pyproject.toml or .coveragerc

**And** coverage can be run via: pytest tests/ --cov=highlight_selector

**Requirements Fulfilled:** NFR-009, NFR-015

---

### Story 7.9: Code Quality Standards (Black, Mypy, Linting)

As a developer,
I want code quality tools configured and passing,
So that the codebase follows Python best practices.

**Acceptance Criteria:**

**Given** I have completed implementation
**When** I run code quality checks
**Then** black formatter validates all Python files (PEP 8 compliance)

**And** mypy strict mode type checking passes with zero errors

**And** all public functions have type hints (100% coverage)

**And** all public functions have docstrings following Google style

**And** code follows single responsibility principle

**And** pure functions are used for core business logic

**And** quality tools are configured in pyproject.toml

**And** quality checks can be run via: black . && mypy highlight_selector/

**Requirements Fulfilled:** NFR-010, NFR-011, NFR-012, NFR-013, NFR-014, NFR-018

---

### Story 7.10: Project Documentation and README

As a user and developer,
I want complete documentation that explains how to install, use, and extend the project,
So that I can quickly understand and work with the codebase.

**Acceptance Criteria:**

**Given** I am a new user or developer
**When** I read the project documentation
**Then** README.md includes project overview and purpose

**And** README includes installation instructions (venv setup, dependencies)

**And** README includes quick start examples (CLI usage with all flags)

**And** README includes programmatic API examples (Python code)

**And** README includes links to additional documentation

**And** quickstart.md provides step-by-step tutorial with sample_data.json

**And** data-model.md documents all data structures with field descriptions

**And** documentation includes working code examples

**And** all code examples are tested and verified to work

**Requirements Fulfilled:** NFR-017, NFR-021, NFR-022, Additional Requirements (Documentation)

---

### Story 7.11: Sample Data and Demo Script

As a user,
I want sample data and a demo script that work out of the box,
So that I can see the tool in action immediately after setup.

**Acceptance Criteria:**

**Given** I have installed the project
**When** I run python run.py with no modifications
**Then** the script processes shared/sample_data.json successfully

**And** the output displays properly formatted highlights

**And** I can run python run.py --player "LeBron James" and see personalized results

**And** I can run python run.py --team "Lakers" and see team-filtered results

**And** I can run python run.py --player "LeBron James" --only for exclusive filtering

**And** sample_data.json contains the 15 events from Track1 (Lakers vs Celtics)

**And** all demo commands are documented in README.md

**And** the demo validates the complete user journey from PRD

**Requirements Fulfilled:** Additional Requirements (Sample Data, Track2 Success)

---

