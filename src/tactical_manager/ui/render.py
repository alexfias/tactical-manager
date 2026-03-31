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

def render_squad(players: list) -> str:
    if not players:
        return "No players to show."

    lines = []
    lines.append(
        f"{'Name':<12} {'Pos':<5} {'Fit':>5} {'Fat':>5} {'Mor':>5} {'Fam':>5} {'Inj':>5}"
    )
    lines.append("-" * 50)

    for p in players:
        inj = "X" if p.injured else ""

        lines.append(
            f"{p.name:<12} {p.position:<5} "
            f"{p.fitness:>5.1f} {p.fatigue:>5.1f} "
            f"{p.morale:>5.1f} {p.familiarity:>5.1f} "
            f"{inj:>5}"
        )
    return "\n".join(lines)


from tactical_manager.core.models import Club


def render_club_overview(club: Club) -> str:
    lines = [
        f"=== {club.identity.name} ===",
        f"City: {club.identity.city or '-'}",
        f"Founded: {club.identity.founded if club.identity.founded is not None else '-'}",
        f"Club size: {club.identity.club_size}",
        f"Reputation: {club.identity.reputation:.1f}",
        "",
        "Finances",
        f"  Balance: €{club.finance.balance:,}",
        f"  Transfer budget: €{club.finance.transfer_budget:,}",
        f"  Weekly wages: €{club.finance.weekly_wages:,}",
        f"  Wage budget: €{club.finance.wage_budget:,}",
        f"  Sponsorship income: €{club.finance.sponsorship_income:,}",
        f"  Matchday base income: €{club.finance.matchday_base_income:,}",
        "",
        "Infrastructure",
        f"  Stadium capacity: {club.infrastructure.stadium_capacity:,}",
        f"  Ticket price: €{club.infrastructure.ticket_price}",
        f"  Training level: {club.infrastructure.training_level}",
        f"  Youth level: {club.infrastructure.youth_level}",
        "",
        "Support",
        f"  Fan confidence: {club.support.fan_confidence:.1f}",
        f"  Fan base: {club.support.fan_base:,}",
        "",
        "Board",
        f"  Target finish: {club.board.target_finish}",
        f"  Max wage ratio: {club.board.max_wage_ratio:.2f}",
        f"  Philosophy: {club.board.philosophy}",
        "",
        f"Squad size: {len(club.team.squad)}",
    ]
    return "\n".join(lines)