from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QTextEdit, QSplashScreen, QDialog, QDialogButtonBox,
    QComboBox, QFormLayout
)
from PySide6.QtGui import QFont, QPalette, QBrush, QPixmap
from PySide6.QtCore import Qt, QTimer

from tactical_manager.core.season import Season
from tactical_manager.ui.render import render_match, render_table
from tactical_manager.core.models import Tactic

class MatchSetupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Match Setup")
        self.setModal(True)

        layout = QVBoxLayout()
        form = QFormLayout()

        self.plan_combo = QComboBox()
        self.plan_combo.addItems(["defensive", "balanced", "attacking"])

        self.mentality_combo = QComboBox()
        self.mentality_combo.addItems(["defensive", "balanced", "attacking"])

        form.addRow("Match approach:", self.plan_combo)
        form.addRow("Mentality:", self.mentality_combo)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)
        self.setLayout(layout)

    def get_values(self) -> tuple[str, str]:
        return self.plan_combo.currentText(), self.mentality_combo.currentText()


class GameWindow(QWidget):
    def __init__(self, season: Season):
        super().__init__()

        self.season = season

        self.setWindowTitle("Tactical Manager")
        self.resize(700, 500)

        # Background only for main window
        palette = self.palette()
        pixmap = QPixmap("assets/backgrounds/stadium_dark.png")
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(12)

        # Main panel
        panel = QWidget()
        panel.setObjectName("mainPanel")
        panel_layout = QVBoxLayout()
        panel_layout.setContentsMargins(16, 16, 16, 16)
        panel_layout.setSpacing(12)
        panel.setLayout(panel_layout)

        # Title
        self.title = QLabel("Tactical Manager")
        self.title.setFont(QFont("Arial", 22, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)

        # Buttons
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

        # Output
        self.output = QTextEdit()
        self.output.setReadOnly(True)

        # Add widgets only to panel layout
        panel_layout.addWidget(self.title)
        panel_layout.addWidget(self.play_button)
        panel_layout.addWidget(self.table_button)
        panel_layout.addWidget(self.club_button)
        panel_layout.addWidget(self.history_button)
        panel_layout.addWidget(self.team_button)
        panel_layout.addWidget(self.quit_button)
        panel_layout.addWidget(self.output)
        # Add panel to main layout
        self.layout.addWidget(panel)
        self.setLayout(self.layout)

        # Styles
        self.setStyleSheet("""
            #mainPanel {
                background-color: rgba(0, 0, 0, 130);
                border-radius: 12px;
            }

            QLabel {
                color: white;
                background-color: rgba(0, 0, 0, 120);
                border-radius: 10px;
                padding: 10px;
            }

            QPushButton {
                background-color: rgba(20, 20, 20, 180);
                color: white;
                border: 1px solid rgba(255, 255, 255, 40);
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: rgba(40, 40, 40, 210);
            }

            QTextEdit {
                background-color: rgba(10, 10, 10, 190);
                color: white;
                border: 1px solid rgba(255, 255, 255, 40);
                border-radius: 10px;
                padding: 8px;
            }
        """)

    def play_match(self):
        dialog = MatchSetupDialog(self)

        if dialog.exec() != QDialog.Accepted:
            return

        plan, mentality = dialog.get_values()

        tempo_map = {
            "defensive": 40,
            "balanced": 50,
            "attacking": 65,
        }

        pressing_map = {
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
            self.output.append("Season finished.\n")
            return

        self.output.clear()
        self.output.append(render_match(fixture.result))
        self.output.append("")

    def show_table(self):
        table = self.season.get_table()
        self.output.append(render_table(table))
        self.output.append("")

    def show_club_overview(self):
        club = self.season.clubs[self.season.user_club]

        lines = [
            f"Club: {club.identity.name}",
            f"Country: {club.country}",
            f"Reputation: {club.identity.reputation}",
            "",
            "Finance",
            f"Balance: {club.finance.balance}",
            f"Transfer budget: {club.finance.transfer_budget}",
            f"Weekly wages: {club.finance.weekly_wages}",
            f"Wage budget: {club.finance.wage_budget}",
            "",
            "Infrastructure",
            f"Stadium capacity: {club.infrastructure.stadium_capacity}",
            f"Ticket price: {club.infrastructure.ticket_price}",
            f"Training level: {club.infrastructure.training_level}",
            f"Youth level: {club.infrastructure.youth_level}",
            "",
            "Support",
            f"Fan confidence: {club.support.fan_confidence}",
            f"Fan base: {club.support.fan_base}",
            "",
            "Board",
            f"Target finish: {club.board.target_finish}",
            f"Max wage ratio: {club.board.max_wage_ratio}",
            f"Philosophy: {club.board.philosophy}",
        ]

        self.output.clear()
        self.output.setPlainText("\n".join(str(x) for x in lines))

    def show_history(self):
        self.output.clear()
        if not self.season.history:
            self.output.setPlainText("No matches played yet.")
            return

        self.output.setPlainText("\n".join(self.season.history))

    def show_team_management(self):
        club = self.season.clubs[self.season.user_club]
        team = club.team

        lines = [f"Team: {team.name}", "", "Squad"]

        for player in team.squad:
            starter_mark = "*" if player in team.starting_xi else " "
            lines.append(
                f"{starter_mark} {player.name} | {player.position} | "
                f"Morale {player.morale:.0f} | Fitness {player.fitness:.0f} | Fatigue {player.fatigue:.0f}"
            )

        self.output.clear()
        self.output.setPlainText("\n".join(lines))


def run_gui(season: Season):
    app = QApplication([])

    pixmap = QPixmap("assets/splash.png")
    splash = QSplashScreen(pixmap)
    splash.setWindowFlag(Qt.FramelessWindowHint)
    splash.showMessage(
        "Tactical Manager\nLoading...",
        Qt.AlignCenter | Qt.AlignBottom,
        Qt.white,
    )
    splash.show()

    app.processEvents()

    window = GameWindow(season)

    def start_main_window():
        window.show()
        splash.finish(window)

    QTimer.singleShot(2000, start_main_window)

    app.exec()


