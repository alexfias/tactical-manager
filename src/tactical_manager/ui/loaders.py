from __future__ import annotations

import json
from pathlib import Path
from tactical_manager.core.models import Player, Tactic, Team


def load_teams_from_json(path: str | Path) -> dict[str, Team]:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    teams: dict[str, Team] = {}
    for team_data in raw["teams"]:
        squad = []
        for p in team_data["squad"]:
            squad.append(Player(**p))

        tactic = Tactic(**team_data.get("tactic", {}))
        team = Team(name=team_data["name"], squad=squad, tactic=tactic)
        teams[team.name] = team

    return teams
