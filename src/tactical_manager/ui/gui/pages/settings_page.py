from __future__ import annotations

from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class SettingsPage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        title = QLabel("Settings")
        title.setProperty("sectionTitle", True)

        info = QLabel("Game settings and system actions will live here.")
        info.setWordWrap(True)

        self.quit_button = QPushButton("Quit")
        self.quit_button.setMinimumHeight(48)

        layout.addWidget(title)
        layout.addWidget(info)
        layout.addWidget(self.quit_button)
        layout.addStretch()