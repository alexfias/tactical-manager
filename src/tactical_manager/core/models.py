
# Starter code

## `src/tactical_manager/core/models.py`

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Literal

MatchPlan = Literal["defensive", "balanced", "attacking"]


@dataclass
class Player:
    name: str
    position: str  # GK, DEF, MID, ATT

    passing: float
    technique: float
    finishing: float
    defending: float
    positioning: float
    pace: float
    stamina: float
    work_rate: float

    fatigue: float = 10.0
    fitness: float = 95.0
    morale: float = 70.0
    familiarity: float = 50.0
    injury_proneness: float = 20.0
    injured: bool = False

    def availability_multiplier(self) -> float:
        if self.injured:
            return 0.0

        fatigue_factor = max(0.0, 1.0 - self.fatigue / 140.0)
        fitness_factor = self.fitness / 100.0
        morale_factor = 0.8 + 0.4 * (self.morale / 100.0)
        familiarity_factor = 0.8 + 0.4 * (self.familiarity / 100.0)
        return max(0.0, fatigue_factor * fitness_factor * morale_factor * familiarity_factor)

    def effective(self, attribute: str) -> float:
        return getattr(self, attribute) * self.availability_multiplier()


@dataclass
class Tactic:
    formation: str = "4-4-2"

    mentality: float = 50.0      # attacking vs defensive
    pressing: float = 50.0       # pressing intensity
    tempo: float = 50.0          # speed of play
    width: float = 50.0          # wide vs narrow
    directness: float = 50.0     # long balls vs short passing
    defensive_line: float = 50.0 # deep vs high line


@dataclass
class Team:
    name: str
    squad: List[Player]
    tactic: Tactic = field(default_factory=Tactic)
    points: int = 0
    goals_for: int = 0
    goals_against: int = 0
    played: int = 0

    def available_players(self) -> List[Player]:
        return [p for p in self.squad if not p.injured]

    def goal_difference(self) -> int:
        return self.goals_for - self.goals_against


@dataclass
class MatchStats:
    home_goals: int = 0
    away_goals: int = 0
    home_shots: int = 0
    away_shots: int = 0
    home_xg: float = 0.0
    away_xg: float = 0.0


@dataclass
class MatchResult:
    home_team: str
    away_team: str
    stats: MatchStats
    events: List[str] = field(default_factory=list)


@dataclass
class Fixture:
    home: str
    away: str
    played: bool = False
    result: Optional[MatchResult] = None

@dataclass
class Club:
    identity: ClubIdentity
    team: Team
    finance: ClubFinance
    infrastructure: ClubInfrastructure
    support: ClubSupport
    board: BoardExpectations

@dataclass
class ClubIdentity:
    name: str
    city: str = ""
    founded: int | None = None
    club_size: str = "medium"   # small / medium / big
    reputation: float = 50.0

@dataclass
class ClubFinance:
    balance: int = 0
    transfer_budget: int = 0
    weekly_wages: int = 0
    wage_budget: int = 0
    sponsorship_income: int = 0
    matchday_base_income: int = 0

@dataclass
class ClubInfrastructure:
    stadium_capacity: int = 10000
    ticket_price: int = 20
    training_level: int = 50
    youth_level: int = 50

@dataclass
class ClubSupport:
    fan_confidence: float = 50.0
    fan_base: int = 10000

@dataclass
class BoardExpectations:
    target_finish: int = 6
    max_wage_ratio: float = 0.7
    philosophy: str = "balanced"   # balanced / youth / ambitious / selling_club