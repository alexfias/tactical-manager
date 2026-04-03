from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy, QWidget


class BottomNavBar(QWidget):
    section_selected = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.buttons: dict[str, QPushButton] = {}

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(12)

        icon_dir = Path("assets/icons")

        sections = [
            ("advance", icon_dir / "advance.png"),
            ("season", icon_dir / "season.png"),
            ("team", icon_dir / "team.png"),
            ("club", icon_dir / "club.png"),
            ("settings", icon_dir / "settings.png"),
        ]

        for section_id, icon_path in sections:
            button = QPushButton()
            button.setCheckable(True)
            button.setCursor(Qt.PointingHandCursor)
            button.setProperty("nav", True)

            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button.setMinimumHeight(96)
            button.setIcon(QIcon(str(icon_path)))
            button.setIconSize(QSize(64, 64))
            button.setToolTip(section_id.capitalize())

            button.clicked.connect(
                lambda checked=False, sid=section_id: self.section_selected.emit(sid)
            )

            self.buttons[section_id] = button
            layout.addWidget(button)

        self.set_active("season")

    def set_active(self, section_id: str) -> None:
        for sid, button in self.buttons.items():
            button.setChecked(sid == section_id)