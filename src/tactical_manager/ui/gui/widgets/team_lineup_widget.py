from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from tactical_manager.core.models import Club, Player
from tactical_manager.ui.gui.widgets.team_overview_widget import current_ability


def role_score(player: Player, role: str) -> float:
    role = role.upper()

    if role == "GK":
        return (
            0.30 * player.positioning
            + 0.20 * player.concentration
            + 0.15 * player.composure
            + 0.15 * player.jumping
            + 0.10 * player.decision_making
            + 0.10 * player.strength
        )

    if role in {"LB", "RB"}:
        return (
            0.20 * player.tackling
            + 0.15 * player.positioning
            + 0.15 * player.pace
            + 0.10 * player.acceleration
            + 0.10 * player.stamina
            + 0.10 * player.crossing
            + 0.10 * player.work_rate
            + 0.10 * player.anticipation
        )

    if role in {"CB1", "CB2", "CB"}:
        return (
            0.25 * player.tackling
            + 0.20 * player.positioning
            + 0.15 * player.heading
            + 0.15 * player.strength
            + 0.10 * player.jumping
            + 0.10 * player.concentration
            + 0.05 * player.composure
        )

    if role in {"LM", "RM"}:
        return (
            0.18 * player.pace
            + 0.14 * player.acceleration
            + 0.14 * player.dribbling
            + 0.12 * player.crossing
            + 0.12 * player.stamina
            + 0.10 * player.work_rate
            + 0.10 * player.technique
            + 0.10 * player.passing
        )

    if role in {"CM1", "CM2", "CM"}:
        return (
            0.18 * player.passing
            + 0.15 * player.vision
            + 0.15 * player.decision_making
            + 0.12 * player.positioning
            + 0.10 * player.stamina
            + 0.10 * player.technique
            + 0.10 * player.composure
            + 0.10 * player.work_rate
        )

    if role in {"ST1", "ST2", "ST"}:
        return (
            0.25 * player.finishing
            + 0.15 * player.positioning
            + 0.15 * player.first_touch
            + 0.10 * player.technique
            + 0.10 * player.composure
            + 0.10 * player.pace
            + 0.10 * player.acceleration
            + 0.05 * player.heading
        )

    return current_ability(player)


class PitchSlotButton(QPushButton):
    def __init__(self, role: str) -> None:
        super().__init__()
        self.role = role
        self.player: Player | None = None
        self.setCheckable(True)
        self.setMinimumSize(120, 68)
        self.refresh_text()

    def set_player(self, player: Player | None) -> None:
        self.player = player
        self.refresh_text()

    def refresh_text(self) -> None:
        if self.player is None:
            self.setText(f"{self.role}\n[Empty]")
        else:
            self.setText(
                f"{self.role}\n"
                f"{self.player.name}\n"
                f"Fit {self.player.fitness:.0f} | Mor {self.player.morale:.0f}"
            )


