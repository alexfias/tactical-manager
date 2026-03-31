from __future__ import annotations

from tactical_manager.core.models import Club


VALID_POSITIONS = {"GK", "DEF", "MID", "ATT"}


def validate_club(club: Club) -> list[str]:
    errors: list[str] = []

    if not club.identity.name.strip():
        errors.append("Club name must not be empty.")

    if club.identity.reputation < 0 or club.identity.reputation > 100:
        errors.append("Club reputation must be between 0 and 100.")

    if not club.team.squad:
        errors.append("Club must have at least one player in the squad.")

    gk_count = 0
    for i, player in enumerate(club.team.squad, start=1):
        if not player.name.strip():
            errors.append(f"Player {i}: name must not be empty.")

        if player.position not in VALID_POSITIONS:
            errors.append(
                f"Player {player.name or i}: invalid position '{player.position}'."
            )

        if player.position == "GK":
            gk_count += 1

        numeric_fields = [
            ("attack", player.attack),
            ("defense", player.defense),
            ("passing", player.passing),
            ("stamina", player.stamina),
            ("morale", player.morale),
            ("form", player.form),
            ("potential", player.potential),
        ]
        for field_name, value in numeric_fields:
            if value < 0 or value > 100:
                errors.append(
                    f"Player {player.name}: {field_name} must be between 0 and 100."
                )

        if player.age < 14 or player.age > 50:
            errors.append(f"Player {player.name}: age looks invalid ({player.age}).")

        if player.wage < 0:
            errors.append(f"Player {player.name}: wage must not be negative.")

        if player.market_value < 0:
            errors.append(f"Player {player.name}: market value must not be negative.")

        if player.contract_weeks < 0:
            errors.append(f"Player {player.name}: contract weeks must not be negative.")

    if gk_count == 0:
        errors.append("Squad should contain at least one goalkeeper.")

    return errors