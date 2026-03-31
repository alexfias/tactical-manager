from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QWidget


class StatRow(QWidget):
    def __init__(self, label: str, home_value: str, away_value: str, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(12)

        self.home_label = QLabel(home_value)
        self.home_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.home_label.setObjectName("statValue")

        self.center_label = QLabel(label)
        self.center_label.setAlignment(Qt.AlignCenter)
        self.center_label.setObjectName("statLabel")

        self.away_label = QLabel(away_value)
        self.away_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.away_label.setObjectName("statValue")

        layout.addWidget(self.home_label, 1)
        layout.addWidget(self.center_label, 1)
        layout.addWidget(self.away_label, 1)

        self.setLayout(layout)


class MatchResultWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("matchResultCard")

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(18, 18, 18, 18)
        self.layout.setSpacing(14)

        self.status_label = QLabel("Full Time")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setObjectName("matchStatus")

        self.score_row = QWidget()
        self.score_layout = QHBoxLayout()
        self.score_layout.setContentsMargins(0, 0, 0, 0)
        self.score_layout.setSpacing(10)

        self.home_team_label = QLabel("Home")
        self.home_team_label.setAlignment(Qt.AlignCenter)
        self.home_team_label.setObjectName("teamName")

        self.score_label = QLabel("0 - 0")
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setObjectName("scoreLine")
        self.score_label.setFont(QFont("Arial", 24, QFont.Bold))

        self.away_team_label = QLabel("Away")
        self.away_team_label.setAlignment(Qt.AlignCenter)
        self.away_team_label.setObjectName("teamName")

        self.score_layout.addWidget(self.home_team_label, 2)
        self.score_layout.addWidget(self.score_label, 1)
        self.score_layout.addWidget(self.away_team_label, 2)
        self.score_row.setLayout(self.score_layout)

        self.summary_title = QLabel("Match Summary")
        self.summary_title.setObjectName("summaryTitle")

        self.stats_container = QWidget()
        self.stats_layout = QVBoxLayout()
        self.stats_layout.setContentsMargins(0, 0, 0, 0)
        self.stats_layout.setSpacing(2)
        self.stats_container.setLayout(self.stats_layout)

        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.score_row)
        self.layout.addWidget(self.summary_title)
        self.layout.addWidget(self.stats_container)
        self.layout.addStretch()

        self.setLayout(self.layout)

    def clear_stats(self) -> None:
        while self.stats_layout.count():
            item = self.stats_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def set_result(
        self,
        home_name: str,
        away_name: str,
        home_goals: int,
        away_goals: int,
        extra_stats: list[tuple[str, str, str]] | None = None,
    ) -> None:
        self.home_team_label.setText(home_name)
        self.away_team_label.setText(away_name)
        self.score_label.setText(f"{home_goals} - {away_goals}")

        self.clear_stats()

        rows = extra_stats or [
            ("Goals", str(home_goals), str(away_goals)),
        ]

        for label, home_value, away_value in rows:
            self.stats_layout.addWidget(StatRow(label, home_value, away_value))