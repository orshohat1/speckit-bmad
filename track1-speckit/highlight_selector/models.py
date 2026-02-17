"""Data models for AI Highlight Selector.

Provides typed dataclasses for game events, user preferences,
score breakdowns, and highlights. All models support JSON
serialization via to_dict()/from_dict() methods.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# Importance level ranking for tie-breaking (higher = more important)
IMPORTANCE_RANK: dict[str, int] = {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1,
}


@dataclass
class GameEvent:
    """Represents a single event in a game.

    Attributes:
        id: Unique identifier for the event.
        type: Event type (e.g., "dunk", "three_pointer", "block").
        timestamp: Game clock string (e.g., "Q4 02:15").
        quarter: Quarter number (1-4).
        player: Player name associated with the event.
        team: Team name associated with the event.
        description: Human-readable description of the event.
        importance: Importance level: "critical", "high", "medium", or "low".
        tags: Categorical tags (e.g., ["clutch", "game_winner"]).
    """

    id: str
    type: str
    timestamp: str
    quarter: int
    player: str
    team: str
    description: str
    importance: str
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a dictionary."""
        return {
            "id": self.id,
            "type": self.type,
            "timestamp": self.timestamp,
            "quarter": self.quarter,
            "player": self.player,
            "team": self.team,
            "description": self.description,
            "importance": self.importance,
            "tags": list(self.tags),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GameEvent:
        """Deserialize from a dictionary.

        Applies lenient validation:
        - Unknown importance defaults to "low" (FR-012).
        - Missing tags defaults to empty list.
        """
        importance = data.get("importance", "low")
        if importance not in IMPORTANCE_RANK:
            importance = "low"
        return cls(
            id=data["id"],
            type=data["type"],
            timestamp=data.get("timestamp", ""),
            quarter=data.get("quarter", 1),
            player=data.get("player", "Unknown"),
            team=data.get("team", "Unknown"),
            description=data.get("description", ""),
            importance=importance,
            tags=data.get("tags", []),
        )


@dataclass
class UserPreference:
    """User's personalization settings.

    Attributes:
        favorite_player: Optional favorite player name.
        favorite_team: Optional favorite team name.
    """

    favorite_player: str | None = None
    favorite_team: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a dictionary."""
        return {
            "favorite_player": self.favorite_player,
            "favorite_team": self.favorite_team,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> UserPreference:
        """Deserialize from a dictionary.

        Handles None input gracefully (FR-011).
        """
        if data is None:
            return cls()
        return cls(
            favorite_player=data.get("favorite_player"),
            favorite_team=data.get("favorite_team"),
        )


@dataclass
class ScoreBreakdown:
    """Detailed scoring components for explainability.

    Attributes:
        base_score: Score from importance level.
        player_boost: Boost for favorite player match (0 or 30).
        team_boost: Boost for favorite team match (0 or 15).
        context_boosts: Dict of contextual boosts (e.g., {"clutch": 20}).
        total_score: Sum of all scoring components.
    """

    base_score: int
    player_boost: int
    team_boost: int
    context_boosts: dict[str, int] = field(default_factory=dict)
    total_score: int = 0

    def __post_init__(self) -> None:
        """Calculate total_score if it was not explicitly provided."""
        if self.total_score == 0:
            self.total_score = (
                self.base_score
                + self.player_boost
                + self.team_boost
                + sum(self.context_boosts.values())
            )

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a dictionary."""
        return {
            "base_score": self.base_score,
            "player_boost": self.player_boost,
            "team_boost": self.team_boost,
            "context_boosts": dict(self.context_boosts),
            "total_score": self.total_score,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ScoreBreakdown:
        """Deserialize from a dictionary."""
        return cls(
            base_score=data["base_score"],
            player_boost=data["player_boost"],
            team_boost=data["team_boost"],
            context_boosts=data.get("context_boosts", {}),
            total_score=data.get("total_score", 0),
        )


@dataclass
class Highlight:
    """A selected highlight with explanation.

    Attributes:
        event: The original game event.
        rank: Position in final output (1 = best).
        score: Final calculated score.
        explanation: Human-readable 1-2 sentence explanation.
    """

    event: GameEvent
    rank: int
    score: int
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a dictionary."""
        return {
            "event": self.event.to_dict(),
            "rank": self.rank,
            "score": self.score,
            "explanation": self.explanation,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Highlight:
        """Deserialize from a dictionary."""
        return cls(
            event=GameEvent.from_dict(data["event"]),
            rank=data["rank"],
            score=data["score"],
            explanation=data["explanation"],
        )
