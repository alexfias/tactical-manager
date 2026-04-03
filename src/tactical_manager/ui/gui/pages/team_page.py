from __future__ import annotations

from PySide6.QtWidgets import QLabel, QStackedWidget, QVBoxLayout, QWidget

from tactical_manager.ui.gui.navigation.sub_nav_bar import SubNavBar
from tactical_manager.ui.gui.widgets.team_lineup_widget import TeamLineupWidget
from tactical_manager.ui.gui.widgets.team_management_widget import TeamManagementWidget


class TeamPage(QWidget):
    def __init__(self, club, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.club = club

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        title = QLabel("Team")
        title.setProperty("sectionTitle", True)

        self.sub_nav = SubNavBar([
            ("squad", "Squad"),
            ("lineup", "Lineup"),
        ])
        self.sub_nav.tab_selected.connect(self.switch_tab)

        self.stack = QStackedWidget()
        self.pages: dict[str, QWidget] = {
            "squad": TeamManagementWidget(self.club),
            "lineup": TeamLineupWidget(self.club),
        }

        for page in self.pages.values():
            self.stack.addWidget(page)

        layout.addWidget(title)
        layout.addWidget(self.sub_nav)
        layout.addWidget(self.stack, 1)

        self.switch_tab("squad")

    def switch_tab(self, tab_id: str) -> None:
        self.sub_nav.set_active(tab_id)
        self.stack.setCurrentWidget(self.pages[tab_id])

    def refresh(self) -> None:
        for page in self.pages.values():
            if hasattr(page, "refresh"):
                page.refresh()