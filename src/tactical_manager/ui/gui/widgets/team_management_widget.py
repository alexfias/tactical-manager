from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHeaderView,
    QLabel,
    QScrollArea,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from tactical_manager.core.models import Club, Player


def current_ability(player: Player) -> float:
    values = [
        # technical
        player.passing,
        player.first_touch,
        player.technique,
        player.dribbling,
        player.finishing,
        player.long_shots,
        player.tackling,
        player.heading,
        player.crossing,

        # mental / tactical
        player.positioning,
        player.vision,
        player.decision_making,
        player.anticipation,
        player.composure,
        player.concentration,
        player.work_rate,
        player.discipline,
        player.aggression,

        # physical
        player.pace,
        player.acceleration,
        player.agility,
        player.strength,
        player.stamina,
        player.jumping,
    ]
    return round(sum(values) / len(values), 1)


def estimate_market_value(player: Player) -> int:
    ability = current_ability(player)

    age = getattr(player, "age", 24)
    potential = getattr(player, "potential", ability)
    fitness = getattr(player, "fitness", 100.0)
    morale = getattr(player, "morale", 100.0)
    injured = getattr(player, "injured", False)

    if age <= 21:
        age_factor = 1.25
    elif age <= 25:
        age_factor = 1.15
    elif age <= 29:
        age_factor = 1.00
    elif age <= 32:
        age_factor = 0.85
    else:
        age_factor = 0.70

    potential_factor = 1.0 + max(0.0, potential - ability) / 200.0
    status_factor = (fitness / 100.0) * (0.8 + morale / 500.0)

    if injured:
        status_factor *= 0.85

    value = 60000 * ability * age_factor * potential_factor * status_factor
    return max(10000, int(round(value / 1000) * 1000))


class PlayerDetailPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.labels: dict[str, QLabel] = {}

        layout = QVBoxLayout(self)

        self.title_label = QLabel("No player selected")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.title_label)

        layout.addWidget(self._make_group("Basic", [
            ("Name", "name"),
            ("Position", "position"),
            ("Age", "age"),
        ]))

        layout.addWidget(self._make_group("Technical", [
            ("Passing", "passing"),
            ("First touch", "first_touch"),
            ("Technique", "technique"),
            ("Dribbling", "dribbling"),
            ("Finishing", "finishing"),
            ("Long shots", "long_shots"),
            ("Tackling", "tackling"),
            ("Heading", "heading"),
            ("Crossing", "crossing"),
        ]))

        layout.addWidget(self._make_group("Mental / Tactical", [
            ("Positioning", "positioning"),
            ("Vision", "vision"),
            ("Decision making", "decision_making"),
            ("Anticipation", "anticipation"),
            ("Composure", "composure"),
            ("Concentration", "concentration"),
            ("Work rate", "work_rate"),
            ("Discipline", "discipline"),
            ("Aggression", "aggression"),
        ]))

        layout.addWidget(self._make_group("Physical", [
            ("Pace", "pace"),
            ("Acceleration", "acceleration"),
            ("Agility", "agility"),
            ("Strength", "strength"),
            ("Stamina", "stamina"),
            ("Jumping", "jumping"),
        ]))

        layout.addWidget(self._make_group("Status", [
            ("Fatigue", "fatigue"),
            ("Fitness", "fitness"),
            ("Morale", "morale"),
            ("Familiarity", "familiarity"),
            ("Confidence", "confidence"),
            ("Sharpness", "sharpness"),
            ("Injury proneness", "injury_proneness"),
            ("Injured", "injured"),
        ]))

        layout.addWidget(self._make_group("Career / Value", [
            ("Current ability", "current_ability"),
            ("Potential", "potential"),
            ("Wage", "wage"),
            ("Contract weeks", "contract_weeks"),
            ("Market value", "market_value"),
        ]))

        layout.addStretch()

        self.setStyleSheet("""
            QWidget {
                color: white;
                background-color: rgba(10, 15, 25, 170);
                border-radius: 10px;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid rgba(255, 255, 255, 40);
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: rgba(10, 15, 25, 120);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 4px 0 4px;
            }
            QLabel {
                background: transparent;
                border: none;
            }
        """)

    def _make_group(self, title: str, fields: list[tuple[str, str]]) -> QGroupBox:
        box = QGroupBox(title)
        form = QFormLayout(box)

        for label_text, key in fields:
            value_label = QLabel("-")
            value_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.labels[key] = value_label
            form.addRow(f"{label_text}:", value_label)

        return box

    def _set_number(self, key: str, value: float | int) -> None:
        self.labels[key].setText(f"{value:.1f}" if isinstance(value, float) else str(value))

    def set_player(self, player: Player | None) -> None:
        if player is None:
            self.title_label.setText("No player selected")
            for label in self.labels.values():
                label.setText("-")
            return

        age = getattr(player, "age", 24)
        wage = getattr(player, "wage", 0)
        contract_weeks = getattr(player, "contract_weeks", 0)
        potential = getattr(player, "potential", current_ability(player))

        self.title_label.setText(player.name)

        self.labels["name"].setText(player.name)
        self.labels["position"].setText(player.position)
        self.labels["age"].setText(str(age))

        for key in [
            "passing", "first_touch", "technique", "dribbling", "finishing",
            "long_shots", "tackling", "heading", "crossing",
            "positioning", "vision", "decision_making", "anticipation",
            "composure", "concentration", "work_rate", "discipline", "aggression",
            "pace", "acceleration", "agility", "strength", "stamina", "jumping",
            "fatigue", "fitness", "morale", "familiarity", "confidence",
            "sharpness", "injury_proneness",
        ]:
            self.labels[key].setText(f"{getattr(player, key):.1f}")

        self.labels["injured"].setText("Yes" if player.injured else "No")
        self.labels["current_ability"].setText(f"{current_ability(player):.1f}")
        self.labels["potential"].setText(f"{potential:.1f}")
        self.labels["wage"].setText(f"{wage:,}")
        self.labels["contract_weeks"].setText(str(contract_weeks))
        self.labels["market_value"].setText(f"{estimate_market_value(player):,}")