class PitchWidget(QWidget):
    SLOT_POSITIONS = {
        "ST1": (0, 1),
        "ST2": (0, 3),
        "LM": (1, 0),
        "CM1": (1, 1),
        "CM2": (1, 3),
        "RM": (1, 4),
        "LB": (2, 0),
        "CB1": (2, 1),
        "CB2": (2, 3),
        "RB": (2, 4),
        "GK": (3, 2),
    }

    def __init__(self, on_slot_selected) -> None:
        super().__init__()
        self.on_slot_selected = on_slot_selected
        self.slot_buttons: dict[str, PitchSlotButton] = {}

        layout = QGridLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(28)

        for role, (row, col) in self.SLOT_POSITIONS.items():
            button = PitchSlotButton(role)
            button.clicked.connect(self._make_slot_handler(role))
            self.slot_buttons[role] = button
            layout.addWidget(button, row, col)

        self.setStyleSheet("""
            PitchWidget {
                background-color: rgba(20, 100, 45, 170);
                border: 2px solid rgba(255, 255, 255, 70);
                border-radius: 12px;
            }
            QPushButton {
                background-color: rgba(20, 35, 60, 210);
                color: white;
                border: 1px solid rgba(255,255,255,70);
                border-radius: 8px;
                padding: 6px;
                font-weight: bold;
                text-align: center;
            }
            QPushButton:checked {
                background-color: rgba(80, 130, 200, 220);
                border: 2px solid rgba(255, 255, 255, 120);
            }
        """)

    def _make_slot_handler(self, role: str):
        def handler() -> None:
            for other_role, button in self.slot_buttons.items():
                if other_role != role:
                    button.setChecked(False)
            self.on_slot_selected(role)
        return handler

    def set_lineup(self, lineup_slots: dict[str, Player | None]) -> None:
        for role, button in self.slot_buttons.items():
            button.set_player(lineup_slots.get(role))

    def clear_selection(self) -> None:
        for button in self.slot_buttons.values():
            button.setChecked(False)


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
        self.setSortingEnabled(True)

        self.itemSelectionChanged.connect(self._handle_selection_changed)

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        for col in range(1, len(self.HEADERS)):
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

    def load_players(self, players: list[Player], selected_players: set[int] | None = None) -> None:
        selected_players = selected_players or set()

        self.setSortingEnabled(False)
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

                if col >= 2:
                    item.setTextAlignment(Qt.AlignCenter)

                if id(player) in selected_players:
                    item.setBackground(QColor(50, 90, 50))
                elif player.injured:
                    item.setBackground(QColor(255, 220, 220))
                elif player.fatigue >= 70:
                    item.setBackground(QColor(255, 245, 200))
                elif player.fitness <= 60:
                    item.setBackground(QColor(255, 235, 200))

                self.setItem(row, col, item)

        self.setSortingEnabled(True)

    def selected_player(self) -> Player | None:
        items = self.selectedItems()
        if not items:
            return None
        return items[0].data(Qt.UserRole)

    def _handle_selection_changed(self) -> None:
        player = self.selected_player()
        if player is not None:
            self.on_player_selected(player)


