from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QSizePolicy


class BottomNavBar(QFrame):
    page_requested = Signal(str)
    quit_requested = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setObjectName("bottom_nav_bar")
        self.setFrameShape(QFrame.NoFrame)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self._buttons: dict[str, QPushButton] = {}

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(12)

        # left-to-right order in the bar
        nav_items = [
            ("main", "Main", "main.png"),
            ("team", "Squad", "squad.png"),
            ("training", "Training", "training.png"),
            ("transfers", "Transfers", "transfers.png"),
            ("season", "Season", "season.png"),
            ("club", "Club", "club.png"),
            ("advance", "Advance Time", "advance.png"),
            ("settings", "Settings", "settings.png"),
        ]

        for key, label, icon_name in nav_items:
            button = self._create_nav_button(label, icon_name)
            button.clicked.connect(lambda checked=False, page=key: self.page_requested.emit(page))
            layout.addWidget(button)
            self._buttons[key] = button

        layout.addStretch(1)

        quit_button = self._create_nav_button("Quit", "quit.png")
        quit_button.clicked.connect(self.quit_requested.emit)
        layout.addWidget(quit_button)
        self._buttons["quit"] = quit_button

    def _create_nav_button(self, label: str, icon_name: str) -> QPushButton:
        button = QPushButton()
        button.setObjectName("nav_button")
        button.setToolTip(label)
        button.setCheckable(True)
        button.setCursor(Qt.PointingHandCursor)

        button.setFixedSize(96, 96)
        button.setIconSize(QSize(64, 64))

        icon_path = Path("assets") / "icons" / icon_name
        if icon_path.exists():
            button.setIcon(QIcon(str(icon_path)))
            button.setText("")
        else:
            button.setText(label)

        button.setText("")
        button.setStyleSheet("text-align: center;")
        
        return button

    def set_active_button(self, key: str) -> None:
        for name, button in self._buttons.items():
            button.setChecked(name == key)