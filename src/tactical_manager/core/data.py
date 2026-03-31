from __future__ import annotations

import json
from pathlib import Path
from dataclasses import fields

from tactical_manager.core.competition import Competition
from tactical_manager.core.models import (
    BoardExpectations,
    Club,
    ClubFinance,
    ClubInfrastructure,
    ClubSupport,
    ClubIdentity,
    Player,
    Tactic,
    Team,
    Fixture,
)


def create_demo_teams() -> dict[str, Team]:
    def make_team(name: str) -> Team:
        squad = []
        squad.append(Player("GK", "GK", 50, 50, 5, 60, 70, 30, 60, 50))
        for i in range(4):
            squad.append(Player(f"D{i}", "DEF", 60, 55, 40, 65, 60, 50, 55, 50))
        for i in range(4):
            squad.append(Player(f"M{i}", "MID", 65, 60, 60, 60, 60, 60, 60, 60))
        for i in range(2):
            squad.append(Player(f"F{i}", "FWD", 70, 65, 70, 50, 50, 65, 55, 60))
        return Team(name=name, squad=squad)

    return {
        "Red FC": make_team("Red FC"),
        "Blue United": make_team("Blue United"),
        "Green Town": make_team("Green Town"),
        "Yellow City": make_team("Yellow City"),
    }


def create_round_robin_fixtures(team_names: list[str]) -> list[Fixture]:
    fixtures: list[Fixture] = []
    for i, home in enumerate(team_names):
        for away in team_names[i + 1:]:
            fixtures.append(Fixture(home=home, away=away))
    return fixtures


def parse_player(data: dict) -> Player:
    return Player(
        name=data["name"],
        position=data["position"],
        passing=float(data["passing"]),
        technique=float(data["technique"]),
        finishing=float(data["finishing"]),
        defending=float(data["defending"]),
        positioning=float(data["positioning"]),
        pace=float(data["pace"]),
        stamina=float(data["stamina"]),
        work_rate=float(data["work_rate"]),
        fatigue=float(data.get("fatigue", 10.0)),
        fitness=float(data.get("fitness", 95.0)),
        morale=float(data.get("morale", 70.0)),
        familiarity=float(data.get("familiarity", 50.0)),
        injury_proneness=float(data.get("injury_proneness", 20.0)),
        injured=bool(data.get("injured", False)),
    )


def parse_tactic(data: dict | None) -> Tactic:
    data = data or {}

    allowed_fields = {f.name for f in fields(Tactic)}

    # normalize old JSON keys to the actual Tactic schema
    normalized = dict(data)

    if "shape" in normalized and "formation" in allowed_fields:
        normalized["formation"] = normalized.pop("shape")

    defaults = {}

    if "formation" in allowed_fields:
        defaults["formation"] = "4-4-2"
    if "pressing" in allowed_fields:
        defaults["pressing"] = 50
    if "tempo" in allowed_fields:
        defaults["tempo"] = 50
    if "width" in allowed_fields:
        defaults["width"] = 50

    tactic_kwargs = {
        key: value
        for key, value in normalized.items()
        if key in allowed_fields
    }

    defaults.update(tactic_kwargs)
    return Tactic(**defaults)


def parse_team(team_data: dict) -> Team:
    return Team(
        name=team_data["name"],
        squad=[parse_player(player) for player in team_data["squad"]],
        tactic=parse_tactic(team_data.get("tactic")),
    )


def parse_club(data: dict) -> Club:
    team_data = data["team"]

    finance_data = data.get("finance", {})
    infrastructure_data = data.get("infrastructure", {})
    support_data = data.get("support", {})
    board_data = data.get("board", {})

    return Club(
        country=data.get("country", "Fictionland"),
        identity=ClubIdentity(
            name=data["name"],
            reputation=data.get("reputation", 50.0),
        ),
        team=parse_team(team_data),
        finance=ClubFinance(
            balance=finance_data.get("balance", 0),
            transfer_budget=finance_data.get("transfer_budget", 0),
            weekly_wages=finance_data.get("weekly_wages", 0),
            wage_budget=finance_data.get("wage_budget", 0),
            sponsorship_income=finance_data.get("sponsorship_income", 0),
            matchday_base_income=finance_data.get("matchday_base_income", 0),
        ),
        infrastructure=ClubInfrastructure(
            stadium_capacity=infrastructure_data.get("stadium_capacity", 10000),
            ticket_price=infrastructure_data.get("ticket_price", 20),
            training_level=infrastructure_data.get("training_level", 50),
            youth_level=infrastructure_data.get("youth_level", 50),
        ),
        support=ClubSupport(
            fan_confidence=support_data.get("fan_confidence", 50.0),
            fan_base=support_data.get("fan_base", 10000),
        ),
        board=BoardExpectations(
            target_finish=board_data.get("target_finish", 6),
            max_wage_ratio=board_data.get("max_wage_ratio", 0.7),
            philosophy=board_data.get("philosophy", "balanced"),
        ),
    )


def load_team_from_file(path: Path) -> Team:
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    return parse_team(raw)


def load_teams_from_folder(folder: Path) -> dict[str, Team]:
    teams: dict[str, Team] = {}

    for path in sorted(folder.glob("*.json")):
        print(f"Loading team file: {path}")
        team = load_team_from_file(path)
        teams[team.name] = team

    return teams


def load_clubs_from_folder(folder: Path) -> dict[str, Club]:
    clubs: dict[str, Club] = {}

    for file_path in sorted(folder.glob("*.json")):
        print(f"Loading club file: {file_path}")
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        club = parse_club(data)
        clubs[club.identity.name] = club

    return clubs


def load_competition_from_file(path: Path) -> Competition:
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    return Competition(
        name=raw["name"],
        country=raw["country"],
        competition_type=raw["type"],
        club_names=raw["clubs"],
        rounds=raw.get("rounds", 2),
        points_for_win=raw.get("points_for_win", 3),
        points_for_draw=raw.get("points_for_draw", 1),
        points_for_loss=raw.get("points_for_loss", 0),
    )


def load_competitions_from_folder(folder: Path) -> list[Competition]:
    competitions = []
    for path in sorted(folder.glob("*.json")):
        competitions.append(load_competition_from_file(path))
    return competitions