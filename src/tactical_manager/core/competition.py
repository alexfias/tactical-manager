from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Competition:
    name: str
    country: str
    competition_type: str  # e.g. "league"
    club_names: List[str]
    rounds: int = 2
    points_for_win: int = 3
    points_for_draw: int = 1
    points_for_loss: int = 0