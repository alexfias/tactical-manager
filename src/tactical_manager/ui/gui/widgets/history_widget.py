from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class HistoryWidget(QWidget):
    def __init__(self, season, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.season = season

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Results / history coming soon"))

    def refresh(self) -> None:
        pass