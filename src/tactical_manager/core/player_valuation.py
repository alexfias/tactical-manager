from __future__ import annotations

from tactical_manager.core.models import Player


ATTRIBUTE_WEIGHTS: dict[str, float] = {
    # technical
    "passing": 1.0,
    "first_touch": 0.8,
    "technique": 1.0,
    "dribbling": 0.8,
    "finishing": 1.0,
    "long_shots": 0.4,
    "tackling": 1.0,
    "heading": 0.5,
    "crossing": 0.5,

    # mental / tactical
    "positioning": 1.0,
    "vision": 0.8,
    "decision_making": 1.0,
    "anticipation": 0.8,
    "composure": 0.8,
    "concentration": 0.6,
    "work_rate": 0.7,
    "discipline": 0.3,
    "aggression": 0.3,

    # physical
    "pace": 0.9,
    "acceleration": 0.7,
    "agility": 0.6,
    "strength": 0.6,
    "stamina": 0.7,
    "jumping": 0.4,
}


def clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def current_ability(player: Player) -> float:
    """
    Compute a general current ability score on roughly a 0-100 scale.

    For now this is a position-agnostic weighted average of the player's
    football attributes. Later this can be made position-specific.
    """
    total_weight = sum(ATTRIBUTE_WEIGHTS.values())
    if total_weight <= 0:
        return 0.0

    weighted_sum = 0.0
    for attr_name, weight in ATTRIBUTE_WEIGHTS.items():
        value = float(getattr(player, attr_name, 50.0))
        weighted_sum += value * weight

    ability = weighted_sum / total_weight
    return clamp(ability, 0.0, 100.0)


def _age_factor(age: int) -> float:
    if age <= 18:
        return 1.35
    if age <= 20:
        return 1.28
    if age <= 22:
        return 1.18
    if age <= 25:
        return 1.08
    if age <= 28:
        return 1.00
    if age <= 31:
        return 0.86
    if age <= 34:
        return 0.68
    return 0.50


def _potential_factor(potential: float, ability: float) -> float:
    gap = max(0.0, potential - ability)
    return 1.0 + 0.012 * gap


def _contract_factor(contract_weeks: int) -> float:
    clamped_weeks = max(0, min(contract_weeks, 260))
    return 0.75 + 0.45 * (clamped_weeks / 260.0)


def _fitness_factor(fitness: float, fatigue: float, injured: bool) -> float:
    fitness_component = 0.85 + 0.20 * (clamp(fitness, 0.0, 100.0) / 100.0)
    fatigue_component = 1.05 - 0.15 * (clamp(fatigue, 0.0, 100.0) / 100.0)
    injury_component = 0.65 if injured else 1.0
    return fitness_component * fatigue_component * injury_component


def _morale_factor(morale: float, confidence: float, sharpness: float) -> float:
    morale_component = 0.92 + 0.12 * (clamp(morale, 0.0, 100.0) / 100.0)
    confidence_component = 0.95 + 0.10 * (clamp(confidence, 0.0, 100.0) / 100.0)
    sharpness_component = 0.94 + 0.12 * (clamp(sharpness, 0.0, 100.0) / 100.0)
    return morale_component * confidence_component * sharpness_component


def estimate_market_value(player: Player) -> int:
    """
    Estimate a player's market value as an integer currency amount.

    This is a stylized game formula, not a real-world football valuation model.
    It combines current ability, age, upside, contract security, and current
    condition into one value.
    """
    ability = current_ability(player)

    age_factor = _age_factor(player.age)
    potential_factor = _potential_factor(player.potential, ability)
    contract_factor = _contract_factor(player.contract_weeks)
    fitness_factor = _fitness_factor(player.fitness, player.fatigue, player.injured)
    morale_factor = _morale_factor(player.morale, player.confidence, player.sharpness)

    # Main scale:
    # quadratic in ability so top players become much more expensive
    base_value = 2500.0 * (ability ** 2)

    value = (
        base_value
        * age_factor
        * potential_factor
        * contract_factor
        * fitness_factor
        * morale_factor
    )

    return max(10000, int(round(value)))