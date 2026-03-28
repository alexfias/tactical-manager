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


def simulate_match(
    home: Team,
    away: Team,
    seed: int | None = None,
    home_plan: str = "balanced",
    away_plan: str = "balanced",
) -> MatchResult:
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

    home_halftime_logged = False
    away_halftime_logged = False

    for minute in range(0, 90, 5):
        live_hp = derive_live_profile(
            base_profile=hp,
            team=home,
            minute=minute,
            goals_for=stats.home_goals,
            goals_against=stats.away_goals,
        )
        live_ap = derive_live_profile(
            base_profile=ap,
            team=away,
            minute=minute,
            goals_for=stats.away_goals,
            goals_against=stats.home_goals,
        )

        live_hp, _ = apply_match_plan(live_hp, home_plan)
        live_ap, _ = apply_match_plan(live_ap, away_plan)

        live_hp, home_ht_event = apply_halftime_adjustment(
            profile=live_hp,
            team=home,
            goals_for=stats.home_goals,
            goals_against=stats.away_goals,
            minute=minute,
        )
        live_ap, away_ht_event = apply_halftime_adjustment(
            profile=live_ap,
            team=away,
            goals_for=stats.away_goals,
            goals_against=stats.home_goals,
            minute=minute,
        )

        if home_ht_event and not home_halftime_logged:
            events.append(home_ht_event)
            home_halftime_logged = True

        if away_ht_event and not away_halftime_logged:
            events.append(away_ht_event)
            away_halftime_logged = True

        home_possession_share = compute_possession_share(
            home_profile=live_hp,
            away_profile=live_ap,
        )
        total_possessions = 6

        home_possessions = sum(
            1 for _ in range(total_possessions) if rng.random() < home_possession_share
        )
        away_possessions = total_possessions - home_possessions

        play_possessions(
            attacking_team=home,
            defending_team=away,
            attacking_profile=live_hp,
            defending_profile=live_ap,
            n_possessions=home_possessions,
            minute=minute,
            stats=stats,
            events=events,
            is_home=True,
            xi=home_xi,
            rng=rng,
        )

        play_possessions(
            attacking_team=away,
            defending_team=home,
            attacking_profile=live_ap,
            defending_profile=live_hp,
            n_possessions=away_possessions,
            minute=minute,
            stats=stats,
            events=events,
            is_home=False,
            xi=away_xi,
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

def derive_live_profile(
    base_profile: Profile,
    team: Team,
    minute: int,
    goals_for: int,
    goals_against: int,
) -> Profile:
    """
    Create a temporary in-match profile for the current 5-minute slice.

    Effects included in v1:
    - fatigue over time
    - stronger fatigue for high pressing / high tempo teams
    - score-state adaptation:
        * trailing teams attack more and defend a bit less
        * leading teams attack a bit less and defend a bit more
    """
    live = dict(base_profile)

    intensity = (team.tactic.pressing + team.tactic.tempo) / 200.0
    fatigue_drop = (minute / 90.0) * (0.08 + 0.12 * intensity)
    fatigue_factor = max(0.82, 1.0 - fatigue_drop)

    # General late-game drop
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
        # trailing team pushes harder
        attack_boost = min(6.0, 2.5 * abs(goal_diff))
        defense_penalty = min(4.0, 1.5 * abs(goal_diff))

        live["chance_creation"] += attack_boost
        live["transition"] += attack_boost * 0.8
        live["build_up"] += attack_boost * 0.4
        live["pressing"] += attack_boost * 0.5

        live["defense"] -= defense_penalty
        live["compactness"] -= defense_penalty

    elif goal_diff > 0:
        # leading team becomes a bit more conservative
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

    Only activates from 45' onward.
    Returns:
    - adjusted profile
    - optional event text describing the tactical change
    """
    if minute < 45:
        return profile, None

    adjusted = dict(profile)
    goal_diff = goals_for - goals_against

    if goal_diff < 0:
        # Trailing: push harder
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
        # Leading: become a bit more cautious
        adjusted["pressing"] -= 2.0
        adjusted["chance_creation"] -= 4.0
        adjusted["transition"] -= 3.0
        adjusted["defense"] += 5.0
        adjusted["compactness"] += 5.0

        for key in adjusted:
            adjusted[key] = clamp(adjusted[key], 1.0, 99.0)

        return adjusted, f"46' {team.name} tighten up defensively"

    # Level: no major change
    return adjusted, None

def apply_match_plan(profile: Profile, plan: str) -> tuple[Profile, str | None]:
    """
    Apply a user- or AI-selected match approach on top of the base profile.

    Plans:
    - defensive
    - balanced
    - attacking
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