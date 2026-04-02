from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QFont, QPalette, QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QTableWidget, 
    QTableWidgetItem,
)

from tactical_manager.core.models import Tactic, Player
from tactical_manager.core.season import Season
from tactical_manager.ui.gui.dialogs import MatchSetupDialog
from tactical_manager.ui.gui.styles import main_stylesheet
from tactical_manager.ui.gui.widgets.match_result_widget import MatchResultWidget
from tactical_manager.ui.gui.widgets.team_management_widget import TeamManagementWidget
from tactical_manager.ui.render import render_table
from tactical_manager.core.analysis import analyze_match, compute_player_ratings



class GameWindow(QWidget):
    def __init__(self, season: Season):
        super().__init__()

        self.season = season

        self.setWindowTitle("Tactical Manager")
        self.resize(1000, 650)

        palette = self.palette()
        pixmap = QPixmap("assets/backgrounds/stadium_dark.png")
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        root_layout = QVBoxLayout()
        root_layout.setContentsMargins(20, 20, 20, 20)
        root_layout.setSpacing(12)

        self.title = QLabel("TACTICAL MANAGER")
        self.title.setFont(QFont("Arial", 20, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setObjectName("titleLabel")
        root_layout.addWidget(self.title)

        body_layout = QHBoxLayout()
        body_layout.setSpacing(16)

        menu_panel = QWidget()
        menu_panel.setObjectName("menuPanel")
        menu_layout = QVBoxLayout()
        menu_layout.setContentsMargins(16, 16, 16, 16)
        menu_layout.setSpacing(10)
        menu_panel.setLayout(menu_layout)
        menu_panel.setFixedWidth(240)

        self.play_button = QPushButton("Play Next Match")
        self.play_button.clicked.connect(self.play_match)

        self.table_button = QPushButton("Show Table")
        self.table_button.clicked.connect(self.show_table)

        self.club_button = QPushButton("Club Overview")
        self.club_button.clicked.connect(self.show_club_overview)

        self.history_button = QPushButton("Show History")
        self.history_button.clicked.connect(self.show_history)

        self.team_button = QPushButton("Team Management")
        self.team_button.clicked.connect(self.show_team_management)

        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self.close)

        self.nav_buttons = [
            self.play_button,
            self.table_button,
            self.club_button,
            self.history_button,
            self.team_button,
            self.quit_button,
        ]

        for button in self.nav_buttons:
            button.setMinimumHeight(42)
            menu_layout.addWidget(button)

        menu_layout.insertStretch(len(self.nav_buttons) - 1, 1)

        content_panel = QWidget()
        content_panel.setObjectName("contentPanel")
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(16, 16, 16, 16)
        content_layout.setSpacing(10)
        content_panel.setLayout(content_layout)

        self.section_title = QLabel("Welcome")
        self.section_title.setObjectName("sectionTitle")
        self.section_title.setFont(QFont("Arial", 18, QFont.Bold))

        self.match_result_widget = MatchResultWidget()
        self.match_result_widget.hide()

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        club = self.season.clubs[self.season.user_club]
        self.team_management_widget = TeamManagementWidget(club)
        self.team_management_widget.hide()

        content_layout.addWidget(self.section_title)
        content_layout.addWidget(self.match_result_widget)
        content_layout.addWidget(self.output)
        content_layout.addWidget(self.team_management_widget)

        body_layout.addWidget(menu_panel)
        body_layout.addWidget(content_panel, 1)

        root_layout.addLayout(body_layout)
        self.setLayout(root_layout)

        self.setStyleSheet(main_stylesheet())

        self.show_club_overview()

    def hide_all_content_widgets(self) -> None:
        self.output.hide()
        self.match_result_widget.hide()
        self.team_management_widget.hide()

    def set_active_button(self, active_button: QPushButton) -> None:
        for button in self.nav_buttons:
            button.setProperty("active", button is active_button)
            button.style().unpolish(button)
            button.style().polish(button)
            button.update()

    def set_text_content(self, title: str, text: str) -> None:
        self.section_title.setText(title)
        self.hide_all_content_widgets()
        self.output.show()
        self.output.setPlainText(text)

    def set_match_content(self, fixture) -> None:
        self.section_title.setText("Match Result")
        self.hide_all_content_widgets()
        self.match_result_widget.show()

        result = fixture.result
        stats = result.stats

        home_goals = stats.home_goals
        away_goals = stats.away_goals

        home_shots = getattr(stats, "home_shots", home_goals * 3 + 5)
        away_shots = getattr(stats, "away_shots", away_goals * 3 + 5)

        home_possession = getattr(stats, "home_possession", 50)
        away_possession = getattr(stats, "away_possession", 100 - home_possession)

        home_big_chances = getattr(stats, "home_big_chances", max(1, home_goals))
        away_big_chances = getattr(stats, "away_big_chances", max(1, away_goals))

        extra_stats = [
            ("Goals", str(home_goals), str(away_goals)),
            ("Shots", str(home_shots), str(away_shots)),
            ("Possession", f"{home_possession}%", f"{away_possession}%"),
            ("Big chances", str(home_big_chances), str(away_big_chances)),
        ]

        self.match_result_widget.set_result(
            home_name=fixture.home,
            away_name=fixture.away,
            home_goals=home_goals,
            away_goals=away_goals,
            extra_stats=extra_stats,
        )

    def play_match(self) -> None:
        self.set_active_button(self.play_button)

        dialog = MatchSetupDialog(self)
        if dialog.exec() != QDialog.Accepted:
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
            self.set_text_content("Match", "Season finished.")
            return

        self.set_match_content(fixture)

        analysis = analyze_match(fixture.result, is_home=True)
        self.match_result_widget.set_analysis(analysis)

        ratings = compute_player_ratings(
            fixture.result,
            home_xi=fixture.result.home_xi,
            away_xi=fixture.result.away_xi,
        )
        self.match_result_widget.set_ratings(ratings)

    def show_table(self) -> None:
        self.set_active_button(self.table_button)
        table = self.season.get_table()
        self.set_text_content("League Table", render_table(table))

    def show_club_overview(self) -> None:
        self.set_active_button(self.club_button)
        club = self.season.clubs[self.season.user_club]

        lines = [
            "=== CLUB OVERVIEW ===",
            "",
            f"Club: {club.identity.name}",
            f"Country: {club.country}",
            f"Reputation: {club.identity.reputation}",
            "",
            "=== FINANCE ===",
            f"Balance: {club.finance.balance}",
            f"Transfer budget: {club.finance.transfer_budget}",
            f"Weekly wages: {club.finance.weekly_wages}",
            f"Wage budget: {club.finance.wage_budget}",
            "",
            "=== INFRASTRUCTURE ===",
            f"Stadium capacity: {club.infrastructure.stadium_capacity}",
            f"Ticket price: {club.infrastructure.ticket_price}",
            f"Training level: {club.infrastructure.training_level}",
            f"Youth level: {club.infrastructure.youth_level}",
            "",
            "=== SUPPORT ===",
            f"Fan confidence: {club.support.fan_confidence}",
            f"Fan base: {club.support.fan_base}",
            "",
            "=== BOARD ===",
            f"Target finish: {club.board.target_finish}",
            f"Max wage ratio: {club.board.max_wage_ratio}",
            f"Philosophy: {club.board.philosophy}",
        ]

        self.set_text_content("Club Overview", "\n".join(str(x) for x in lines))

    def show_history(self) -> None:
        self.set_active_button(self.history_button)

        if not self.season.history:
            self.set_text_content("History", "No matches played yet.")
            return

        self.set_text_content("History", "\n".join(self.season.history))

    def show_team_management(self) -> None:
        self.set_active_button(self.team_button)

        club = self.season.clubs[self.season.user_club]
        self.team_management_widget.club = club
        self.team_management_widget.refresh()

        self.section_title.setText("Team Management")
        self.hide_all_content_widgets()
        self.team_management_widget.show()


class AvailablePlayersTable(QTableWidget):
    HEADERS = ["Name", "Pos", "CA", "Fit", "Fat", "Mor"]

    def __init__(self, on_player_selected) -> None:
        super().__init__()
        self.on_player_selected = on_player_selected

        self.setColumnCount(len(self.HEADERS))
        self.setHorizontalHeaderLabels(self.HEADERS)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.verticalHeader().setVisible(False)

        self.itemSelectionChanged.connect(self._handle_selection_changed)

    def load_players(self, players: list[Player]) -> None:
        self.setRowCount(len(players))

        for row, player in enumerate(players):
            values = [
                player.name,
                player.position,
                f"{current_ability(player):.1f}",
                f"{player.fitness:.1f}",
                f"{player.fatigue:.1f}",
                f"{player.morale:.1f}",
            ]

            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setData(Qt.UserRole, player)
                self.setItem(row, col, item)

        self.resizeColumnsToContents()

    def selected_player(self) -> Player | None:
        items = self.selectedItems()
        if not items:
            return None
        return items[0].data(Qt.UserRole)

    def _handle_selection_changed(self) -> None:
        player = self.selected_player()
        if player is not None:
            self.on_player_selected(player)