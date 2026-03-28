
from __future__ import annotations

import math
import random
from tactical_manager.core.models import MatchResult, MatchStats, Team
from tactical_manager.core.tactics import compute_team_profile, pick_starting_xi


def logistic(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def clamp(x: float, low: float, high: float) -> float:
    return max(low, min(high, x))


def simulate_match(home: Team, away: Team, seed: int | None = None) -> MatchResult:
    if seed is not None:
        random.seed(seed)

    home_xi = pick_starting_xi(home)
    away_xi = pick_starting_xi(away)

    hp = compute_team_profile(home, home_xi)
    ap = compute_team_profile(away, away_xi)

    stats = MatchStats()
    events: list[str] = []

    for minute in range(0, 90, 5):
        home_possession_share = logistic(
            -0.2 + 0.025 * hp["build_up"] - 0.02 * ap["pressing"]
        )

        total_possessions = 6
        home_possessions = sum(1 for _ in range(total_possessions) if random.random() < home_possession_share)
        away_possessions = total_possessions - home_possessions

        for _ in range(home_possessions):
            shot, xg, goal = simulate_possession(hp, ap)
            if shot:
                stats.home_shots += 1
                stats.home_xg += xg
            if goal:
                stats.home_goals += 1
                events.append(f"{minute + random.randint(1, 5)}' {home.name} scored")

        for _ in range(away_possessions):
            shot, xg, goal = simulate_possession(ap, hp)
            if shot:
                stats.away_shots += 1
                stats.away_xg += xg
            if goal:
                stats.away_goals += 1
                events.append(f"{minute + random.randint(1, 5)}' {away.name} scored")

    return MatchResult(
        home_team=home.name,
        away_team=away.name,
        stats=stats,
        events=sorted(events, key=lambda e: int(e.split("'")[0])),
    )


def simulate_possession(attacking: dict[str, float], defending: dict[str, float]) -> tuple[bool, float, bool]:
    p_progress = logistic(
        -1.0 + 0.03 * attacking["build_up"] - 0.025 * defending["pressing"]
    )
    if random.random() > p_progress:
        return False, 0.0, False

    p_chance = logistic(
        -1.1
        + 0.03 * attacking["chance_creation"]
        + 0.02 * attacking["transition"]
        - 0.03 * defending["defense"]
    )
    if random.random() > p_chance:
        return False, 0.0, False

    xg = clamp(
        0.05
        + 0.0035 * attacking["chance_creation"]
        + 0.0025 * attacking["finishing"]
        - 0.0025 * defending["defense"],
        0.02,
        0.45,
    )

    goal = random.random() < xg
    return True, xg, goal