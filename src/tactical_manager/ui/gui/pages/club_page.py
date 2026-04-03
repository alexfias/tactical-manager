from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from tactical_manager.ui.gui.widgets.club_overview_widget import ClubOverviewWidget


class ClubPage(QWidget):
    def __init__(self, club, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.club = club

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        title = QLabel("Club")
        title.setProperty("sectionTitle", True)

        self.overview_widget = ClubOverviewWidget(self.club)

        layout.addWidget(title)
        layout.addWidget(self.overview_widget, 1)

    def refresh(self) -> None:
        if hasattr(self.overview_widget, "refresh"):
            self.overview_widget.refresh()