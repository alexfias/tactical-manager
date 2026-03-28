from __future__ import annotations

import math
import random
from typing import Any

from tactical_manager.core.models import MatchResult, MatchStats, Team
from tactical_manager.core.tactics import compute_team_profile, pick_starting_xi


Profile = dict[str, float]


def logistic(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def clamp(x: float, low: float, high: float) -> float:
    return max(low, min(high, x))


def simulate_match(home: Team, away: Team, seed: int | None = None) -> MatchResult:
    """
    Minimal match engine v1.

    Flow:
    - pick starting XIs
    - compute static team profiles
    - simulate 18 time slices of 5 minutes each
    - each slice contains a small number of possessions
    - possessions may become shots, xG, and goals
    """
    rng = random.Random(seed)

    home_xi = pick_starting_xi(home)
    away_xi = pick_starting_xi(away)

    if len(home_xi) < 11:
        raise ValueError(f"{home.name} does not have a valid starting XI.")
    if len(away_xi) < 11:
        raise ValueError(f"{away.name} does not have a valid starting XI.")

    hp = compute_team_profile(home, home_xi)
    ap = compute_team_profile(away, away_xi)

    validate_profile(hp, team_name=home.name)
    validate_profile(ap, team_name=away.name)

    stats = MatchStats()
    events: list[str] = []

    for minute in range(0, 90, 5):
        home_possession_share = compute_possession_share(home_profile=hp, away_profile=ap)
        total_possessions = 6

        home_possessions = sum(
            1 for _ in range(total_possessions) if rng.random() < home_possession_share
        )
        away_possessions = total_possessions - home_possessions

        play_possessions(
            attacking_team=home,
            defending_team=away,
            attacking_profile=hp,
            defending_profile=ap,
            n_possessions=home_possessions,
            minute=minute,
            stats=stats,
            events=events,
            is_home=True,
            xi=home_xi,  # NEW
            rng=rng,
        )

        play_possessions(
            attacking_team=away,
            defending_team=home,
            attacking_profile=ap,
            defending_profile=hp,
            n_possessions=away_possessions,
            minute=minute,
            stats=stats,
            events=events,
            is_home=False,
            xi=home_xi,  # NEW
            rng=rng,
        )

    stats.home_xg = round(stats.home_xg, 2)
    stats.away_xg = round(stats.away_xg, 2)

    return MatchResult(
        home_team=home.name,
        away_team=away.name,
        stats=stats,
        events=sorted(events, key=_event_minute_key),
    )


def play_possessions(
    attacking_team: Team,
    defending_team: Team,
    attacking_profile: Profile,
    defending_profile: Profile,
    n_possessions: int,
    minute: int,
    stats: MatchStats,
    events: list[str],
    is_home: bool,
    xi: list,  # NEW
    rng: random.Random,
) -> None:
    """
    Simulate a batch of possessions for one team in one time slice.
    """
    for _ in range(n_possessions):
        outcome = simulate_possession(
            attacking=attacking_profile,
            defending=defending_profile,
            rng=rng,
        )

        if not outcome["shot"]:
            continue

        if is_home:
            stats.home_shots += 1
            stats.home_xg += outcome["xg"]
        else:
            stats.away_shots += 1
            stats.away_xg += outcome["xg"]

        if outcome["goal"]:
            event_minute = minute + rng.randint(1, 5)

            if is_home:
                stats.home_goals += 1
            else:
                stats.away_goals += 1

            scorer = pick_scorer(xi, rng)
            assister = pick_assister(xi, scorer.name, rng)
            goal_type = pick_goal_type(scorer, rng)

            if assister:
                events.append(
                    f"{event_minute}' GOAL {attacking_team.name}: {scorer.name} "
                    f"(assist: {assister}, {goal_type})"
                )
            else:
                events.append(
                    f"{event_minute}' GOAL {attacking_team.name}: {scorer.name} "
                    f"({goal_type})"
                )


def compute_possession_share(home_profile: Profile, away_profile: Profile) -> float:
    """
    Returns the home team's possession share for one slice.

    Home side gets a small fixed edge.
    """
    share = logistic(
        -0.10
        + 0.025 * home_profile["build_up"]
        - 0.020 * away_profile["pressing"]
        + 0.008 * home_profile["midfield_control"]
        - 0.008 * away_profile["midfield_control"]
    )
    return clamp(share, 0.25, 0.75)


def simulate_possession(
    attacking: Profile,
    defending: Profile,
    rng: random.Random,
) -> dict[str, Any]:
    """
    Simulate a single possession.

    Output keys:
    - shot: bool
    - xg: float
    - goal: bool
    - scorer: optional str (placeholder for future use)
    """
    p_progress = logistic(
        -1.0
        + 0.030 * attacking["build_up"]
        + 0.015 * attacking["transition"]
        - 0.025 * defending["pressing"]
        - 0.010 * defending["compactness"]
    )
    if rng.random() > p_progress:
        return {"shot": False, "xg": 0.0, "goal": False}

    p_chance = logistic(
        -1.1
        + 0.030 * attacking["chance_creation"]
        + 0.020 * attacking["transition"]
        - 0.030 * defending["defense"]
        - 0.010 * defending["compactness"]
    )
    if rng.random() > p_chance:
        return {"shot": False, "xg": 0.0, "goal": False}

    xg = clamp(
        0.05
        + 0.0035 * attacking["chance_creation"]
        + 0.0025 * attacking["finishing"]
        - 0.0025 * defending["defense"]
        - 0.0010 * defending["goalkeeping"],
        0.02,
        0.45,
    )

    goal = rng.random() < xg

    return {
        "shot": True,
        "xg": xg,
        "goal": goal,
        "scorer": None,  # future extension
    }


def validate_profile(profile: Profile, team_name: str) -> None:
    required_keys = {
        "build_up",
        "pressing",
        "chance_creation",
        "transition",
        "defense",
        "finishing",
        "midfield_control",
        "compactness",
        "goalkeeping",
    }

    missing = required_keys - set(profile.keys())
    if missing:
        missing_str = ", ".join(sorted(missing))
        raise ValueError(f"Profile for team '{team_name}' is missing keys: {missing_str}")


def _event_minute_key(event: str) -> int:
    try:
        return int(event.split("'")[0])
    except (IndexError, ValueError):
        return 999

def pick_scorer(xi, rng: random.Random):
    weighted = []

    for p in xi:
        if p.position == "ATT":
            weight = p.effective("finishing") * 1.5
        elif p.position == "MID":
            weight = p.effective("finishing")
        elif p.position == "DEF":
            weight = p.effective("finishing") * 0.3
        else:
            weight = 1

        weight = max(1, int(weight / 10))
        weighted.extend([p] * weight)

    return rng.choice(weighted)


def pick_assister(xi, scorer_name: str, rng: random.Random) -> str | None:
    candidates = [p for p in xi if p.name != scorer_name]

    if not candidates:
        return None

    weighted = []
    for p in candidates:
        weight = (
            0.4 * p.effective("passing")
            + 0.3 * p.effective("technique")
            + 0.3 * p.effective("positioning")
        )
        weight = max(1, int(weight / 10))
        weighted.extend([p] * weight)

    assister = rng.choice(weighted).name

    # Not every goal has an assist
    if rng.random() < 0.25:
        return None

    return assister

def pick_goal_type(scorer, rng: random.Random) -> str:
    header_score = (
        0.45 * scorer.effective("positioning")
        + 0.30 * scorer.effective("stamina")
        + 0.25 * scorer.effective("work_rate")
    )

    long_shot_score = (
        0.55 * scorer.effective("technique")
        + 0.45 * scorer.effective("finishing")
    )

    open_play_score = (
        0.35 * scorer.effective("finishing")
        + 0.25 * scorer.effective("positioning")
        + 0.20 * scorer.effective("pace")
        + 0.20 * scorer.effective("technique")
    )

    total = header_score + long_shot_score + open_play_score
    if total <= 0:
        return "open play"

    weights = [
        open_play_score / total,
        header_score / total,
        long_shot_score / total,
    ]

    return rng.choices(
        ["open play", "header", "long shot"],
        weights=weights,
    )[0]

