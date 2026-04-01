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

        # technical
        passing=float(data.get("passing", 50.0)),
        first_touch=float(data.get("first_touch", 50.0)),
        technique=float(data.get("technique", 50.0)),
        dribbling=float(data.get("dribbling", 50.0)),
        finishing=float(data.get("finishing", 50.0)),
        long_shots=float(data.get("long_shots", 50.0)),
        tackling=float(data.get("tackling", 50.0)),
        heading=float(data.get("heading", 50.0)),
        crossing=float(data.get("crossing", 50.0)),

        # mental / tactical
        positioning=float(data.get("positioning", 50.0)),
        vision=float(data.get("vision", 50.0)),
        decision_making=float(data.get("decision_making", 50.0)),
        anticipation=float(data.get("anticipation", 50.0)),
        composure=float(data.get("composure", 50.0)),
        concentration=float(data.get("concentration", 50.0)),
        work_rate=float(data.get("work_rate", 50.0)),
        discipline=float(data.get("discipline", 50.0)),
        aggression=float(data.get("aggression", 50.0)),

        # physical
        pace=float(data.get("pace", 50.0)),
        acceleration=float(data.get("acceleration", 50.0)),
        agility=float(data.get("agility", 50.0)),
        strength=float(data.get("strength", 50.0)),
        stamina=float(data.get("stamina", 50.0)),
        jumping=float(data.get("jumping", 50.0)),

        # dynamic state
        fatigue=float(data.get("fatigue", 10.0)),
        fitness=float(data.get("fitness", 95.0)),
        morale=float(data.get("morale", 60.0)),
        familiarity=float(data.get("familiarity", 50.0)),
        confidence=float(data.get("confidence", 50.0)),
        sharpness=float(data.get("sharpness", 50.0)),
        injury_proneness=float(data.get("injury_proneness", 20.0)),
        injured=bool(data.get("injured", False)),

        # career / economic
        age=int(data.get("age", 24)),
        wage=int(data.get("wage", 1000)),
        contract_weeks=int(data.get("contract_weeks", 104)),
        potential=float(data.get("potential", 60.0)),
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


def parse_team(data: dict) -> Team:
    squad_data = data.get("squad", [])
    squad = [parse_player(player_data) for player_data in squad_data]

    return Team(
        name=data["name"],
        squad=squad,
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



def load_club(path: Path) -> Club:
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    return parse_club(raw)


def club_to_dict(club: Club) -> dict:
    return {
        "name": club.identity.name,
        "reputation": club.identity.reputation,
        "team": {
            "name": club.team.name,
            "squad": [
                {
                    "name": p.name,
                    "position": p.position,
                    "attack": p.attack,
                    "defense": p.defense,
                    "passing": p.passing,
                    "stamina": p.stamina,
                    "morale": p.morale,
                    "form": p.form,
                    "wage": p.wage,
                    "market_value": p.market_value,
                    "age": p.age,
                    "contract_weeks": p.contract_weeks,
                    "potential": p.potential,
                }
                for p in club.team.squad
            ],
        },
        "finance": {
            "balance": club.finance.balance,
            "transfer_budget": club.finance.transfer_budget,
            "weekly_wages": club.finance.weekly_wages,
            "wage_budget": club.finance.wage_budget,
            "sponsorship_income": club.finance.sponsorship_income,
            "matchday_base_income": club.finance.matchday_base_income,
        },
        "infrastructure": {
            "stadium_capacity": club.infrastructure.stadium_capacity,
            "ticket_price": club.infrastructure.ticket_price,
            "training_level": club.infrastructure.training_level,
            "youth_level": club.infrastructure.youth_level,
            "medical_level": club.infrastructure.medical_level,
        },
        "support": {
            "fan_mood": club.support.fan_mood,
            "expectation": club.support.expectation,
        },
        "board": {
            "patience": club.board.patience,
            "confidence": club.board.confidence,
        },
    }


def save_club(club: Club, path: Path) -> None:
    data = club_to_dict(club)

    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)