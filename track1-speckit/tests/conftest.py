"""Pytest fixtures for AI Highlight Selector tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

SAMPLE_DATA_PATH = (
    Path(__file__).resolve().parent.parent / "shared" / "sample_data.json"
)


@pytest.fixture
def sample_data() -> dict[str, Any]:
    """Load the full sample data from shared/sample_data.json."""
    with open(SAMPLE_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def sample_events(sample_data: dict[str, Any]) -> list[dict[str, Any]]:
    """Return the raw events list from sample data."""
    return sample_data["events"]


@pytest.fixture
def sample_game_events(sample_events: list[dict[str, Any]]) -> list[Any]:
    """Return GameEvent objects from sample data."""
    from highlight_selector.models import GameEvent

    return [GameEvent.from_dict(e) for e in sample_events]


@pytest.fixture
def no_preference() -> Any:
    """Return a UserPreference with no preferences set."""
    from highlight_selector.models import UserPreference

    return UserPreference()


@pytest.fixture
def lebron_preference() -> Any:
    """Return a UserPreference for LeBron James."""
    from highlight_selector.models import UserPreference

    return UserPreference(favorite_player="LeBron James")


@pytest.fixture
def celtics_preference() -> Any:
    """Return a UserPreference for the Celtics."""
    from highlight_selector.models import UserPreference

    return UserPreference(favorite_team="Celtics")


@pytest.fixture
def davis_lakers_preference() -> Any:
    """Return a UserPreference for Anthony Davis and Lakers."""
    from highlight_selector.models import UserPreference

    return UserPreference(favorite_player="Anthony Davis", favorite_team="Lakers")
