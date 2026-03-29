# tactical_manager/core/match_logic.py
from __future__ import annotations

import math
import random
from typing import Any

from tactical_manager.core.models import Team

Profile = dict[str, float]


def logistic(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def clamp(x: float, low: float, high: float) -> float:
    return max(low, min(high, x))


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


def compute_possession_share(home_profile: Profile, away_profile: Profile) -> float:
    """
    Returns the home team's possession share for one slice.
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
        "scorer": None,
    }


def derive_live_profile(
    base_profile: Profile,
    team: Team,
    minute: int,
    goals_for: int,
    goals_against: int,
) -> Profile:
    """
    Create a temporary in-match profile for the current 5-minute slice.
    """
    live = dict(base_profile)

    intensity = (team.tactic.pressing + team.tactic.tempo) / 200.0
    fatigue_drop = (minute / 90.0) * (0.08 + 0.12 * intensity)
    fatigue_factor = max(0.82, 1.0 - fatigue_drop)

    live["build_up"] *= fatigue_factor
    live["chance_creation"] *= fatigue_factor
    live["transition"] *= fatigue_factor
    live["pressing"] *= fatigue_factor
    live["midfield_control"] *= fatigue_factor
    live["compactness"] *= fatigue_factor
    live["defense"] *= fatigue_factor
    live["finishing"] *= max(0.88, fatigue_factor + 0.03)

    goal_diff = goals_for - goals_against

    if goal_diff < 0:
        attack_boost = min(6.0, 2.5 * abs(goal_diff))
        defense_penalty = min(4.0, 1.5 * abs(goal_diff))

        live["chance_creation"] += attack_boost
        live["transition"] += attack_boost * 0.8
        live["build_up"] += attack_boost * 0.4
        live["pressing"] += attack_boost * 0.5

        live["defense"] -= defense_penalty
        live["compactness"] -= defense_penalty

    elif goal_diff > 0:
        attack_penalty = min(4.0, 1.5 * goal_diff)
        defense_boost = min(5.0, 2.0 * goal_diff)

        live["chance_creation"] -= attack_penalty
        live["transition"] -= attack_penalty * 0.5
        live["defense"] += defense_boost
        live["compactness"] += defense_boost
        live["build_up"] -= attack_penalty * 0.3

    for key in live:
        live[key] = clamp(live[key], 1.0, 99.0)

    return live


def apply_halftime_adjustment(
    profile: Profile,
    team: Team,
    goals_for: int,
    goals_against: int,
    minute: int,
) -> tuple[Profile, str | None]:
    """
    Apply a simple AI halftime tactical adjustment.
    """
    if minute < 45:
        return profile, None

    adjusted = dict(profile)
    goal_diff = goals_for - goals_against

    if goal_diff < 0:
        adjusted["pressing"] += 6.0
        adjusted["chance_creation"] += 8.0
        adjusted["transition"] += 6.0
        adjusted["build_up"] += 3.0
        adjusted["defense"] -= 4.0
        adjusted["compactness"] -= 4.0

        for key in adjusted:
            adjusted[key] = clamp(adjusted[key], 1.0, 99.0)

        return adjusted, f"46' {team.name} switch to a more attacking approach"

    if goal_diff > 0:
        adjusted["pressing"] -= 2.0
        adjusted["chance_creation"] -= 4.0
        adjusted["transition"] -= 3.0
        adjusted["defense"] += 5.0
        adjusted["compactness"] += 5.0

        for key in adjusted:
            adjusted[key] = clamp(adjusted[key], 1.0, 99.0)

        return adjusted, f"46' {team.name} tighten up defensively"

    return adjusted, None


def apply_match_plan(profile: Profile, plan: str) -> tuple[Profile, str | None]:
    """
    Apply a user- or AI-selected match approach on top of the base profile.
    """
    adjusted = dict(profile)

    if plan == "defensive":
        adjusted["pressing"] -= 3.0
        adjusted["chance_creation"] -= 5.0
        adjusted["transition"] -= 3.0
        adjusted["defense"] += 6.0
        adjusted["compactness"] += 6.0
        adjusted["build_up"] -= 1.5

        for key in adjusted:
            adjusted[key] = clamp(adjusted[key], 1.0, 99.0)

        return adjusted, "set up more defensively"

    if plan == "attacking":
        adjusted["pressing"] += 4.0
        adjusted["chance_creation"] += 7.0
        adjusted["transition"] += 5.0
        adjusted["build_up"] += 2.0
        adjusted["defense"] -= 4.0
        adjusted["compactness"] -= 4.0

        for key in adjusted:
            adjusted[key] = clamp(adjusted[key], 1.0, 99.0)

        return adjusted, "set up more aggressively"

    return adjusted, None