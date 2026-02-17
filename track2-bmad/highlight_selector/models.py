"""Data models for the AI Highlight Selector.

This module defines the core data structures used throughout the system:
- GameEvent: Represents a single game event with metadata
- UserPreference: User personalization settings for highlight selection
- ScoreBreakdown: Transparent breakdown showing how a score was calculated
- Highlight: Output model packaging selected events with metadata
"""

from dataclasses import dataclass, field
from typing import Any, Optional, Union


@dataclass
class GameEvent:
    """Represents a single game event with metadata and importance scoring.

    A GameEvent captures a moment in the game that could potentially be
    selected as a highlight. It includes timing information, player/team
    attribution, importance level, and optional context tags.

    Attributes:
        id: Unique identifier for the event (e.g., "event_001").
        type: Type of play (e.g., "dunk", "three_pointer", "block").
        timestamp: Game clock time when event occurred (e.g., "Q4 2:45").
        quarter: Quarter number (1-4 for regulation, 5+ for overtime).
        player: Name of player who performed the action.
        team: Name of the team (e.g., "Lakers", "Celtics").
        description: Human-readable description of what happened.
        importance: Importance level - must be "critical", "high", "medium", or "low".
        tags: Optional context tags like "clutch", "buzzer_beater", "game_winner".
              Defaults to empty list if not provided.

    Example:
        >>> event = GameEvent(
        ...     id="event_001",
        ...     type="dunk",
        ...     timestamp="Q4 2:45",
        ...     quarter=4,
        ...     player="LeBron James",
        ...     team="Lakers",
        ...     description="Powerful dunk in transition",
        ...     importance="critical",
        ...     tags=["clutch", "game_winner"]
        ... )
        >>> event.player
        'LeBron James'
        >>> event.tags
        ['clutch', 'game_winner']
    """

    id: str
    type: str
    timestamp: str
    quarter: int
    player: str
    team: str
    description: str
    importance: str  # "critical", "high", "medium", or "low"
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert GameEvent to dictionary for JSON serialization.

        Returns:
            Dictionary representation suitable for JSON serialization.
        """
        return {
            "id": self.id,
            "type": self.type,
            "timestamp": self.timestamp,
            "quarter": self.quarter,
            "player": self.player,
            "team": self.team,
            "description": self.description,
            "importance": self.importance,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GameEvent":
        """Create GameEvent from dictionary.

        Args:
            data: Dictionary containing GameEvent fields.

        Returns:
            GameEvent instance.
        """
        return cls(**data)


@dataclass
class UserPreference:
    """User personalization settings for highlight selection.

    Captures the user's favorite player and/or team to apply scoring boosts
    during highlight selection. Both fields are optional - users can specify
    neither, one, or both preferences.

    Attributes:
        favorite_player: Name of user's favorite player (e.g., "LeBron James").
                         When specified, events featuring this player receive a
                         scoring boost (+30 points). Defaults to None.
        favorite_team: Name of user's favorite team (e.g., "Lakers").
                       When specified, events involving this team receive a
                       scoring boost (+15 points). Defaults to None.

    Example:
        >>> # Both preferences specified
        >>> pref = UserPreference(
        ...     favorite_player="LeBron James",
        ...     favorite_team="Lakers"
        ... )
        >>> pref.favorite_player
        'LeBron James'

        >>> # Only player preference
        >>> pref = UserPreference(favorite_player="Stephen Curry")
        >>> pref.favorite_team is None
        True

        >>> # No preferences (objective ranking)
        >>> pref = UserPreference()
        >>> pref.favorite_player is None and pref.favorite_team is None
        True
    """

    favorite_player: Optional[str] = None
    favorite_team: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert UserPreference to dictionary for JSON serialization.

        Returns:
            Dictionary representation suitable for JSON serialization.
            None values are preserved (not converted to "null" strings).
        """
        return {
            "favorite_player": self.favorite_player,
            "favorite_team": self.favorite_team,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UserPreference":
        """Create UserPreference from dictionary.

        Args:
            data: Dictionary containing UserPreference fields.

        Returns:
            UserPreference instance.
        """
        return cls(**data)


@dataclass
class ScoreBreakdown:
    """Transparent breakdown showing how an event's score was calculated.

    Provides visibility into the scoring algorithm by documenting each
    component that contributed to the final score. This enables accurate
    explanations and debugging of scoring logic.

    Attributes:
        base_score: Base importance score (e.g., 100 for critical, 70 for high).
        player_boost: Points added for favorite player match (+30 if matched).
        team_boost: Points added for favorite team match (+15 if matched).
        context_boosts: Dictionary mapping tag names to boost values
                        (e.g., {"clutch": 15, "highlight-reel": 10}).
        total_score: Final calculated score (sum of all components).

    Example:
        >>> breakdown = ScoreBreakdown(
        ...     base_score=100,
        ...     player_boost=30,
        ...     team_boost=15,
        ...     context_boosts={"clutch": 15, "highlight-reel": 10},
        ...     total_score=170
        ... )
        >>> breakdown.total_score == (
        ...     breakdown.base_score +
        ...     breakdown.player_boost +
        ...     breakdown.team_boost +
        ...     sum(breakdown.context_boosts.values())
        ... )
        True
    """

    base_score: Union[int, float]
    player_boost: Union[int, float]
    team_boost: Union[int, float]
    context_boosts: dict[str, Union[int, float]]
    total_score: Union[int, float]

    def to_dict(self) -> dict[str, Any]:
        """Convert ScoreBreakdown to dictionary for JSON serialization.

        Returns:
            Dictionary representation suitable for JSON serialization.
        """
        return {
            "base_score": self.base_score,
            "player_boost": self.player_boost,
            "team_boost": self.team_boost,
            "context_boosts": self.context_boosts,
            "total_score": self.total_score,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ScoreBreakdown":
        """Create ScoreBreakdown from dictionary.

        Args:
            data: Dictionary containing ScoreBreakdown fields.

        Returns:
            ScoreBreakdown instance.
        """
        return cls(**data)


@dataclass
class Highlight:
    """Output model packaging a selected event with its metadata.

    Represents a single highlight in the final output, combining the full
    GameEvent with its computed rank, score, and human-readable explanation.

    Attributes:
        event: Full GameEvent object containing all event details.
        rank: Position in highlight reel (1-8, where 1 is most important).
        score: Final calculated score (numeric value).
        explanation: Human-readable 1-2 sentence explanation of why this
                     event was selected (e.g., "Critical touchdown in Q3.").

    Example:
        >>> event = GameEvent(
        ...     id="evt1",
        ...     type="touchdown",
        ...     timestamp="10:23",
        ...     quarter=3,
        ...     player="J.Allen",
        ...     team="BUF",
        ...     description="15-yard TD pass",
        ...     importance="critical"
        ... )
        >>> highlight = Highlight(
        ...     event=event,
        ...     rank=1,
        ...     score=95.5,
        ...     explanation="Critical touchdown in Q3."
        ... )
        >>> highlight.event.player
        'J.Allen'
    """

    event: GameEvent
    rank: int
    score: Union[int, float]
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        """Convert Highlight to dictionary for JSON serialization.

        Nested GameEvent is also converted to a dictionary.

        Returns:
            Dictionary representation suitable for JSON serialization.
        """
        return {
            "event": self.event.to_dict(),
            "rank": self.rank,
            "score": self.score,
            "explanation": self.explanation,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Highlight":
        """Create Highlight from dictionary.

        Nested GameEvent dictionary is properly reconstructed.

        Args:
            data: Dictionary containing Highlight fields.

        Returns:
            Highlight instance.
        """
        # Reconstruct nested GameEvent
        event_data = data["event"]
        event = GameEvent.from_dict(event_data)

        return cls(
            event=event,
            rank=data["rank"],
            score=data["score"],
            explanation=data["explanation"],
        )
