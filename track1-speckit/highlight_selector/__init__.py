"""AI Highlight Selector - Curated game highlights with explanations."""

from highlight_selector.models import (
    GameEvent,
    Highlight,
    ScoreBreakdown,
    UserPreference,
)
from highlight_selector.selector import select_highlights

__all__ = [
    "GameEvent",
    "Highlight",
    "ScoreBreakdown",
    "UserPreference",
    "select_highlights",
]
