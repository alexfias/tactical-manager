from __future__ import annotations

import json
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from tactical_manager.core.data import parse_club
from tactical_manager.core.models import Club, Player
from tactical_manager.editor.state import EditorState
from tactical_manager.editor.validators import validate_club
from tactical_manager.editor.widgets.club_details_widget import ClubDetailsWidget
from tactical_manager.editor.widgets.player_form_widget import PlayerFormWidget
from tactical_manager.editor.widgets.squad_table_widget import SquadTableWidget


class ClubEditorWindow(QMainWindow):
    def __init__(self, clubs_dir: Path) -> None:
        super().__init__()

        self.setWindowTitle("Tactical Manager Editor")
        self.resize(1400, 800)

        self.clubs_dir = clubs_dir
        self.state = EditorState()

        self.club_list = QListWidget()
        self.club_list.currentItemChanged.connect(self.on_club_selected)

        self.club_details = ClubDetailsWidget()

        self.squad_table = SquadTableWidget()
        self.squad_table.itemSelectionChanged.connect(self.on_player_selected)

        self.player_form = PlayerFormWidget()

        self.validation_box = QTextEdit()
        self.validation_box.setReadOnly(True)

        self.status_label = QLabel("Ready")

        self.load_button = QPushButton("Open File...")
        self.load_button.clicked.connect(self.open_file_dialog)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_current_club)

        self.save_as_button = QPushButton("Save As...")
        self.save_as_button.clicked.connect(self.save_as_current_club)

        self.validate_button = QPushButton("Validate")
        self.validate_button.clicked.connect(self.run_validation)

        self.add_player_button = QPushButton("Add Player")
        self.add_player_button.clicked.connect(self.add_player)

        self.remove_player_button = QPushButton("Remove Player")
        self.remove_player_button.clicked.connect(self.remove_selected_player)

        self.apply_player_button = QPushButton("Apply Player Changes")
        self.apply_player_button.clicked.connect(self.apply_player_changes)

        self.apply_club_button = QPushButton("Apply Club Changes")
        self.apply_club_button.clicked.connect(self.apply_club_changes)

        self._build_ui()
        self.load_club_list()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout()
        central.setLayout(root)

        left = QVBoxLayout()
        left.addWidget(QLabel("Club Files"))
        left.addWidget(self.club_list)
        left.addWidget(self.load_button)

        middle = QVBoxLayout()
        middle.addWidget(self.club_details)
        middle.addWidget(self.apply_club_button)
        middle.addWidget(QLabel("Squad"))
        middle.addWidget(self.squad_table)

        squad_actions = QHBoxLayout()
        squad_actions.addWidget(self.add_player_button)
        squad_actions.addWidget(self.remove_player_button)
        middle.addLayout(squad_actions)

        right = QVBoxLayout()
        right.addWidget(self.player_form)
        right.addWidget(self.apply_player_button)
        right.addWidget(QLabel("Validation"))
        right.addWidget(self.validation_box)
        right.addWidget(self.validate_button)
        right.addWidget(self.save_button)
        right.addWidget(self.save_as_button)
        right.addWidget(self.status_label)

        root.addLayout(left, 1)
        root.addLayout(middle, 2)
        root.addLayout(right, 2)

    def load_club_list(self) -> None:
        self.club_list.clear()
        self.clubs_dir.mkdir(parents=True, exist_ok=True)

        for path in sorted(self.clubs_dir.glob("*.json")):
            item = QListWidgetItem(path.stem)
            item.setData(Qt.UserRole, path)
            self.club_list.addItem(item)

    def on_club_selected(self, current: QListWidgetItem | None, previous: QListWidgetItem | None) -> None:
        if current is None:
            return

        path = current.data(Qt.UserRole)
        if not isinstance(path, Path):
            return

        self.load_club_file(path)

    def load_club_file(self, path: Path) -> None:
        try:
            with path.open("r", encoding="utf-8") as f:
                raw = json.load(f)
            club = parse_club(raw)
        except Exception as exc:
            QMessageBox.critical(self, "Load Error", f"Could not load club file:\n{path}\n\n{exc}")
            return

        self.state.current_file = path
        self.state.current_club = club
        self.state.selected_player_index = None
        self.state.dirty = False

        self.club_details.load_club(club)
        self.squad_table.load_players(club.team.squad)
        self.validation_box.clear()
        self.status_label.setText(f"Loaded: {path.name}")

    def open_file_dialog(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open club JSON",
            str(self.clubs_dir),
            "JSON Files (*.json)",
        )
        if file_name:
            self.load_club_file(Path(file_name))

    def on_player_selected(self) -> None:
        club = self.state.current_club
        if club is None:
            return

        selected = self.squad_table.selectionModel().selectedRows()
        if not selected:
            return

        row = selected[0].row()
        self.state.selected_player_index = row
        self.player_form.load_player(club.team.squad[row])

    def apply_club_changes(self) -> None:
        club = self.state.current_club
        if club is None:
            return

        self.club_details.apply_to_club(club)
        self.state.dirty = True
        self.status_label.setText("Club changes applied.")

    def apply_player_changes(self) -> None:
        club = self.state.current_club
        idx = self.state.selected_player_index

        if club is None or idx is None:
            return

        self.player_form.apply_to_player(club.team.squad[idx])
        self.squad_table.load_players(club.team.squad)
        self.squad_table.selectRow(idx)
        self.state.dirty = True
        self.status_label.setText("Player changes applied.")

    def add_player(self) -> None:
        club = self.state.current_club
        if club is None:
            return

        player = Player(
            name="New Player",
            position="MID",
            attack=50,
            defense=50,
            passing=50,
            stamina=50,
            morale=50,
            form=50,
            wage=1000,
            market_value=100000,
            age=22,
            contract_weeks=52,
            potential=60,
        )
        club.team.squad.append(player)
        self.squad_table.load_players(club.team.squad)
        self.squad_table.selectRow(len(club.team.squad) - 1)
        self.state.dirty = True
        self.status_label.setText("Player added.")

    def remove_selected_player(self) -> None:
        club = self.state.current_club
        idx = self.state.selected_player_index

        if club is None or idx is None:
            return

        removed = club.team.squad.pop(idx)
        self.state.selected_player_index = None
        self.squad_table.load_players(club.team.squad)
        self.validation_box.append(f"Removed player: {removed.name}")
        self.state.dirty = True
        self.status_label.setText("Player removed.")

    def run_validation(self) -> None:
        club = self.state.current_club
        if club is None:
            return

        self.apply_club_changes()
        if self.state.selected_player_index is not None:
            self.apply_player_changes()

        errors = validate_club(club)
        self.validation_box.clear()

        if errors:
            self.validation_box.setPlainText("\n".join(f"- {e}" for e in errors))
            self.status_label.setText(f"Validation failed: {len(errors)} issue(s)")
        else:
            self.validation_box.setPlainText("No validation errors.")
            self.status_label.setText("Validation passed.")

    def save_current_club(self) -> None:
        club = self.state.current_club
        path = self.state.current_file

        if club is None or path is None:
            self.save_as_current_club()
            return

        self.apply_club_changes()
        if self.state.selected_player_index is not None:
            self.apply_player_changes()

        errors = validate_club(club)
        if errors:
            QMessageBox.warning(
                self,
                "Validation Failed",
                "Cannot save because validation failed.\n\n" + "\n".join(errors),
            )
            return

        try:
            payload = self.club_to_dict(club)
            with path.open("w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
            self.state.dirty = False
            self.status_label.setText(f"Saved: {path.name}")
            self.load_club_list()
        except Exception as exc:
            QMessageBox.critical(self, "Save Error", f"Could not save file:\n{path}\n\n{exc}")

    def save_as_current_club(self) -> None:
        club = self.state.current_club
        if club is None:
            return

        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save club JSON",
            str(self.clubs_dir / "new_club.json"),
            "JSON Files (*.json)",
        )
        if not file_name:
            return

        self.state.current_file = Path(file_name)
        self.save_current_club()

    def club_to_dict(self, club: Club) -> dict:
        return {
            "name": club.identity.name,
            "reputation": club.identity.reputation,
            "team": {
                "name": club.team.name,
                "squad": [
                    {
                        "name": p.name,
                        "position": p.position,
                        "attack": p.attack,
                        "defense": p.defense,
                        "passing": p.passing,
                        "stamina": p.stamina,
                        "morale": p.morale,
                        "form": p.form,
                        "wage": p.wage,
                        "market_value": p.market_value,
                        "age": p.age,
                        "contract_weeks": p.contract_weeks,
                        "potential": p.potential,
                    }
                    for p in club.team.squad
                ],
            },
            "finance": {
                "balance": club.finance.balance,
                "transfer_budget": club.finance.transfer_budget,
                "weekly_wages": club.finance.weekly_wages,
                "wage_budget": club.finance.wage_budget,
                "sponsorship_income": club.finance.sponsorship_income,
                "matchday_base_income": club.finance.matchday_base_income,
            },
            "infrastructure": {
                "stadium_capacity": club.infrastructure.stadium_capacity,
                "ticket_price": club.infrastructure.ticket_price,
                "training_level": club.infrastructure.training_level,
                "youth_level": club.infrastructure.youth_level,
                "medical_level": club.infrastructure.medical_level,
            },
            "support": {
                "fan_mood": club.support.fan_mood,
                "expectation": club.support.expectation,
            },
            "board": {
                "patience": club.board.patience,
                "confidence": club.board.confidence,
            },
        }