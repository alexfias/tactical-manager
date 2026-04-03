from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class AdvancePage(QWidget):
    advance_requested = Signal()

    def __init__(self, season, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.season = season

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        title = QLabel("Advance")
        title.setProperty("sectionTitle", True)

        self.info_label = QLabel("Advance to the next event.")
        self.info_label.setWordWrap(True)

        self.advance_button = QPushButton("Advance")
        self.advance_button.setMinimumHeight(52)
        self.advance_button.clicked.connect(self.advance_requested.emit)

        layout.addWidget(title)
        layout.addWidget(self.info_label)
        layout.addWidget(self.advance_button)
        layout.addStretch()

    def refresh(self) -> None:
        pass