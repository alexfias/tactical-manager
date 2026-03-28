from tactical_manager.core.match_engine import simulate_match
from tactical_manager.core.models import Player, Team, Tactic


def make_team(name: str) -> Team:
    squad = []
    squad.append(Player("GK", "GK", 50, 50, 5, 60, 70, 30, 60, 50))
    for i in range(4):
        squad.append(Player(f"D{i}", "DEF", 60, 55, 10, 70, 70, 65, 75, 75))
    for i in range(3):
        squad.append(Player(f"M{i}", "MID", 72, 72, 40, 60, 70, 68, 78, 80))
    for i in range(3):
        squad.append(Player(f"A{i}", "ATT", 65, 74, 75, 25, 72, 80, 75, 78))
    return Team(name=name, squad=squad, tactic=Tactic())


def test_simulate_match_runs():
    home = make_team("Home")
    away = make_team("Away")
    result = simulate_match(home, away, seed=1)

    assert result.home_team == "Home"
    assert result.away_team == "Away"
    assert result.stats.home_goals >= 0
    assert result.stats.away_goals >= 0


def test_goals_reasonable_range():
    home = make_team("Home")
    away = make_team("Away")

    result = simulate_match(home, away, seed=1)

    assert result.stats.home_goals < 10
    assert result.stats.away_goals < 10