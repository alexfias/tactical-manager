# src/tactical_manager/core/data.py

from tactical_manager.core.models import Team, Player, Fixture


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