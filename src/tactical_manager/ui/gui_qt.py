from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QLabel, QTextEdit
)

from tactical_manager.core.season import Season
from tactical_manager.ui.render import render_match, render_table


class GameWindow(QWidget):
    def __init__(self, season: Season):
        super().__init__()

        self.season = season

        self.setWindowTitle("Tactical Manager")

        # Layout
        self.layout = QVBoxLayout()

        self.title = QLabel("Tactical Manager")
        self.layout.addWidget(self.title)

        self.play_button = QPushButton("Play Next Match")
        self.play_button.clicked.connect(self.play_match)
        self.layout.addWidget(self.play_button)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.layout.addWidget(self.output)

        self.table_button = QPushButton("Show Table")
        self.table_button.clicked.connect(self.show_table)
        self.layout.addWidget(self.table_button)

        self.setLayout(self.layout)

    def play_match(self):
        fixture = self.season.play_next_fixture()

        if fixture is None:
            self.output.append("Season finished.\n")
            return

        self.output.append(render_match(fixture.result))
        self.output.append("")

    def show_table(self):
        table = self.season.table()
        self.output.append(render_table(table))
        self.output.append("")


def run_gui(season: Season):
    app = QApplication([])
    window = GameWindow(season)
    window.show()
    app.exec()