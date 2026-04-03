from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QFont, QPalette, QPixmap
from PySide6.QtWidgets import QLabel, QStackedWidget, QVBoxLayout, QWidget

from tactical_manager.core.analysis import analyze_match, compute_player_ratings
from tactical_manager.core.models import Tactic
from tactical_manager.core.season import Season
from tactical_manager.ui.gui.dialogs import MatchSetupDialog
from tactical_manager.ui.gui.navigation.bottom_nav_bar import BottomNavBar
from tactical_manager.ui.gui.pages.advance_page import AdvancePage
from tactical_manager.ui.gui.pages.club_page import ClubPage
from tactical_manager.ui.gui.pages.season_page import SeasonPage
from tactical_manager.ui.gui.pages.settings_page import SettingsPage
from tactical_manager.ui.gui.pages.team_page import TeamPage
from tactical_manager.ui.gui.styles import main_stylesheet


class GameWindow(QWidget):
    def __init__(self, season: Season):
        super().__init__()

        self.season = season
        self.club = self.season.clubs[self.season.user_club]

        self.setWindowTitle("Tactical Manager")
        self.resize(1000, 650)

        palette = self.palette()
        pixmap = QPixmap("assets/backgrounds/stadium_dark.png")
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(20, 20, 20, 20)
        root_layout.setSpacing(12)

        self.title = QLabel("TACTICAL MANAGER")
        self.title.setFont(QFont("Arial", 20, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setObjectName("titleLabel")
        root_layout.addWidget(self.title)

        self.content_stack = QStackedWidget()

        self.advance_page = AdvancePage(self.season)
        self.season_page = SeasonPage(self.season)
        self.team_page = TeamPage(self.club)
        self.club_page = ClubPage(self.club)
        self.settings_page = SettingsPage()

        self.pages: dict[str, QWidget] = {
            "advance": self.advance_page,
            "season": self.season_page,
            "team": self.team_page,
            "club": self.club_page,
            "settings": self.settings_page,
        }

        for page in self.pages.values():
            self.content_stack.addWidget(page)

        root_layout.addWidget(self.content_stack, 1)

        self.bottom_nav = BottomNavBar()
        self.bottom_nav.section_selected.connect(self.switch_section)
        root_layout.addWidget(self.bottom_nav)

        self._connect_page_signals()

        self.setStyleSheet(main_stylesheet())
        self.switch_section("season")

    def _connect_page_signals(self) -> None:
        if hasattr(self.advance_page, "advance_requested"):
            self.advance_page.advance_requested.connect(self.advance_time)

        if hasattr(self.settings_page, "quit_button"):
            self.settings_page.quit_button.clicked.connect(self.close)

    def switch_section(self, section_id: str) -> None:
        page = self.pages[section_id]
        self.content_stack.setCurrentWidget(page)
        self.bottom_nav.set_active(section_id)

        if hasattr(page, "refresh"):
            page.refresh()

    def refresh_all(self) -> None:
        for page in self.pages.values():
            if hasattr(page, "refresh"):
                page.refresh()

    def advance_time(self) -> None:
        dialog = MatchSetupDialog(self)
        if dialog.exec() != MatchSetupDialog.Accepted:
            return

        plan, mentality = dialog.get_values()

        pressing_map = {
            "defensive": 40,
            "balanced": 50,
            "attacking": 65,
        }

        tempo_map = {
            "defensive": 40,
            "balanced": 50,
            "attacking": 65,
        }

        tactic = Tactic(
            formation="4-4-2",
            pressing=pressing_map[mentality],
            tempo=tempo_map[plan],
            width=50,
        )

        fixture = self.season.play_next_fixture(
            user_plan=plan,
            user_tactic=tactic,
        )

        if fixture is None:
            if hasattr(self.advance_page, "show_message"):
                self.advance_page.show_message("Season finished.")
            self.refresh_all()
            self.switch_section("advance")
            return

        if hasattr(self.advance_page, "set_match_content"):
            self.advance_page.set_match_content(fixture)

        analysis = analyze_match(fixture.result, is_home=True)
        if hasattr(self.advance_page, "set_analysis"):
            self.advance_page.set_analysis(analysis)

        ratings = compute_player_ratings(
            fixture.result,
            home_xi=fixture.result.home_xi,
            away_xi=fixture.result.away_xi,
        )
        if hasattr(self.advance_page, "set_ratings"):
            self.advance_page.set_ratings(ratings)

        self.refresh_all()
        self.switch_section("advance")