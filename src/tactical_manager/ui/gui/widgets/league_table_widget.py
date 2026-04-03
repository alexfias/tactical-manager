from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class LeagueTableWidget(QWidget):
    def __init__(self, season, parent=None):
        super().__init__(parent)
        self.season = season

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("League table coming soon"))