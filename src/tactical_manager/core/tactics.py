from __future__ import annotations

from typing import Dict, List
from tactical_manager.core.models import Player, Team


def _avg(values: List[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def pick_starting_xi(team: Team) -> List[Player]:
    players = team.available_players()

    gks = [p for p in players if p.position == "GK"]
    defs = [p for p in players if p.position == "DEF"]
    mids = [p for p in players if p.position == "MID"]
    atts = [p for p in players if p.position == "ATT"]

    gks = sorted(gks, key=lambda p: p.effective("positioning") + p.effective("defending"), reverse=True)
    defs = sorted(defs, key=lambda p: p.effective("defending") + p.effective("positioning"), reverse=True)
    mids = sorted(mids, key=lambda p: p.effective("passing") + p.effective("technique"), reverse=True)
    atts = sorted(atts, key=lambda p: p.effective("finishing") + p.effective("pace"), reverse=True)

    xi = gks[:1] + defs[:4] + mids[:3] + atts[:3]
    return xi[:11]


def compute_team_profile(team: Team, xi: List[Player]) -> Dict[str, float]:
    defs = [p for p in xi if p.position == "DEF"]
    mids = [p for p in xi if p.position == "MID"]
    atts = [p for p in xi if p.position == "ATT"]

    build_up = (
        0.45 * _avg([p.effective("passing") for p in defs + mids]) +
        0.25 * _avg([p.effective("technique") for p in mids]) +
        0.15 * team.tactic.tempo +
        0.15 * (100 - team.tactic.directness)
    )

    chance_creation = (
        0.35 * _avg([p.effective("passing") for p in mids + atts]) +
        0.25 * _avg([p.effective("technique") for p in mids + atts]) +
        0.20 * team.tactic.width +
        0.20 * team.tactic.tempo
    )

    finishing = _avg([p.effective("finishing") for p in atts])

    pressing = (
        0.35 * _avg([p.effective("work_rate") for p in mids + atts]) +
        0.25 * _avg([p.effective("stamina") for p in mids + atts]) +
        0.20 * _avg([p.effective("pace") for p in atts]) +
        0.20 * team.tactic.pressing
    )

    defense = (
        0.40 * _avg([p.effective("defending") for p in defs]) +
        0.25 * _avg([p.effective("positioning") for p in defs + mids]) +
        0.20 * (100 - team.tactic.defensive_line) +
        0.15 * _avg([p.effective("pace") for p in defs])
    )

    transition = (
        0.40 * _avg([p.effective("pace") for p in atts]) +
        0.25 * _avg([p.effective("finishing") for p in atts]) +
        0.20 * team.tactic.directness +
        0.15 * team.tactic.tempo
    )

    energy = 100 - _avg([p.fatigue for p in xi])

    return {
        "build_up": build_up,
        "chance_creation": chance_creation,
        "finishing": finishing,
        "pressing": pressing,
        "defense": defense,
        "transition": transition,
        "energy": energy,
    }
