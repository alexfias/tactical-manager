from __future__ import annotations

from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)

from tactical_manager.core.models import Player
from tactical_manager.core.player_valuation import current_ability, estimate_market_value


class SquadTableWidget(QTableWidget):
    HEADERS = [
        "Name",
        "Pos",
        "Age",
        "CA",
        "Value",
    ]

    def __init__(self) -> None:
        super().__init__(0, len(self.HEADERS))
        self.setHorizontalHeaderLabels(self.HEADERS)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSortingEnabled(False)

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)          # Name
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents) # Pos
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents) # Age
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents) # CA
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents) # Value

    def load_players(self, players: list[Player]) -> None:
        self.clearContents()
        self.setRowCount(0)

        if not players:
            return

        self.setRowCount(len(players))

        for row, player in enumerate(players):
            age = getattr(player, "age", 24)
            ability = current_ability(player)
            value = estimate_market_value(player)

            values = [
                str(getattr(player, "name", "")),
                str(getattr(player, "position", "")),
                str(age),
                f"{ability:.1f}",
                self._format_value(value),
            ]

            for col, value_text in enumerate(values):
                item = QTableWidgetItem(value_text)
                self.setItem(row, col, item)

    @staticmethod
    def _format_value(value: int) -> str:
        if value >= 1_000_000:
            return f"€{value / 1_000_000:.1f}M"
        if value >= 1_000:
            return f"€{value / 1_000:.0f}K"
        return f"€{value}"