from __future__ import annotations

import math
import random
from tactical_manager.core.models import MatchResult, Team
from tactical_manager.core.tactics import pick_starting_xi


def logistic(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def clamp(x: float, low: float, high: float) -> float:
    return max(low, min(high, x))


def apply_match_result(home: Team, away: Team, result: MatchResult) -> None:
    hg = result.stats.home_goals
    ag = result.stats.away_goals

    home.played += 1
    away.played += 1

    home.goals_for += hg
    home.goals_against += ag
    away.goals_for += ag
    away.goals_against += hg

    if hg > ag:
        home.points += 3
    elif ag > hg:
        away.points += 3
    else:
        home.points += 1
        away.points += 1

    update_player_states(home, hg, ag)
    update_player_states(away, ag, hg)


def update_player_states(team: Team, goals_for: int, goals_against: int) -> None:
    xi = pick_starting_xi(team)

    result_bonus = 4 if goals_for > goals_against else 1 if goals_for == goals_against else -4
    intensity = (
        0.35 * team.tactic.pressing +
        0.20 * team.tactic.tempo +
        0.15 * team.tactic.directness
    ) / 100.0

    for player in team.squad:
        if player in xi:
            fatigue_gain = 8.0 + 8.0 * intensity - 0.05 * player.stamina
            player.fatigue = clamp(player.fatigue + fatigue_gain, 0.0, 100.0)
            player.morale = clamp(player.morale + result_bonus, 0.0, 100.0)
            player.familiarity = clamp(player.familiarity + 1.5, 0.0, 100.0)
            player.fitness = clamp(player.fitness - 0.2 * fatigue_gain + 1.0, 60.0, 100.0)

            injury_prob = logistic(
                -5.2
                + 0.045 * player.fatigue
                + 0.03 * player.injury_proneness
                + 0.02 * team.tactic.pressing
                - 0.02 * player.fitness
            )
            if random.random() < injury_prob:
                player.injured = True
        else:
            player.fatigue = clamp(player.fatigue - 6.0, 0.0, 100.0)
            player.morale = clamp(player.morale - 0.5, 0.0, 100.0)

    for player in team.squad:
        player.fatigue = clamp(player.fatigue - 3.0, 0.0, 100.0)
        if not player.injured:
            player.fitness = clamp(player.fitness + 1.0, 60.0, 100.0)
