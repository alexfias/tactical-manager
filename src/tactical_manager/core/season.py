from __future__ import annotations

from dataclasses import dataclass, field
from tactical_manager.core.match_engine import simulate_match
from tactical_manager.core.models import Fixture, Team
from tactical_manager.core.updates import apply_match_result


@dataclass
class Season:
    teams: dict[str, Team]
    fixtures: list[Fixture]
    current_round: int = 0
    history: list[str] = field(default_factory=list)

    def play_next_fixture(self, user_plan: str = "balanced"):
        for fixture in self.fixtures:
            if not fixture.played:
                home = self.teams[fixture.home]
                away = self.teams[fixture.away]

                result = simulate_match(
                    home,
                    away,
                    home_plan=user_plan,
                    away_plan="balanced",
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
