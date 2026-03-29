from __future__ import annotations

import random

from tactical_manager.core.events import (
    event_minute_key,
    pick_assister,
    pick_goal_type,
    pick_scorer,
)
from tactical_manager.core.match_logic import (
    Profile,
    apply_halftime_adjustment,
    apply_match_plan,
    compute_possession_share,
    derive_live_profile,
    simulate_possession,
    validate_profile,
)
from tactical_manager.core.models import MatchResult, MatchStats, Team
from tactical_manager.core.tactics import compute_team_profile, pick_starting_xi


def simulate_match(
    home: Team,
    away: Team,
    seed: int | None = None,
    home_plan: str = "balanced",
    away_plan: str = "balanced",
) -> MatchResult:
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
        events=sorted(events, key=event_minute_key),
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
    xi: list,
    rng: random.Random,
) -> None:
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