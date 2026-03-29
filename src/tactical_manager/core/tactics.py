from __future__ import annotations

from tactical_manager.core.models import Player, Team

def clamp(x: float, low: float, high: float) -> float:
    return max(low, min(high, x))


def avg(values: list[float]) -> float:
    if not values:
        return 50.0
    return sum(values) / len(values)


def by_position(players: list[Player], position: str) -> list[Player]:
    return [p for p in players if p.position == position]


def pick_starting_xi(team: Team) -> list[Player]:
    """
    Simple v1 lineup selection:
    1 GK, 4 DEF, 3 MID, 3 ATT if possible.
    Fills remaining slots from available players if needed.
    """
    available = team.available_players()

    gks = by_position(available, "GK")
    defs = by_position(available, "DEF")
    mids = by_position(available, "MID")
    atts = by_position(available, "ATT")

    xi: list[Player] = []

    if gks:
        xi.append(gks[0])

    xi.extend(defs[:4])
    xi.extend(mids[:3])
    xi.extend(atts[:3])

    used_ids = {id(p) for p in xi}
    for player in available:
        if len(xi) >= 11:
            break
        if id(player) not in used_ids:
            xi.append(player)
            used_ids.add(id(player))

    return xi[:11]


def compute_team_profile(team: Team, xi: list[Player]) -> dict[str, float]:
    """
    Returns the profile contract expected by match_engine.py.
    All values are roughly on a 0..100 scale.
    """
    tactic = team.tactic

    gks = by_position(xi, "GK")
    defs = by_position(xi, "DEF")
    mids = by_position(xi, "MID")
    atts = by_position(xi, "ATT")

    # Fallbacks so the engine never crashes just because a line is thin.
    gk = gks[0] if gks else None

    def eff(players: list[Player], attr: str, fallback: float = 50.0) -> float:
        if not players:
            return fallback
        return avg([p.effective(attr) for p in players])

    build_up = (
        0.35 * eff(defs + mids, "passing")
        + 0.25 * eff(defs + mids, "technique")
        + 0.20 * eff(defs + mids, "positioning")
        + 0.10 * tactic.tempo
        + 0.10 * (100.0 - abs(tactic.directness - 50.0))
    )

    pressing = (
        0.35 * eff(defs + mids + atts, "work_rate")
        + 0.25 * eff(defs + mids + atts, "stamina")
        + 0.40 * tactic.pressing
    )

    chance_creation = (
        0.30 * eff(mids + atts, "passing")
        + 0.30 * eff(mids + atts, "technique")
        + 0.20 * eff(mids + atts, "positioning")
        + 0.10 * tactic.width
        + 0.10 * tactic.tempo
    )

    transition = (
        0.35 * eff(mids + atts, "pace")
        + 0.25 * eff(mids + atts, "work_rate")
        + 0.20 * tactic.directness
        + 0.20 * tactic.tempo
    )

    defense = (
        0.45 * eff(defs + mids, "defending")
        + 0.30 * eff(defs + mids, "positioning")
        + 0.15 * eff(defs + mids, "stamina")
        + 0.10 * (100.0 - abs(tactic.defensive_line - 50.0))
    )

    finishing = (
        0.55 * eff(atts + mids[:1], "finishing")
        + 0.25 * eff(atts + mids[:1], "technique")
        + 0.20 * eff(atts + mids[:1], "positioning")
    )

    midfield_control = (
        0.35 * eff(mids, "passing")
        + 0.25 * eff(mids, "technique")
        + 0.20 * eff(mids, "positioning")
        + 0.10 * eff(mids, "work_rate")
        + 0.10 * tactic.tempo
    )

    compactness = (
        0.35 * eff(defs + mids, "defending")
        + 0.25 * eff(defs + mids, "positioning")
        + 0.15 * eff(defs + mids, "work_rate")
        + 0.15 * (100.0 - abs(tactic.width - 50.0))
        + 0.10 * (100.0 - abs(tactic.defensive_line - 50.0))
    )

    # Temporary v1 GK approximation since Player has no dedicated gk stat yet.
    goalkeeping = (
        0.50 * (gk.effective("positioning") if gk else 40.0)
        + 0.20 * (gk.effective("technique") if gk else 40.0)
        + 0.20 * (gk.effective("defending") if gk else 40.0)
        + 0.10 * (gk.effective("passing") if gk else 40.0)
    )

    profile = {
        "build_up": clamp(build_up, 1.0, 99.0),
        "pressing": clamp(pressing, 1.0, 99.0),
        "chance_creation": clamp(chance_creation, 1.0, 99.0),
        "transition": clamp(transition, 1.0, 99.0),
        "defense": clamp(defense, 1.0, 99.0),
        "finishing": clamp(finishing, 1.0, 99.0),
        "midfield_control": clamp(midfield_control, 1.0, 99.0),
        "compactness": clamp(compactness, 1.0, 99.0),
        "goalkeeping": clamp(goalkeeping, 1.0, 99.0),
    }

    return profile