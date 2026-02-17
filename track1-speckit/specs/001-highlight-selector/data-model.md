# Data Model Reference: AI Highlight Selector

**Feature**: `001-highlight-selector`  
**Last Updated**: 2026-02-17  

## Overview

The AI Highlight Selector uses four dataclasses to model the full pipeline from raw game events to curated highlights. All models support JSON serialization via `to_dict()` and `from_dict()` methods.

---

## GameEvent

Represents a single event in a game.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | `str` | Yes | — | Unique identifier (e.g., `"evt-001"`) |
| `type` | `str` | Yes | — | Event type: `"dunk"`, `"three_pointer"`, `"block"`, `"steal"`, etc. |
| `timestamp` | `str` | No | `""` | Game clock string (e.g., `"Q4 02:15"`) |
| `quarter` | `int` | No | `1` | Quarter number: 1-4 |
| `player` | `str` | No | `"Unknown"` | Player name associated with the event |
| `team` | `str` | No | `"Unknown"` | Team name associated with the event |
| `description` | `str` | No | `""` | Human-readable description |
| `importance` | `str` | No | `"low"` | One of: `"critical"`, `"high"`, `"medium"`, `"low"` |
| `tags` | `list[str]` | No | `[]` | Categorical tags (e.g., `["clutch", "game_winner"]`) |

**Validation Rules**:
- Unknown `importance` values default to `"low"` (FR-012)
- Missing optional fields use sensible defaults
- Recognized tags for scoring: `clutch`, `highlight_reel`, `game_winner`, `buzzer_beater`

### JSON Example

```json
{
  "id": "evt-014",
  "type": "dunk",
  "timestamp": "Q4 11:30",
  "quarter": 4,
  "player": "LeBron James",
  "team": "Lakers",
  "description": "LeBron finishes with a game-winning dunk off the steal!",
  "importance": "critical",
  "tags": ["game_winner", "clutch", "highlight_reel", "iconic"]
}
```

---

## UserPreference

User's personalization settings.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `favorite_player` | `str \| None` | No | `None` | Optional favorite player name |
| `favorite_team` | `str \| None` | No | `None` | Optional favorite team name |

**Validation Rules**:
- Both fields are optional (FR-011)
- `None` is treated as "no preference"
- `from_dict(None)` returns an empty preference object

### JSON Example

```json
{
  "favorite_player": "LeBron James",
  "favorite_team": "Lakers"
}
```

---

## ScoreBreakdown

Detailed scoring components for explainability (Article III).

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `base_score` | `int` | Yes | — | Score from importance level (25-100) |
| `player_boost` | `int` | Yes | — | Boost for favorite player match (0 or 30) |
| `team_boost` | `int` | Yes | — | Boost for favorite team match (0 or 15) |
| `context_boosts` | `dict[str, int]` | No | `{}` | Context-based boosts (e.g., `{"clutch": 20}`) |
| `total_score` | `int` | No | auto | Sum of all components (auto-calculated) |

### Scoring Table

| Importance | Base Score |
|-----------|-----------|
| `critical` | 100 |
| `high` | 75 |
| `medium` | 50 |
| `low` | 25 |

| Context Modifier | Points | Condition |
|-----------------|--------|-----------|
| Favorite player | +30 | Player matches preference |
| Game winner | +25 | `"game_winner"` tag |
| Clutch moment | +20 | `"clutch"` tag |
| Buzzer beater | +20 | `"buzzer_beater"` tag |
| Highlight reel | +15 | `"highlight_reel"` tag |
| Favorite team | +15 | Team matches preference |
| Fourth quarter | +10 | Quarter == 4 |

### JSON Example

```json
{
  "base_score": 100,
  "player_boost": 30,
  "team_boost": 15,
  "context_boosts": {
    "game_winner": 25,
    "clutch": 20,
    "highlight_reel": 15,
    "fourth_quarter": 10
  },
  "total_score": 215
}
```

---

## Highlight

A selected highlight with explanation for the end user.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `event` | `GameEvent` | Yes | — | The original game event |
| `rank` | `int` | Yes | — | Position in output (1 = best) |
| `score` | `int` | Yes | — | Final calculated score |
| `explanation` | `str` | Yes | — | Human-readable 1-2 sentence explanation |

### JSON Example

```json
{
  "event": {
    "id": "evt-014",
    "type": "dunk",
    "timestamp": "Q4 11:30",
    "quarter": 4,
    "player": "LeBron James",
    "team": "Lakers",
    "description": "LeBron finishes with a game-winning dunk off the steal!",
    "importance": "critical",
    "tags": ["game_winner", "clutch", "highlight_reel", "iconic"]
  },
  "rank": 1,
  "score": 215,
  "explanation": "This critical dunk by LeBron James was a defining moment of the game. Sealed the victory, in a clutch fourth-quarter moment, a highlight-reel play, featuring your favorite player, LeBron James, by your favorite team, the Lakers."
}
```
