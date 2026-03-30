# src/tactical_manager/core/data.py

from __future__ import annotations

import json
from pathlib import Path

from tactical_manager.core.models import (
    BoardExpectations,
    Club,
    ClubFinance,
    ClubInfrastructure,
    ClubSupport,
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



def load_team_from_file(path: Path) -> Team:
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    squad = [Player(**player_data) for player_data in raw["squad"]]
    return Team(name=raw["name"], squad=squad)


def load_teams_from_folder(folder: Path) -> dict[str, Team]:
    teams: dict[str, Team] = {}

    for path in sorted(folder.glob("*.json")):
        print(f"Loading team file: {path}")
        team = load_team_from_file(path)
        teams[team.name] = team

    return teams

def parse_player(data: dict) -> Player:
    return Player(
        name=data["name"],
        position=data["position"],
        attack=data["attack"],
        defense=data["defense"],
        passing=data["passing"],
        stamina=data["stamina"],
        morale=data["morale"],
        form=data["form"],
        wage=data.get("wage", 0),
        market_value=data.get("market_value", 0),
        age=data.get("age", 24),
        contract_weeks=data.get("contract_weeks", 104),
        potential=data.get("potential", 50),
    )

def parse_tactic(data: dict | None) -> Tactic:
    data = data or {}
    return Tactic(
        shape=data.get("shape", "4-4-2"),
        pressing=data.get("pressing", 50),
        tempo=data.get("tempo", 50),
        width=data.get("width", 50),
    )

def parse_club(data: dict) -> Club:
    team_data = data["team"]

    finance_data = data.get("finance", {})
    infrastructure_data = data.get("infrastructure", {})
    support_data = data.get("support", {})
    board_data = data.get("board", {})

    return Club(
        name=data["name"],
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
        reputation=data.get("reputation", 50.0),
    )

def load_clubs_from_folder(folder: Path) -> dict[str, Club]:
    clubs: dict[str, Club] = {}

    for file_path in sorted(folder.glob("*.json")):
        print(f"Loading club file: {file_path}")
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        club = parse_club(data)
        clubs[club.name] = club

    return clubs

def parse_team(data: dict) -> Team:
    squad = [parse_player(player_data) for player_data in data.get("squad", [])]

    tactic_data = data.get("tactic", {})
    tactic = Tactic(
        shape=tactic_data.get("shape", "4-4-2"),
        pressing=tactic_data.get("pressing", 50),
        tempo=tactic_data.get("tempo", 50),
        width=tactic_data.get("width", 50),
    )

    return Team(
        name=data["name"],
        squad=squad,
        tactic=tactic,
    )

