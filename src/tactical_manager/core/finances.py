from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(slots=True)
class FinancialReport:
    """Profit and loss style report for a season or financial year."""

    season_label: str
    revenues: dict[str, float] = field(default_factory=dict)
    costs: dict[str, float] = field(default_factory=dict)

    @property
    def total_revenue(self) -> float:
        return float(sum(self.revenues.values()))

    @property
    def total_cost(self) -> float:
        return float(sum(self.costs.values()))

    @property
    def net_result(self) -> float:
        return self.total_revenue - self.total_cost

    def add_revenue(self, category: str, amount: float) -> None:
        self.revenues[category] = self.revenues.get(category, 0.0) + float(amount)

    def add_cost(self, category: str, amount: float) -> None:
        self.costs[category] = self.costs.get(category, 0.0) + float(amount)


@dataclass(slots=True)
class BalanceSheet:
    """Snapshot of club assets, liabilities, and equity."""

    assets: dict[str, float] = field(default_factory=dict)
    liabilities: dict[str, float] = field(default_factory=dict)

    @property
    def total_assets(self) -> float:
        return float(sum(self.assets.values()))

    @property
    def total_liabilities(self) -> float:
        return float(sum(self.liabilities.values()))

    @property
    def equity(self) -> float:
        return self.total_assets - self.total_liabilities

    def add_asset(self, category: str, amount: float) -> None:
        self.assets[category] = self.assets.get(category, 0.0) + float(amount)

    def add_liability(self, category: str, amount: float) -> None:
        self.liabilities[category] = self.liabilities.get(category, 0.0) + float(amount)


@dataclass(slots=True)
class FinanceSnapshot:
    """
    Minimal financial state of a club at a point in time.

    This can either be stored directly on the Club model or assembled from it.
    """

    cash: float = 0.0
    debt: float = 0.0
    transfer_budget: float = 0.0
    squad_value: float = 0.0
    stadium_value: float = 0.0
    facilities_value: float = 0.0
    transfer_payables: float = 0.0


def safe_sum(values: Iterable[float]) -> float:
    return float(sum(float(v) for v in values))


def build_financial_report(
    season_label: str,
    revenues: dict[str, float] | None = None,
    costs: dict[str, float] | None = None,
) -> FinancialReport:
    """
    Build a FinancialReport from simple dictionaries.

    Example:
        report = build_financial_report(
            season_label="2025/26",
            revenues={"Matchday": 1_200_000, "Sponsors": 800_000},
            costs={"Player wages": 1_000_000, "Staff wages": 250_000},
        )
    """
    return FinancialReport(
        season_label=season_label,
        revenues=dict(revenues or {}),
        costs=dict(costs or {}),
    )


def build_balance_sheet(snapshot: FinanceSnapshot) -> BalanceSheet:
    """
    Build a balance sheet from a finance snapshot.

    Assets:
    - cash
    - squad value
    - stadium value
    - facilities value

    Liabilities:
    - debt
    - transfer payables
    """
    sheet = BalanceSheet()

    if snapshot.cash:
        sheet.add_asset("Cash", snapshot.cash)
    if snapshot.squad_value:
        sheet.add_asset("Squad value", snapshot.squad_value)
    if snapshot.stadium_value:
        sheet.add_asset("Stadium", snapshot.stadium_value)
    if snapshot.facilities_value:
        sheet.add_asset("Facilities", snapshot.facilities_value)

    if snapshot.debt:
        sheet.add_liability("Debt", snapshot.debt)
    if snapshot.transfer_payables:
        sheet.add_liability("Transfer payables", snapshot.transfer_payables)

    return sheet


def estimate_squad_value(players: Iterable[object]) -> float:
    """
    Very simple placeholder squad valuation.

    This function is intentionally generic so it can already be used before
    the player valuation model is finalized.

    Expected player attributes (if present):
    - market_value
    - value
    - overall

    Priority:
    1. use `market_value`
    2. use `value`
    3. estimate from `overall`
    4. fallback to 0
    """
    total = 0.0

    for player in players:
        if hasattr(player, "market_value"):
            total += float(getattr(player, "market_value") or 0.0)
        elif hasattr(player, "value"):
            total += float(getattr(player, "value") or 0.0)
        elif hasattr(player, "overall"):
            overall = float(getattr(player, "overall") or 0.0)
            total += overall * 100_000.0

    return total


def snapshot_from_club(club: object) -> FinanceSnapshot:
    finance = getattr(club, "finance", None)

    if finance is None:
        return FinanceSnapshot()

    players = getattr(club, "players", [])

    return FinanceSnapshot(
        cash=finance.cash,
        debt=finance.debt,
        transfer_budget=finance.transfer_budget,
        squad_value=estimate_squad_value(players),
        transfer_payables=finance.transfer_payables,
    )