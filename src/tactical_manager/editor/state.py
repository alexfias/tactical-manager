from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tactical_manager.core.models import Club


@dataclass
class EditorState:
    current_file: Path | None = None
    current_club: Club | None = None
    selected_player_index: int | None = None
    dirty: bool = False