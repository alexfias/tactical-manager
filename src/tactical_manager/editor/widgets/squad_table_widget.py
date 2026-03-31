from __future__ import annotations

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

from tactical_manager.core.models import Player


class SquadTableWidget(QTableWidget):
    HEADERS = [
        "Name",
        "Pos",
        "Atk",
        "Def",
        "Pass",
        "Sta",
        "Mor",
        "Form",
        "Age",
    ]

    def __init__(self) -> None:
        super().__init__(0, len(self.HEADERS))
        self.setHorizontalHeaderLabels(self.HEADERS)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setSelectionMode(QTableWidget.SingleSelection)
        self.setEditTriggers(QTableWidget.NoEditTriggers)

    def load_players(self, players: list[Player]) -> None:
        self.setRowCount(len(players))
        for row, p in enumerate(players):
            values = [
                p.name,
                p.position,
                str(p.attack),
                str(p.defense),
                str(p.passing),
                str(p.stamina),
                str(p.morale),
                str(p.form),
                str(p.age),
            ]
            for col, value in enumerate(values):
                self.setItem(row, col, QTableWidgetItem(value))

        self.resizeColumnsToContents()