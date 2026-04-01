from __future__ import annotations

from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)


class SquadTableWidget(QTableWidget):
    HEADERS = [
        "Name",
        "Pos",
        "Pass",
        "Tech",
        "Fin",
        "Def",
        "Posit",
        "Pace",
        "Sta",
        "Work",
        "Morale",
        "Fitness",
    ]

    def __init__(self) -> None:
        super().__init__(0, len(self.HEADERS))
        self.setHorizontalHeaderLabels(self.HEADERS)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def load_players(self, players: list) -> None:
        self.clearContents()
        self.setRowCount(0)

        if not players:
            return

        self.setRowCount(len(players))

        for row, p in enumerate(players):
            values = [
                str(getattr(p, "name", "")),
                str(getattr(p, "position", "")),
                str(getattr(p, "passing", "")),
                str(getattr(p, "technique", "")),
                str(getattr(p, "finishing", "")),
                str(getattr(p, "defending", "")),
                str(getattr(p, "positioning", "")),
                str(getattr(p, "pace", "")),
                str(getattr(p, "stamina", "")),
                str(getattr(p, "work_rate", "")),
                str(getattr(p, "morale", "")),
                str(getattr(p, "fitness", "")),
            ]

            for col, value in enumerate(values):
                self.setItem(row, col, QTableWidgetItem(value))