class SquadTableWidget(QTableWidget):
    COLUMN_HEADERS = [
        "Name",
        "Pos",
        "Age",
        "CA",
        "Pot",
        "Fit",
        "Fat",
        "Mor",
        "Value",
    ]

    def __init__(self, on_player_selected) -> None:
        super().__init__()
        self.on_player_selected = on_player_selected
        self.players: list[Player] = []

        self.setColumnCount(len(self.COLUMN_HEADERS))
        self.setHorizontalHeaderLabels(self.COLUMN_HEADERS)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSortingEnabled(True)
        self.verticalHeader().setVisible(False)

        self.itemSelectionChanged.connect(self._handle_selection_changed)

        header = self.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        for col in range(1, len(self.COLUMN_HEADERS)):
            header.setSectionResizeMode(col, QHeaderView.ResizeToContents)

        self.setStyleSheet("""
            QTableWidget {
                background-color: rgba(15, 20, 30, 210);
                color: white;
                gridline-color: rgba(255, 255, 255, 40);
                border: 1px solid rgba(255, 255, 255, 50);
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: rgba(30, 40, 55, 220);
                color: white;
                padding: 6px;
                border: none;
                border-bottom: 1px solid rgba(255, 255, 255, 40);
            }
            QTableWidget::item:selected {
                background-color: rgba(90, 130, 190, 180);
            }
        """)

    def load_players(self, players: list[Player]) -> None:
        self.setSortingEnabled(False)
        self.players = players
        self.setRowCount(len(players))

        for row, player in enumerate(players):
            age = getattr(player, "age", 24)
            potential = getattr(player, "potential", current_ability(player))

            values = [
                player.name,
                player.position,
                str(age),
                f"{current_ability(player):.1f}",
                f"{potential:.1f}",
                f"{player.fitness:.1f}",
                f"{player.fatigue:.1f}",
                f"{player.morale:.1f}",
                f"{estimate_market_value(player):,}",
            ]

            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setData(Qt.UserRole, player)

                if col >= 2:
                    item.setTextAlignment(Qt.AlignCenter)

                if player.injured:
                    item.setBackground(QColor(255, 220, 220))
                elif player.fatigue >= 70:
                    item.setBackground(QColor(255, 245, 200))
                elif player.fitness <= 60:
                    item.setBackground(QColor(255, 235, 200))

                self.setItem(row, col, item)

        self.setSortingEnabled(True)

        if players:
            self.selectRow(0)
            self.on_player_selected(players[0])

    def _handle_selection_changed(self) -> None:
        selected_items = self.selectedItems()
        if not selected_items:
            return

        player = selected_items[0].data(Qt.UserRole)
        if player is not None:
            self.on_player_selected(player)


class TeamOverviewWidget(QWidget):
    def __init__(self, club: Club) -> None:
        super().__init__()
        self.club = club

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Horizontal)

        self.squad_table = SquadTableWidget(self._on_player_selected)
        self.detail_panel = PlayerDetailPanel()

        detail_scroll = QScrollArea()
        detail_scroll.setWidgetResizable(True)
        detail_scroll.setWidget(self.detail_panel)
        detail_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        splitter.addWidget(self.squad_table)
        splitter.addWidget(detail_scroll)
        splitter.setSizes([700, 350])

        outer_layout.addWidget(splitter)

        self.refresh()

    def refresh(self) -> None:
        self.squad_table.load_players(self.club.team.squad)

    def _on_player_selected(self, player: Player) -> None:
        self.detail_panel.set_player(player)


class PlaceholderPage(QWidget):
    def __init__(self, title: str, text: str) -> None:
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: white;
            background: transparent;
        """)

        text_label = QLabel(text)
        text_label.setWordWrap(True)
        text_label.setStyleSheet("""
            font-size: 14px;
            color: rgba(255, 255, 255, 210);
            background: transparent;
        """)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(10, 15, 25, 170);
                border: 1px solid rgba(255, 255, 255, 40);
                border-radius: 10px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.addWidget(title_label)
        card_layout.addSpacing(8)
        card_layout.addWidget(text_label)
        card_layout.addStretch()

        layout.addWidget(card)
        layout.addStretch()