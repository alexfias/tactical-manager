from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import List, Optional, Literal, Any

from uuid import uuid4

MatchPlan = Literal["defensive", "balanced", "attacking"]


@dataclass
class Player:
    name: str
    position: str  # GK, DEF, MID, ATT
    player_id: str = field(default_factory=lambda: str(uuid4()))

    # technical
    passing: float = 50.0
    first_touch: float = 50.0
    technique: float = 50.0
    dribbling: float = 50.0
    finishing: float = 50.0
    long_shots: float = 50.0
    tackling: float = 50.0
    heading: float = 50.0
    crossing: float = 50.0

    # mental / tactical
    positioning: float = 50.0
    vision: float = 50.0
    decision_making: float = 50.0
    anticipation: float = 50.0
    composure: float = 50.0
    concentration: float = 50.0
    work_rate: float = 50.0
    discipline: float = 50.0
    aggression: float = 50.0
    off_the_ball: float = 50.0

    # physical
    pace: float = 50.0
    acceleration: float = 50.0
    agility: float = 50.0
    strength: float = 50.0
    stamina: float = 50.0
    jumping: float = 50.0

    # dynamic state
    fatigue: float = 10.0
    fitness: float = 95.0
    morale: float = 60.0
    familiarity: float = 50.0
    confidence: float = 50.0
    sharpness: float = 50.0
    injury_proneness: float = 20.0
    injured: bool = False

    # career / economic
    age: int = 24
    wage: int = 1000
    contract_weeks: int = 104
    potential: float = 60.0
    development_rate: float = 1.0  # professionalism / growth factor

    def availability_multiplier(self) -> float:
        if self.injured:
            return 0.0

        fatigue_factor = max(0.0, 1.0 - self.fatigue / 140.0)
        fitness_factor = self.fitness / 100.0
        morale_factor = 0.8 + 0.4 * (self.morale / 100.0)
        familiarity_factor = 0.8 + 0.4 * (self.familiarity / 100.0)
        return max(0.0, fatigue_factor * fitness_factor * morale_factor * familiarity_factor)

    def effective(self, attribute: str) -> float:
        base = self._get_attribute_value(attribute)
        return base * self.availability_multiplier()

    def _get_attribute_value(self, attribute: str) -> float:
        # Direct attributes
        if hasattr(self, attribute):
            return getattr(self, attribute)

        # Derived attributes
        if attribute == "defending":
            return (
                0.4 * self.tackling
                + 0.2 * self.positioning
                + 0.15 * self.anticipation
                + 0.1 * self.strength
                + 0.1 * self.heading
                + 0.05 * self.discipline
            )

        if attribute == "passing":
            return (
                0.4 * self.passing
                + 0.2 * self.vision
                + 0.2 * self.technique
                + 0.2 * self.decision_making
            )

        if attribute == "finishing":
            return (
                0.5 * self.finishing
                + 0.2 * self.composure
                + 0.2 * self.technique
                + 0.1 * self.off_the_ball
            )

        if attribute == "dribbling":
            return (
                0.5 * self.dribbling
                + 0.3 * self.technique
                + 0.2 * self.agility
            )

        if attribute == "pace":
            return (
                0.6 * self.pace
                + 0.4 * self.acceleration
            )

        raise AttributeError(f"Unknown attribute requested: {attribute}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Player":
        return cls(**data)


@dataclass
class Tactic:
    formation: str = "4-4-2"
    mentality: float = 50.0
    pressing: float = 50.0
    tempo: float = 50.0
    width: float = 50.0
    directness: float = 50.0
    defensive_line: float = 50.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Tactic":
        return cls(**data)


@dataclass
class Team:
    name: str
    squad: List[Player]
    tactic: Tactic = field(default_factory=Tactic)
    starting_xi: list[Player] = field(default_factory=list)
    lineup_by_role: dict[str, Player | None] = field(default_factory=dict)
    played: int = 0
    wins: int = 0
    draws: int = 0
    losses: int = 0
    goals_for: int = 0
    goals_against: int = 0
    points: int = 0

    def __post_init__(self) -> None:
        if not self.starting_xi and len(self.squad) >= 11:
            self.starting_xi = self.squad[:11]

    def available_players(self) -> List[Player]:
        return [p for p in self.squad if not p.injured]

    def goal_difference(self) -> int:
        return self.goals_for - self.goals_against

    def has_valid_starting_xi(self) -> bool:
        return self.starting_xi is not None and len(self.starting_xi) == 11

    def auto_pick_starting_xi(self) -> None:
        self.starting_xi = self.squad[:11]

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "squad": [player.to_dict() for player in self.squad],
            "tactic": self.tactic.to_dict(),
            "starting_xi": [player.player_id for player in self.starting_xi],
            "lineup_by_role": {
                role: player.player_id if player is not None else None
                for role, player in self.lineup_by_role.items()
            },
            "played": self.played,
            "wins": self.wins,
            "draws": self.draws,
            "losses": self.losses,
            "goals_for": self.goals_for,
            "goals_against": self.goals_against,
            "points": self.points,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Team":
        squad = [Player.from_dict(p) for p in data.get("squad", [])]
        players_by_id = {player.player_id: player for player in squad}

        tactic_data = data.get("tactic", {})
        tactic = Tactic.from_dict(tactic_data) if tactic_data else Tactic()

        starting_xi = [
            players_by_id[player_id]
            for player_id in data.get("starting_xi", [])
            if player_id in players_by_id
        ]

        lineup_by_role = {
            role: players_by_id[player_id] if player_id in players_by_id else None
            for role, player_id in data.get("lineup_by_role", {}).items()
            if player_id is None or player_id in players_by_id
        }

        return cls(
            name=data["name"],
            squad=squad,
            tactic=tactic,
            starting_xi=starting_xi,
            lineup_by_role=lineup_by_role,
            played=data.get("played", 0),
            wins=data.get("wins", 0),
            draws=data.get("draws", 0),
            losses=data.get("losses", 0),
            goals_for=data.get("goals_for", 0),
            goals_against=data.get("goals_against", 0),
            points=data.get("points", 0),
        )

@dataclass
class MatchStats:
    home_goals: int = 0
    away_goals: int = 0
    home_shots: int = 0
    away_shots: int = 0
    home_xg: float = 0.0
    away_xg: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MatchStats":
        return cls(**data)


@dataclass
class MatchResult:
    home_team: str
    away_team: str
    stats: MatchStats
    events: List[str] = field(default_factory=list)
    analysis_data: dict | None = None
    home_xi: list[str] | None = None
    away_xi: list[str] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "home_team": self.home_team,
            "away_team": self.away_team,
            "stats": self.stats.to_dict(),
            "events": list(self.events),
            "analysis_data": self.analysis_data,
            "home_xi": list(self.home_xi) if self.home_xi is not None else None,
            "away_xi": list(self.away_xi) if self.away_xi is not None else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MatchResult":
        return cls(
            home_team=data["home_team"],
            away_team=data["away_team"],
            stats=MatchStats.from_dict(data["stats"]),
            events=data.get("events", []),
            analysis_data=data.get("analysis_data"),
            home_xi=data.get("home_xi"),
            away_xi=data.get("away_xi"),
        )


@dataclass
class Fixture:
    home: str
    away: str
    played: bool = False
    result: Optional[MatchResult] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "home": self.home,
            "away": self.away,
            "played": self.played,
            "result": self.result.to_dict() if self.result is not None else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Fixture":
        result_data = data.get("result")
        return cls(
            home=data["home"],
            away=data["away"],
            played=data.get("played", False),
            result=MatchResult.from_dict(result_data) if result_data else None,
        )


@dataclass
class ClubIdentity:
    name: str
    city: str = ""
    founded: int | None = None
    club_size: str = "medium"   # small / medium / big
    reputation: float = 50.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ClubIdentity":
        return cls(**data)


from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class ClubFinance:
    # liquidity
    cash: float = 0.0

    # budgets
    transfer_budget: float = 0.0
    wage_budget: float = 0.0

    # ongoing flows
    weekly_wages: float = 0.0
    sponsorship_income: float = 0.0
    matchday_base_income: float = 0.0

    # liabilities (important for balance sheet later)
    debt: float = 0.0
    transfer_payables: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ClubFinance":
        data = dict(data)

        if "balance" in data and "cash" not in data:
            data["cash"] = data.pop("balance")

        return cls(**data)


@dataclass
class ClubInfrastructure:
    stadium_capacity: int = 10000
    ticket_price: int = 20
    training_level: int = 50
    youth_level: int = 50

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ClubInfrastructure":
        return cls(**data)


@dataclass
class ClubSupport:
    fan_confidence: float = 50.0
    fan_base: int = 10000

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ClubSupport":
        return cls(**data)


@dataclass
class BoardExpectations:
    target_finish: int = 6
    max_wage_ratio: float = 0.7
    philosophy: str = "balanced"   # balanced / youth / ambitious / selling_club

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BoardExpectations":
        return cls(**data)


@dataclass
class Club:
    identity: ClubIdentity
    country: str
    team: Team
    finance: ClubFinance
    infrastructure: ClubInfrastructure
    support: ClubSupport
    board: BoardExpectations

    def to_dict(self) -> dict[str, Any]:
        return {
            "identity": self.identity.to_dict(),
            "country": self.country,
            "team": self.team.to_dict(),
            "finance": self.finance.to_dict(),
            "infrastructure": self.infrastructure.to_dict(),
            "support": self.support.to_dict(),
            "board": self.board.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Club":
        return cls(
            identity=ClubIdentity.from_dict(data["identity"]),
            country=data["country"],
            team=Team.from_dict(data["team"]),
            finance=ClubFinance.from_dict(data["finance"]),
            infrastructure=ClubInfrastructure.from_dict(data["infrastructure"]),
            support=ClubSupport.from_dict(data["support"]),
            board=BoardExpectations.from_dict(data["board"]),
        )


@dataclass
class LeagueTableRow:
    name: str
    played: int = 0
    wins: int = 0
    draws: int = 0
    losses: int = 0
    goals_for: int = 0
    goals_against: int = 0
    points: int = 0

    def goal_difference(self) -> int:
        return self.goals_for - self.goals_against

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LeagueTableRow":
        return cls(**data)