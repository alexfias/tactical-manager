from __future__ import annotations

import json
from pathlib import Path

from tactical_manager.core.game_state import GameState
from tactical_manager.core.season import Season


SAVE_VERSION = 1


def game_state_to_dict(game_state: GameState) -> dict:
    return {
        "version": SAVE_VERSION,
        "user_club_id": game_state.user_club_id,
        "season": game_state.season.to_dict(),
    }


def game_state_from_dict(data: dict) -> GameState:
    version = data.get("version", 1)
    if version != SAVE_VERSION:
        raise ValueError(f"Unsupported save version: {version}")

    season = Season.from_dict(data["season"])

    return GameState(
        season=season,
        user_club_id=data["user_club_id"],
    )


def save_game(game_state: GameState, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    payload = game_state_to_dict(game_state)

    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    game_state.save_path = path


def load_game(path: str | Path) -> GameState:
    path = Path(path)

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    game_state = game_state_from_dict(data)
    game_state.save_path = path
    return game_state