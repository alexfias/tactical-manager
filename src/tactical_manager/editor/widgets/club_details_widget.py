from __future__ import annotations

from PySide6.QtWidgets import (
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QLineEdit,
    QWidget,
)

from tactical_manager.core.models import Club


class ClubDetailsWidget(QGroupBox):
    def __init__(self) -> None:
        super().__init__("Club Details")

        self.name_edit = QLineEdit()
        self.reputation_spin = QDoubleSpinBox()
        self.reputation_spin.setRange(0, 100)
        self.reputation_spin.setDecimals(1)

        layout = QFormLayout()
        layout.addRow("Name", self.name_edit)
        layout.addRow("Reputation", self.reputation_spin)
        self.setLayout(layout)

    def load_club(self, club: Club) -> None:
        self.name_edit.setText(club.identity.name)
        self.reputation_spin.setValue(club.identity.reputation)

    def apply_to_club(self, club: Club) -> None:
        club.identity.name = self.name_edit.text().strip()
        club.identity.reputation = self.reputation_spin.value()