class TeamLineupWidget(QWidget):
    DEFAULT_ROLES = ["GK", "LB", "CB1", "CB2", "RB", "LM", "CM1", "CM2", "RM", "ST1", "ST2"]

    def __init__(self, club: Club) -> None:
        super().__init__()
        self.club = club

        self.lineup_slots: dict[str, Player | None] = {
            role: None for role in self.DEFAULT_ROLES
        }
        self.selected_role: str | None = None
        self.selected_player: Player | None = None

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Horizontal)

        self.pitch_widget = PitchWidget(self.on_slot_selected)
        splitter.addWidget(self.pitch_widget)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        self.selection_box = QGroupBox("Selection")
        selection_form = QFormLayout(self.selection_box)
        self.role_label = QLabel("-")
        self.slot_player_label = QLabel("-")
        self.chosen_player_label = QLabel("-")
        self.fit_score_label = QLabel("-")
        selection_form.addRow("Slot:", self.role_label)
        selection_form.addRow("Current:", self.slot_player_label)
        selection_form.addRow("Chosen player:", self.chosen_player_label)
        selection_form.addRow("Role fit:", self.fit_score_label)

        right_layout.addWidget(self.selection_box)

        self.players_table = AvailablePlayersTable(self.on_player_selected)
        right_layout.addWidget(self.players_table)

        self.assign_button = QPushButton("Assign to Slot")
        self.assign_button.clicked.connect(self.assign_selected_player)

        self.remove_button = QPushButton("Remove from Slot")
        self.remove_button.clicked.connect(self.remove_selected_slot_player)

        self.auto_pick_button = QPushButton("Auto Pick Best XI")
        self.auto_pick_button.clicked.connect(self.auto_pick_best_xi)

        right_layout.addWidget(self.assign_button)
        right_layout.addWidget(self.remove_button)
        right_layout.addWidget(self.auto_pick_button)
        right_layout.addStretch()

        right_widget.setStyleSheet("""
            QWidget {
                color: white;
                background-color: rgba(10, 15, 25, 150);
                border-radius: 10px;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid rgba(255, 255, 255, 40);
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: rgba(10, 15, 25, 100);
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
            QPushButton {
                background-color: rgba(35, 55, 85, 200);
                color: white;
                padding: 10px;
                border-radius: 8px;
                border: 1px solid rgba(255,255,255,60);
            }
            QPushButton:hover {
                background-color: rgba(55, 85, 125, 220);
            }
        """)

        splitter.addWidget(right_widget)
        splitter.setSizes([700, 360])

        root_layout.addWidget(splitter)

        self.load_existing_lineup()
        self.refresh()

    def refresh(self) -> None:
        self.load_existing_lineup()
        self.refresh_pitch()
        selected_players = {id(player) for player in self.lineup_slots.values() if player is not None}
        self.players_table.load_players(self.club.team.squad, selected_players=selected_players)
        self.refresh_selection_box()

    def load_existing_lineup(self) -> None:
        for role in self.DEFAULT_ROLES:
            self.lineup_slots[role] = None

        lineup_by_role = getattr(self.club.team, "lineup_by_role", None)
        if isinstance(lineup_by_role, dict) and lineup_by_role:
            for role in self.DEFAULT_ROLES:
                self.lineup_slots[role] = lineup_by_role.get(role)
            return

        starting_xi = getattr(self.club.team, "starting_xi", [])
        for role, player in zip(self.DEFAULT_ROLES, starting_xi):
            self.lineup_slots[role] = player

    def refresh_pitch(self) -> None:
        self.pitch_widget.set_lineup(self.lineup_slots)

    def refresh_selection_box(self) -> None:
        self.role_label.setText(self.selected_role or "-")

        slot_player = self.lineup_slots.get(self.selected_role) if self.selected_role else None
        self.slot_player_label.setText(slot_player.name if slot_player else "[Empty]")

        self.chosen_player_label.setText(self.selected_player.name if self.selected_player else "-")

        if self.selected_role and self.selected_player:
            self.fit_score_label.setText(f"{role_score(self.selected_player, self.selected_role):.1f}")
        else:
            self.fit_score_label.setText("-")

    def on_slot_selected(self, role: str) -> None:
        self.selected_role = role
        self.refresh_selection_box()

    def on_player_selected(self, player: Player) -> None:
        self.selected_player = player
        self.refresh_selection_box()

    def assign_selected_player(self) -> None:
        if self.selected_role is None or self.selected_player is None:
            return

        for role, player in self.lineup_slots.items():
            if player is self.selected_player:
                self.lineup_slots[role] = None

        self.lineup_slots[self.selected_role] = self.selected_player
        self._write_back_starting_xi()
        self.refresh()

    def remove_selected_slot_player(self) -> None:
        if self.selected_role is None:
            return

        self.lineup_slots[self.selected_role] = None
        self._write_back_starting_xi()
        self.refresh()

    def auto_pick_best_xi(self) -> None:
        remaining_players = list(self.club.team.squad)
        new_slots: dict[str, Player | None] = {}

        for role in self.DEFAULT_ROLES:
            if not remaining_players:
                new_slots[role] = None
                continue

            best_player = max(remaining_players, key=lambda p: role_score(p, role))
            new_slots[role] = best_player
            remaining_players.remove(best_player)

        self.lineup_slots = new_slots
        self._write_back_starting_xi()
        self.refresh()

    def _write_back_starting_xi(self) -> None:
        self.club.team.lineup_by_role = {
            role: self.lineup_slots[role]
            for role in self.DEFAULT_ROLES
        }

        self.club.team.starting_xi = [
            self.lineup_slots[role]
            for role in self.DEFAULT_ROLES
            if self.lineup_slots[role] is not None
        ]