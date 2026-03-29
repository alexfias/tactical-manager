from __future__ import annotations

from dataclasses import dataclass, field
from tactical_manager.core.match_engine import simulate_match
from tactical_manager.core.models import Fixture, Team
from tactical_manager.core.updates import apply_match_result


@dataclass
class Season:
    def __init__(self, teams: dict[str, Team], fixtures: list, user_team: str):
        self.teams = teams
        self.fixtures = fixtures
        self.user_team = user_team
        self.current_round = 1
        self.history = []

    def play_next_fixture(
            self,
            user_plan: str = "balanced",
            user_tactic: Tactic | None = None,
    ):
        for fixture in self.fixtures:
            if not fixture.played:
                home = self.teams[fixture.home]
                away = self.teams[fixture.away]

                # Determine which team is controlled by the user
                if home.name == self.user_team:
                    user_side = "home"
                elif away.name == self.user_team:
                    user_side = "away"
                else:
                    user_side = None  # AI vs AI match (future use)

                # Apply tactic to correct team
                if user_tactic is not None:
                    if user_side == "home":
                        home.tactic = user_tactic
                    elif user_side == "away":
                        away.tactic = user_tactic

                # Apply plans correctly
                home_plan = user_plan if user_side == "home" else "balanced"
                away_plan = user_plan if user_side == "away" else "balanced"

                result = simulate_match(
                    home,
                    away,
                    home_plan=home_plan,
                    away_plan=away_plan,
                )

                apply_match_result(home, away, result)

                fixture.played = True
                fixture.result = result
                self.history.append(
                    f"{fixture.home} {result.stats.home_goals}-{result.stats.away_goals} {fixture.away}"
                )

                return fixture

        return None

    def table(self) -> list[Team]:
        return sorted(
            self.teams.values(),
            key=lambda t: (t.points, t.goal_difference(), t.goals_for),
            reverse=True,
        )


def create_double_round_robin(team_names: list[str]) -> list[Fixture]:
    fixtures: list[Fixture] = []
    for i, home in enumerate(team_names):
        for j, away in enumerate(team_names):
            if i == j:
                continue
            fixtures.append(Fixture(home=home, away=away))
    return fixtures
