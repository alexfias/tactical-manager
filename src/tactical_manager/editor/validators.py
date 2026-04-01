from __future__ import annotations

from tactical_manager.core.models import Club


VALID_POSITIONS = {"GK", "DEF", "MID", "ATT"}

PLAYER_RATING_FIELDS = [
    # technical
    "passing",
    "first_touch",
    "technique",
    "dribbling",
    "finishing",
    "long_shots",
    "tackling",
    "heading",
    "crossing",

    # mental / tactical
    "positioning",
    "vision",
    "decision_making",
    "anticipation",
    "composure",
    "concentration",
    "work_rate",
    "discipline",
    "aggression",

    # physical
    "pace",
    "acceleration",
    "agility",
    "strength",
    "stamina",
    "jumping",

    # dynamic / state
    "fatigue",
    "fitness",
    "morale",
    "familiarity",
    "confidence",
    "sharpness",
    "injury_proneness",

    # long-term
    "potential",
]


def validate_club(club: Club) -> list[str]:
    errors: list[str] = []

    if not club.identity.name.strip():
        errors.append("Club name must not be empty.")

    if not (0 <= club.identity.reputation <= 100):
        errors.append("Club reputation must be between 0 and 100.")

    if not club.team.squad:
        errors.append("Club must have at least one player in the squad.")

    gk_count = 0

    for i, player in enumerate(club.team.squad, start=1):
        player_name = player.name.strip() or f"#{i}"

        if not player.name.strip():
            errors.append(f"Player {i}: name must not be empty.")

        if player.position not in VALID_POSITIONS:
            errors.append(
                f"Player {player_name}: invalid position '{player.position}'."
            )

        if player.position == "GK":
            gk_count += 1

        for field_name in PLAYER_RATING_FIELDS:
            value = getattr(player, field_name, None)

            if value is None:
                errors.append(f"Player {player_name}: missing field '{field_name}'.")
                continue

            if not (0 <= value <= 100):
                errors.append(
                    f"Player {player_name}: {field_name} must be between 0 and 100."
                )

        if not (14 <= player.age <= 50):
            errors.append(f"Player {player_name}: age looks invalid ({player.age}).")

        if player.wage < 0:
            errors.append(f"Player {player_name}: wage must not be negative.")

        if player.contract_weeks < 0:
            errors.append(f"Player {player_name}: contract weeks must not be negative.")

    if gk_count == 0:
        errors.append("Squad should contain at least one goalkeeper.")

    return errors