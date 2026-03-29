# tactical_manager/core/events.py
from __future__ import annotations

import random


def event_minute_key(event: str) -> int:
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