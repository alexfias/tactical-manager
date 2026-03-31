from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QLineEdit,
    QSpinBox,
)

from tactical_manager.core.models import Player


class PlayerFormWidget(QGroupBox):
    def __init__(self) -> None:
        super().__init__("Player Details")

        self.name_edit = QLineEdit()

        self.position_combo = QComboBox()
        self.position_combo.addItems(["GK", "DEF", "MID", "ATT"])

        self.attack_spin = self._rating_spin()
        self.defense_spin = self._rating_spin()
        self.passing_spin = self._rating_spin()
        self.stamina_spin = self._rating_spin()
        self.morale_spin = self._rating_spin()
        self.form_spin = self._rating_spin()
        self.potential_spin = self._rating_spin()

        self.age_spin = QSpinBox()
        self.age_spin.setRange(14, 50)

        self.wage_spin = QSpinBox()
        self.wage_spin.setRange(0, 10_000_000)

        self.market_value_spin = QSpinBox()
        self.market_value_spin.setRange(0, 1_000_000_000)

        self.contract_weeks_spin = QSpinBox()
        self.contract_weeks_spin.setRange(0, 1000)

        layout = QFormLayout()
        layout.addRow("Name", self.name_edit)
        layout.addRow("Position", self.position_combo)
        layout.addRow("Attack", self.attack_spin)
        layout.addRow("Defense", self.defense_spin)
        layout.addRow("Passing", self.passing_spin)
        layout.addRow("Stamina", self.stamina_spin)
        layout.addRow("Morale", self.morale_spin)
        layout.addRow("Form", self.form_spin)
        layout.addRow("Potential", self.potential_spin)
        layout.addRow("Age", self.age_spin)
        layout.addRow("Wage", self.wage_spin)
        layout.addRow("Market Value", self.market_value_spin)
        layout.addRow("Contract Weeks", self.contract_weeks_spin)
        self.setLayout(layout)

    def _rating_spin(self) -> QSpinBox:
        spin = QSpinBox()
        spin.setRange(0, 100)
        return spin

    def load_player(self, player: Player) -> None:
        self.name_edit.setText(player.name)
        self.position_combo.setCurrentText(player.position)
        self.attack_spin.setValue(player.attack)
        self.defense_spin.setValue(player.defense)
        self.passing_spin.setValue(player.passing)
        self.stamina_spin.setValue(player.stamina)
        self.morale_spin.setValue(player.morale)
        self.form_spin.setValue(player.form)
        self.potential_spin.setValue(player.potential)
        self.age_spin.setValue(player.age)
        self.wage_spin.setValue(player.wage)
        self.market_value_spin.setValue(player.market_value)
        self.contract_weeks_spin.setValue(player.contract_weeks)

    def apply_to_player(self, player: Player) -> None:
        player.name = self.name_edit.text().strip()
        player.position = self.position_combo.currentText()
        player.attack = self.attack_spin.value()
        player.defense = self.defense_spin.value()
        player.passing = self.passing_spin.value()
        player.stamina = self.stamina_spin.value()
        player.morale = self.morale_spin.value()
        player.form = self.form_spin.value()
        player.potential = self.potential_spin.value()
        player.age = self.age_spin.value()
        player.wage = self.wage_spin.value()
        player.market_value = self.market_value_spin.value()
        player.contract_weeks = self.contract_weeks_spin.value()