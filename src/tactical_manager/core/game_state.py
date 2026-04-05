from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tactical_manager.core.models import Club
from tactical_manager.core.season import Season


@dataclass
class GameState:
    season: Season
    user_club_name: str
    save_path: Path | None = None

    @property
    def user_club(self) -> Club:
        for club in self.season.clubs.values():
            if club.identity.name == self.user_club_name:
                return club
        raise ValueError(f"User club '{self.user_club_name}' not found.")