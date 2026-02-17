# 🏀 AI Highlight Selector — Feature Overview

## Purpose

The **AI Highlight Selector** is a logic-only engine that takes a list of game events (JSON) and simple user preferences, then intelligently selects the most relevant highlights and provides a short human-readable explanation for each selection.

## What It Does

| Input | Output |
|---|---|
| List of game events (JSON) | Filtered & ranked highlights |
| User preference (favorite player / team) | Short explanation per highlight |

## Scope & Constraints

- **No real video processing** — this is pure selection logic
- **Deterministic** — given the same input, always produces the same output
- **Explainable** — every selection includes a reason
- **Configurable** — users can express preferences via player or team

## How Selection Works

The selector uses a scoring algorithm that considers:

1. **Event importance** — critical > high > medium > low
2. **User preference match** — events involving the user's favorite player/team get a boost
3. **Event type weight** — game-winning plays, dunks, and blocks are visually exciting
4. **Clutch factor** — events tagged as "clutch" or in Q4 receive extra weight
5. **Diversity** — the selector favors variety across event types and quarters

## Example

**Input preference:** `{ "favorite_player": "LeBron James" }`

**Output:** A ranked list of 5–8 top highlights featuring LeBron-related events scored highest, with exciting plays from other players included for context and narrative flow.

## Data Schema

### Game Event

```json
{
  "id": "evt-001",
  "type": "three_pointer",
  "timestamp": "Q1 02:34",
  "quarter": 1,
  "player": "LeBron James",
  "team": "Lakers",
  "description": "LeBron James drains a deep three from the logo.",
  "importance": "high",
  "tags": ["clutch", "logo_shot", "momentum"]
}
```

### User Preference

```json
{
  "favorite_player": "LeBron James",
  "favorite_team": null
}
```

### Output Highlight

```json
{
  "event_id": "evt-001",
  "rank": 1,
  "score": 95,
  "explanation": "Selected because this is a high-importance three-pointer by your favorite player LeBron James, tagged as clutch — a momentum-setting play to open the game."
}
```
