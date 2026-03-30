from __future__ import annotations

from dataclasses import dataclass, field
from tactical_manager.core.match_engine import simulate_match
from tactical_manager.core.models import Fixture, Team, Club
from tactical_manager.core.updates import apply_match_result


from dataclasses import dataclass, field

from tactical_manager.core.match_engine import simulate_match
from tactical_manager.core.models import Club, Tactic


@dataclass
class Season:
    clubs: dict[str, Club]
    fixtures: list
    user_club: str
    current_round: int = 1
    history: list[str] = field(default_factory=list)

    def play_next_fixture(
        self,
        user_plan: str = "balanced",
        user_tactic: Tactic | None = None,
    ):
        for fixture in self.fixtures:
            if fixture.played:
                continue

            home_club = self.clubs[fixture.home]
            away_club = self.clubs[fixture.away]

            home = home_club.team
            away = away_club.team

            # Determine which club is controlled by the user
            if fixture.home == self.user_club:
                user_side = "home"
            elif fixture.away == self.user_club:
                user_side = "away"
            else:
                user_side = None

            # Apply tactic to the correct team
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

def create_double_round_robin(team_names: list[str]) -> list[Fixture]:
    fixtures: list[Fixture] = []
    for i, home in enumerate(team_names):
        for j, away in enumerate(team_names):
            if i == j:
                continue
            fixtures.append(Fixture(home=home, away=away))
    return fixtures

def apply_match_result(home, away, result) -> None:
    home.goals_for += result.stats.home_goals
    home.goals_against += result.stats.away_goals
    away.goals_for += result.stats.away_goals
    away.goals_against += result.stats.home_goals

    if result.stats.home_goals > result.stats.away_goals:
        home.points += 3
        home.wins += 1
        away.losses += 1
    elif result.stats.home_goals < result.stats.away_goals:
        away.points += 3
        away.wins += 1
        home.losses += 1
    else:
        home.points += 1
        away.points += 1
        home.draws += 1
        away.draws += 1

    home.played += 1
    away.played += 1