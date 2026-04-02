from __future__ import annotations

from tactical_manager.core.models import MatchResult


def analyze_match(result: MatchResult, is_home: bool = True) -> list[str]:
    """
    High-level match analysis for the user's team.
    Returns a list of human-readable insights.
    """
    data = extract_team_view(result, is_home)

    insights: list[str] = []

    insights += analyze_chance_quality(data)
    insights += analyze_finishing(data)
    insights += analyze_attack(data)
    insights += analyze_defense(data)
    insights += analyze_match_result(data)

    if not insights:
        insights.append("A balanced match with no clear patterns.")

    return insights


# -------------------------------------------------------------------
# DATA LAYER
# -------------------------------------------------------------------

def extract_team_view(result: MatchResult, is_home: bool) -> dict:
    stats = result.stats

    if is_home:
        return {
            "xg_for": stats.home_xg,
            "xg_against": stats.away_xg,
            "goals_for": stats.home_goals,
            "goals_against": stats.away_goals,
            "shots_for": stats.home_shots,
            "shots_against": stats.away_shots,
        }
    else:
        return {
            "xg_for": stats.away_xg,
            "xg_against": stats.home_xg,
            "goals_for": stats.away_goals,
            "goals_against": stats.home_goals,
            "shots_for": stats.away_shots,
            "shots_against": stats.home_shots,
        }


# -------------------------------------------------------------------
# ANALYSIS RULES
# -------------------------------------------------------------------

def analyze_chance_quality(d: dict) -> list[str]:
    insights = []

    if d["xg_for"] > d["xg_against"] + 0.5:
        insights.append("You created significantly better chances than your opponent.")
    elif d["xg_for"] < d["xg_against"] - 0.5:
        insights.append("Your opponent created better chances.")

    return insights


def analyze_finishing(d: dict) -> list[str]:
    insights = []

    if d["goals_for"] > d["xg_for"] + 0.5:
        insights.append("You were very clinical in front of goal.")
    elif d["goals_for"] < d["xg_for"] - 0.5:
        insights.append("You were wasteful with your chances.")

    return insights


def analyze_attack(d: dict) -> list[str]:
    insights = []

    if d["shots_for"] < 5:
        insights.append("Your attack produced too few shots.")
    elif d["shots_for"] > 12:
        insights.append("Your attack generated constant pressure.")

    if d["xg_for"] < 1.0:
        insights.append("Your build-up play was ineffective.")

    return insights


def analyze_defense(d: dict) -> list[str]:
    insights = []

    if d["shots_against"] > 10:
        insights.append("Your defense allowed too many shots.")

    if d["xg_against"] > 2.0:
        insights.append("You allowed high-quality chances.")

    return insights


def analyze_match_result(d: dict) -> list[str]:
    insights = []

    if d["goals_for"] > d["goals_against"]:
        if d["xg_for"] < d["xg_against"]:
            insights.append("You won despite being second best.")
        else:
            insights.append("A deserved victory.")

    elif d["goals_for"] < d["goals_against"]:
        if d["xg_for"] > d["xg_against"]:
            insights.append("You were unlucky to lose.")
        else:
            insights.append("A deserved defeat.")

    else:
        if abs(d["xg_for"] - d["xg_against"]) > 0.7:
            insights.append("The draw does not reflect the balance of chances.")
        else:
            insights.append("A fair draw.")

    return insights


def compute_player_ratings(result: MatchResult, home_xi: list, away_xi: list) -> dict:
    ratings = {}

    stats = result.stats

    # team performance baseline
    home_team_factor = team_performance_factor(
        stats.home_goals, stats.away_goals, stats.home_xg, stats.away_xg
    )
    away_team_factor = team_performance_factor(
        stats.away_goals, stats.home_goals, stats.away_xg, stats.home_xg
    )

    # initialize all players
    for p in home_xi:
        ratings[p.name] = 50 + home_team_factor

    for p in away_xi:
        ratings[p.name] = 50 + away_team_factor

    # apply event-based contributions
    apply_event_contributions(ratings, result.events)

    # clamp
    for k in ratings:
        ratings[k] = max(0, min(100, round(ratings[k], 1)))

    return ratings


def team_performance_factor(goals_for, goals_against, xg_for, xg_against):
    factor = 0

    # result impact
    if goals_for > goals_against:
        factor += 5
    elif goals_for < goals_against:
        factor -= 5

    # xG performance
    if xg_for > xg_against + 0.5:
        factor += 3
    elif xg_for < xg_against - 0.5:
        factor -= 3

    return factor


def apply_event_contributions(ratings: dict, events: list[str]):
    for e in events:
        if "GOAL" in e:
            try:
                # scorer
                parts = e.split(":")[1].strip()
                scorer = parts.split("(")[0].strip()

                if scorer in ratings:
                    ratings[scorer] += 8

                # assist
                if "assist:" in e:
                    assist_part = e.split("assist:")[1]
                    assister = assist_part.split(",")[0].strip()

                    if assister in ratings:
                        ratings[assister] += 5

            except Exception:
                continue