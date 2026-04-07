from __future__ import annotations

from tactical_manager.core.models import Club, Stadium, StadiumSection


CAPACITY_EXPANSION_STEP = 1000
BASE_EXPANSION_COST = 250_000
EXPANSION_COST_PER_LEVEL = 125_000

BASE_ROOF_COST = 400_000
ROOF_COST_PER_1000_CAPACITY = 75_000

BASE_QUALITY_COST = 150_000
QUALITY_COST_PER_LEVEL = 100_000
MAX_QUALITY = 5


def get_section(stadium: Stadium, section_name: str) -> StadiumSection | None:
    for section in stadium.sections:
        if section.name == section_name:
            return section
    return None


def total_capacity(stadium: Stadium) -> int:
    return sum(section.capacity for section in stadium.sections)


def covered_capacity(stadium: Stadium) -> int:
    return sum(section.capacity for section in stadium.sections if section.covered)


def average_quality(stadium: Stadium) -> float:
    if not stadium.sections:
        return 0.0
    return sum(section.quality for section in stadium.sections) / len(stadium.sections)


def expansion_cost(section: StadiumSection) -> int:
    return BASE_EXPANSION_COST + section.expansion_level * EXPANSION_COST_PER_LEVEL


def roof_cost(section: StadiumSection) -> int:
    capacity_units = max(1, section.capacity // 1000)
    return BASE_ROOF_COST + capacity_units * ROOF_COST_PER_1000_CAPACITY


def quality_upgrade_cost(section: StadiumSection) -> int:
    return BASE_QUALITY_COST + (section.quality - 1) * QUALITY_COST_PER_LEVEL


def can_afford(club: Club, amount: int) -> bool:
    return club.finance.cash >= amount


def can_expand(section: StadiumSection) -> bool:
    return True


def can_add_roof(section: StadiumSection) -> bool:
    return not section.covered


def can_improve_quality(section: StadiumSection) -> bool:
    return section.quality < MAX_QUALITY


def expand_section(club: Club, section_name: str) -> bool:
    section = get_section(club.stadium, section_name)
    if section is None:
        return False

    if not can_expand(section):
        return False

    cost = expansion_cost(section)
    if not can_afford(club, cost):
        return False

    club.finance.cash -= cost
    section.capacity += CAPACITY_EXPANSION_STEP
    section.expansion_level += 1
    return True


def add_roof(club: Club, section_name: str) -> bool:
    section = get_section(club.stadium, section_name)
    if section is None:
        return False

    if not can_add_roof(section):
        return False

    cost = roof_cost(section)
    if not can_afford(club, cost):
        return False

    club.finance.cash -= cost
    section.covered = True
    return True


def improve_section_quality(club: Club, section_name: str) -> bool:
    section = get_section(club.stadium, section_name)
    if section is None:
        return False

    if not can_improve_quality(section):
        return False

    cost = quality_upgrade_cost(section)
    if not can_afford(club, cost):
        return False

    club.finance.cash -= cost
    section.quality += 1
    return True

def stadium_summary(stadium: Stadium) -> dict[str, int | float]:
    return {
        "total_capacity": total_capacity(stadium),
        "covered_capacity": covered_capacity(stadium),
        "average_quality": average_quality(stadium),
    }