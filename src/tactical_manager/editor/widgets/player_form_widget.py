from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QLineEdit,
)


class PlayerFormWidget(QGroupBox):
    def __init__(self) -> None:
        super().__init__("Player Details")

        self.name_edit = QLineEdit()

        self.position_combo = QComboBox()
        self.position_combo.addItems(["GK", "DEF", "MID", "ATT"])

        self.passing_spin = self._rating_spin()
        self.technique_spin = self._rating_spin()
        self.finishing_spin = self._rating_spin()
        self.defending_spin = self._rating_spin()
        self.positioning_spin = self._rating_spin()
        self.pace_spin = self._rating_spin()
        self.stamina_spin = self._rating_spin()
        self.work_rate_spin = self._rating_spin()
        self.fatigue_spin = self._rating_spin()
        self.fitness_spin = self._rating_spin()
        self.morale_spin = self._rating_spin()
        self.familiarity_spin = self._rating_spin()
        self.injury_proneness_spin = self._rating_spin()

        self.injured_check = QCheckBox()

        layout = QFormLayout()
        layout.addRow("Name", self.name_edit)
        layout.addRow("Position", self.position_combo)
        layout.addRow("Passing", self.passing_spin)
        layout.addRow("Technique", self.technique_spin)
        layout.addRow("Finishing", self.finishing_spin)
        layout.addRow("Defending", self.defending_spin)
        layout.addRow("Positioning", self.positioning_spin)
        layout.addRow("Pace", self.pace_spin)
        layout.addRow("Stamina", self.stamina_spin)
        layout.addRow("Work Rate", self.work_rate_spin)
        layout.addRow("Fatigue", self.fatigue_spin)
        layout.addRow("Fitness", self.fitness_spin)
        layout.addRow("Morale", self.morale_spin)
        layout.addRow("Familiarity", self.familiarity_spin)
        layout.addRow("Injury Proneness", self.injury_proneness_spin)
        layout.addRow("Injured", self.injured_check)
        self.setLayout(layout)

    def _rating_spin(self) -> QDoubleSpinBox:
        spin = QDoubleSpinBox()
        spin.setRange(0, 100)
        spin.setDecimals(1)
        return spin

    def load_player(self, player) -> None:
        self.name_edit.setText(player.name)
        self.position_combo.setCurrentText(player.position)
        self.passing_spin.setValue(player.passing)
        self.technique_spin.setValue(player.technique)
        self.finishing_spin.setValue(player.finishing)
        self.defending_spin.setValue(player.defending)
        self.positioning_spin.setValue(player.positioning)
        self.pace_spin.setValue(player.pace)
        self.stamina_spin.setValue(player.stamina)
        self.work_rate_spin.setValue(player.work_rate)
        self.fatigue_spin.setValue(player.fatigue)
        self.fitness_spin.setValue(player.fitness)
        self.morale_spin.setValue(player.morale)
        self.familiarity_spin.setValue(player.familiarity)
        self.injury_proneness_spin.setValue(player.injury_proneness)
        self.injured_check.setChecked(player.injured)

    def apply_to_player(self, player) -> None:
        player.name = self.name_edit.text().strip()
        player.position = self.position_combo.currentText()
        player.passing = self.passing_spin.value()
        player.technique = self.technique_spin.value()
        player.finishing = self.finishing_spin.value()
        player.defending = self.defending_spin.value()
        player.positioning = self.positioning_spin.value()
        player.pace = self.pace_spin.value()
        player.stamina = self.stamina_spin.value()
        player.work_rate = self.work_rate_spin.value()
        player.fatigue = self.fatigue_spin.value()
        player.fitness = self.fitness_spin.value()
        player.morale = self.morale_spin.value()
        player.familiarity = self.familiarity_spin.value()
        player.injury_proneness = self.injury_proneness_spin.value()
        player.injured = self.injured_check.isChecked()