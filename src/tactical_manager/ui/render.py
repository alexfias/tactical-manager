from __future__ import annotations

from tactical_manager.core.models import MatchResult, Team


def render_table(teams: list[Team]) -> str:
    lines = []
    lines.append("Pos Team                  P   GF  GA  GD  Pts")
    lines.append("-" * 45)
    for i, team in enumerate(teams, start=1):
        lines.append(
            f"{i:>3} {team.name:<20} {team.played:>2}  {team.goals_for:>2}  {team.goals_against:>2}  {team.goal_difference():>3}  {team.points:>3}"
        )
    return "\n".join(lines)


def render_match(result: MatchResult) -> str:
    s = result.stats
    lines = [
        f"{result.home_team} {s.home_goals} - {s.away_goals} {result.away_team}",
        f"Shots: {s.home_shots} - {s.away_shots}",
        f"xG:    {s.home_xg:.2f} - {s.away_xg:.2f}",
        "Events:",
    ]
    if result.events:
        lines.extend(f"  {event}" for event in result.events)
    else:
        lines.append("  No major events recorded.")
    return "\n".join(lines)
