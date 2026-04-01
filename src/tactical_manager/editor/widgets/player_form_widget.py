from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from tactical_manager.core.player_valuation import current_ability, estimate_market_value


class PlayerFormWidget(QGroupBox):
    def __init__(self) -> None:
        super().__init__("Player Details")

        # ---------- basic ----------
        self.name_edit = QLineEdit()

        self.position_combo = QComboBox()
        self.position_combo.addItems(["GK", "DEF", "MID", "ATT"])

        self.age_spin = QSpinBox()
        self.age_spin.setRange(15, 45)

        self.potential_spin = self._rating_spin()

        self.ca_label = QLabel("-")
        self.value_label = QLabel("-")

        # ---------- technical ----------
        self.passing_spin = self._rating_spin()
        self.first_touch_spin = self._rating_spin()
        self.technique_spin = self._rating_spin()
        self.dribbling_spin = self._rating_spin()
        self.finishing_spin = self._rating_spin()
        self.long_shots_spin = self._rating_spin()
        self.tackling_spin = self._rating_spin()
        self.heading_spin = self._rating_spin()
        self.crossing_spin = self._rating_spin()

        # ---------- mental / tactical ----------
        self.positioning_spin = self._rating_spin()
        self.vision_spin = self._rating_spin()
        self.decision_making_spin = self._rating_spin()
        self.anticipation_spin = self._rating_spin()
        self.composure_spin = self._rating_spin()
        self.concentration_spin = self._rating_spin()
        self.work_rate_spin = self._rating_spin()
        self.discipline_spin = self._rating_spin()
        self.aggression_spin = self._rating_spin()

        # ---------- physical ----------
        self.pace_spin = self._rating_spin()
        self.acceleration_spin = self._rating_spin()
        self.agility_spin = self._rating_spin()
        self.strength_spin = self._rating_spin()
        self.stamina_spin = self._rating_spin()
        self.jumping_spin = self._rating_spin()

        # ---------- contract / state ----------
        self.contract_weeks_spin = QSpinBox()
        self.contract_weeks_spin.setRange(0, 520)

        self.fatigue_spin = self._rating_spin()
        self.fitness_spin = self._rating_spin()
        self.morale_spin = self._rating_spin()
        self.familiarity_spin = self._rating_spin()
        self.confidence_spin = self._rating_spin()
        self.sharpness_spin = self._rating_spin()
        self.injury_proneness_spin = self._rating_spin()

        self.injured_check = QCheckBox()

        # ---------- build grouped layout ----------
        content = QWidget()
        content_layout = QVBoxLayout(content)

        content_layout.addWidget(self._build_basic_group())
        content_layout.addWidget(self._build_technical_group())
        content_layout.addWidget(self._build_mental_group())
        content_layout.addWidget(self._build_physical_group())
        content_layout.addWidget(self._build_state_group())

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content)

        outer_layout = QVBoxLayout()
        outer_layout.addWidget(scroll)
        self.setLayout(outer_layout)

    def _rating_spin(self) -> QDoubleSpinBox:
        spin = QDoubleSpinBox()
        spin.setRange(0.0, 100.0)
        spin.setDecimals(1)
        spin.setSingleStep(1.0)
        return spin

    def _build_basic_group(self) -> QGroupBox:
        group = QGroupBox("Basic")
        layout = QFormLayout()
        layout.addRow("Name", self.name_edit)
        layout.addRow("Position", self.position_combo)
        layout.addRow("Age", self.age_spin)
        layout.addRow("Potential", self.potential_spin)
        layout.addRow("Current Ability", self.ca_label)
        layout.addRow("Market Value", self.value_label)
        group.setLayout(layout)
        return group

    def _build_technical_group(self) -> QGroupBox:
        group = QGroupBox("Technical")
        layout = QFormLayout()
        layout.addRow("Passing", self.passing_spin)
        layout.addRow("First Touch", self.first_touch_spin)
        layout.addRow("Technique", self.technique_spin)
        layout.addRow("Dribbling", self.dribbling_spin)
        layout.addRow("Finishing", self.finishing_spin)
        layout.addRow("Long Shots", self.long_shots_spin)
        layout.addRow("Tackling", self.tackling_spin)
        layout.addRow("Heading", self.heading_spin)
        layout.addRow("Crossing", self.crossing_spin)
        group.setLayout(layout)
        return group

    def _build_mental_group(self) -> QGroupBox:
        group = QGroupBox("Mental / Tactical")
        layout = QFormLayout()
        layout.addRow("Positioning", self.positioning_spin)
        layout.addRow("Vision", self.vision_spin)
        layout.addRow("Decision Making", self.decision_making_spin)
        layout.addRow("Anticipation", self.anticipation_spin)
        layout.addRow("Composure", self.composure_spin)
        layout.addRow("Concentration", self.concentration_spin)
        layout.addRow("Work Rate", self.work_rate_spin)
        layout.addRow("Discipline", self.discipline_spin)
        layout.addRow("Aggression", self.aggression_spin)
        group.setLayout(layout)
        return group

    def _build_physical_group(self) -> QGroupBox:
        group = QGroupBox("Physical")
        layout = QFormLayout()
        layout.addRow("Pace", self.pace_spin)
        layout.addRow("Acceleration", self.acceleration_spin)
        layout.addRow("Agility", self.agility_spin)
        layout.addRow("Strength", self.strength_spin)
        layout.addRow("Stamina", self.stamina_spin)
        layout.addRow("Jumping", self.jumping_spin)
        group.setLayout(layout)
        return group

    def _build_state_group(self) -> QGroupBox:
        group = QGroupBox("Contract / State")
        layout = QFormLayout()
        layout.addRow("Contract Weeks", self.contract_weeks_spin)
        layout.addRow("Fatigue", self.fatigue_spin)
        layout.addRow("Fitness", self.fitness_spin)
        layout.addRow("Morale", self.morale_spin)
        layout.addRow("Familiarity", self.familiarity_spin)
        layout.addRow("Confidence", self.confidence_spin)
        layout.addRow("Sharpness", self.sharpness_spin)
        layout.addRow("Injury Proneness", self.injury_proneness_spin)
        layout.addRow("Injured", self.injured_check)
        group.setLayout(layout)
        return group

    def load_player(self, player) -> None:
        self.name_edit.setText(player.name)
        self.position_combo.setCurrentText(player.position)
        self.age_spin.setValue(getattr(player, "age", 24))
        self.potential_spin.setValue(getattr(player, "potential", 50.0))

        self.passing_spin.setValue(getattr(player, "passing", 50.0))
        self.first_touch_spin.setValue(getattr(player, "first_touch", 50.0))
        self.technique_spin.setValue(getattr(player, "technique", 50.0))
        self.dribbling_spin.setValue(getattr(player, "dribbling", 50.0))
        self.finishing_spin.setValue(getattr(player, "finishing", 50.0))
        self.long_shots_spin.setValue(getattr(player, "long_shots", 50.0))
        self.tackling_spin.setValue(getattr(player, "tackling", 50.0))
        self.heading_spin.setValue(getattr(player, "heading", 50.0))
        self.crossing_spin.setValue(getattr(player, "crossing", 50.0))

        self.positioning_spin.setValue(getattr(player, "positioning", 50.0))
        self.vision_spin.setValue(getattr(player, "vision", 50.0))
        self.decision_making_spin.setValue(getattr(player, "decision_making", 50.0))
        self.anticipation_spin.setValue(getattr(player, "anticipation", 50.0))
        self.composure_spin.setValue(getattr(player, "composure", 50.0))
        self.concentration_spin.setValue(getattr(player, "concentration", 50.0))
        self.work_rate_spin.setValue(getattr(player, "work_rate", 50.0))
        self.discipline_spin.setValue(getattr(player, "discipline", 50.0))
        self.aggression_spin.setValue(getattr(player, "aggression", 50.0))

        self.pace_spin.setValue(getattr(player, "pace", 50.0))
        self.acceleration_spin.setValue(getattr(player, "acceleration", 50.0))
        self.agility_spin.setValue(getattr(player, "agility", 50.0))
        self.strength_spin.setValue(getattr(player, "strength", 50.0))
        self.stamina_spin.setValue(getattr(player, "stamina", 50.0))
        self.jumping_spin.setValue(getattr(player, "jumping", 50.0))

        self.contract_weeks_spin.setValue(getattr(player, "contract_weeks", 104))
        self.fatigue_spin.setValue(getattr(player, "fatigue", 10.0))
        self.fitness_spin.setValue(getattr(player, "fitness", 95.0))
        self.morale_spin.setValue(getattr(player, "morale", 50.0))
        self.familiarity_spin.setValue(getattr(player, "familiarity", 50.0))
        self.confidence_spin.setValue(getattr(player, "confidence", 50.0))
        self.sharpness_spin.setValue(getattr(player, "sharpness", 50.0))
        self.injury_proneness_spin.setValue(getattr(player, "injury_proneness", 20.0))
        self.injured_check.setChecked(getattr(player, "injured", False))

        self._update_derived_labels(player)

    def apply_to_player(self, player) -> None:
        player.name = self.name_edit.text().strip()
        player.position = self.position_combo.currentText()
        player.age = self.age_spin.value()
        player.potential = self.potential_spin.value()

        player.passing = self.passing_spin.value()
        player.first_touch = self.first_touch_spin.value()
        player.technique = self.technique_spin.value()
        player.dribbling = self.dribbling_spin.value()
        player.finishing = self.finishing_spin.value()
        player.long_shots = self.long_shots_spin.value()
        player.tackling = self.tackling_spin.value()
        player.heading = self.heading_spin.value()
        player.crossing = self.crossing_spin.value()

        player.positioning = self.positioning_spin.value()
        player.vision = self.vision_spin.value()
        player.decision_making = self.decision_making_spin.value()
        player.anticipation = self.anticipation_spin.value()
        player.composure = self.composure_spin.value()
        player.concentration = self.concentration_spin.value()
        player.work_rate = self.work_rate_spin.value()
        player.discipline = self.discipline_spin.value()
        player.aggression = self.aggression_spin.value()

        player.pace = self.pace_spin.value()
        player.acceleration = self.acceleration_spin.value()
        player.agility = self.agility_spin.value()
        player.strength = self.strength_spin.value()
        player.stamina = self.stamina_spin.value()
        player.jumping = self.jumping_spin.value()

        player.contract_weeks = self.contract_weeks_spin.value()
        player.fatigue = self.fatigue_spin.value()
        player.fitness = self.fitness_spin.value()
        player.morale = self.morale_spin.value()
        player.familiarity = self.familiarity_spin.value()
        player.confidence = self.confidence_spin.value()
        player.sharpness = self.sharpness_spin.value()
        player.injury_proneness = self.injury_proneness_spin.value()
        player.injured = self.injured_check.isChecked()

        self._update_derived_labels(player)

    def _update_derived_labels(self, player) -> None:
        ability = current_ability(player)
        value = estimate_market_value(player)

        self.ca_label.setText(f"{ability:.1f}")
        self.value_label.setText(self._format_value(value))

    @staticmethod
    def _format_value(value: int) -> str:
        if value >= 1_000_000:
            return f"€{value / 1_000_000:.2f}M"
        if value >= 1_000:
            return f"€{value / 1_000:.0f}K"
        return f"€{value}"