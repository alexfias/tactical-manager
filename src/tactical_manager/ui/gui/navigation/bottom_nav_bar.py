from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget


class BottomNavBar(QWidget):
    section_selected = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.buttons: dict[str, QPushButton] = {}

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(12)

        for section_id, label in [
            ("advance", "Advance"),
            ("season", "Season"),
            ("team", "Team"),
            ("club", "Club"),
            ("settings", "Settings"),
        ]:
            button = QPushButton(label)
            button.setCheckable(True)
            button.clicked.connect(
                lambda checked=False, sid=section_id: self.section_selected.emit(sid)
            )
            button.setMinimumHeight(52)
            button.setProperty("nav", True)

            self.buttons[section_id] = button
            layout.addWidget(button)

        self.set_active("season")

    def set_active(self, section_id: str) -> None:
        for sid, button in self.buttons.items():
            button.setChecked(sid == section_id)