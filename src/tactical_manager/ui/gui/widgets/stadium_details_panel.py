from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from tactical_manager.core.models import Club, StadiumSection
from tactical_manager.core.stadium_logic import (
    add_roof,
    expansion_cost,
    get_section,
    improve_section_quality,
    quality_upgrade_cost,
    roof_cost,
    expand_section,
)


class StadiumDetailsPanel(QWidget):
    section_updated = Signal()

    def __init__(self, club: Club):
        super().__init__()
        self.club = club
        self._selected_section_name: str | None = None

        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        self.title_label = QLabel("Section Details")
        self.title_label.setObjectName("section_title")
        layout.addWidget(self.title_label)

        self.name_label = QLabel("No section selected")
        layout.addWidget(self.name_label)

        self.capacity_label = QLabel("")
        layout.addWidget(self.capacity_label)

        self.covered_label = QLabel("")
        layout.addWidget(self.covered_label)

        self.quality_label = QLabel("")
        layout.addWidget(self.quality_label)

        self.type_label = QLabel("")
        layout.addWidget(self.type_label)

        self.expansion_level_label = QLabel("")
        layout.addWidget(self.expansion_level_label)

        self.cash_label = QLabel("")
        layout.addWidget(self.cash_label)

        self.expand_button = QPushButton("Expand Section")
        self.expand_button.clicked.connect(self._on_expand_clicked)
        layout.addWidget(self.expand_button)

        self.add_roof_button = QPushButton("Add Roof")
        self.add_roof_button.clicked.connect(self._on_add_roof_clicked)
        layout.addWidget(self.add_roof_button)

        self.improve_quality_button = QPushButton("Improve Quality")
        self.improve_quality_button.clicked.connect(self._on_improve_quality_clicked)
        layout.addWidget(self.improve_quality_button)

        self.cost_hint_label = QLabel("")
        self.cost_hint_label.setWordWrap(True)
        layout.addWidget(self.cost_hint_label)

        self.message_label = QLabel("")
        self.message_label.setWordWrap(True)
        layout.addWidget(self.message_label)

        layout.addStretch()

    def set_section(self, section_name: str) -> None:
        self._selected_section_name = section_name
        self.message_label.setText("")
        self.refresh()

    def refresh(self) -> None:
        section = self._get_selected_section()

        self.cash_label.setText(
            f"Available cash: {self.club.finance.cash:,.0f}"
        )

        if section is None:
            self.name_label.setText("No section selected")
            self.capacity_label.setText("")
            self.covered_label.setText("")
            self.quality_label.setText("")
            self.type_label.setText("")
            self.expansion_level_label.setText("")
            self.cost_hint_label.setText("Select a stadium section to inspect and upgrade it.")

            self.expand_button.setEnabled(False)
            self.add_roof_button.setEnabled(False)
            self.improve_quality_button.setEnabled(False)
            return

        self.name_label.setText(f"Name: {section.name}")
        self.capacity_label.setText(f"Capacity: {section.capacity:,}")
        self.covered_label.setText(f"Covered: {'Yes' if section.covered else 'No'}")
        self.quality_label.setText(f"Quality: {section.quality}")
        self.type_label.setText(f"Type: {section.section_type}")
        self.expansion_level_label.setText(
            f"Expansion level: {section.expansion_level}"
        )

        expand_cost = expansion_cost(section)
        roof_upgrade_cost = roof_cost(section)
        quality_cost = quality_upgrade_cost(section)

        self.cost_hint_label.setText(
            (
                f"Next upgrade costs:\n"
                f"- Expand: {expand_cost:,.0f}\n"
                f"- Roof: {roof_upgrade_cost:,.0f}\n"
                f"- Quality: {quality_cost:,.0f}"
            )
        )

        self.expand_button.setEnabled(True)
        self.add_roof_button.setEnabled(not section.covered)
        self.improve_quality_button.setEnabled(section.quality < 5)

    def _get_selected_section(self) -> StadiumSection | None:
        if self._selected_section_name is None:
            return None
        return get_section(self.club.stadium, self._selected_section_name)

    def _on_expand_clicked(self) -> None:
        section = self._get_selected_section()
        if section is None:
            return

        success = expand_section(self.club, section.name)
        if success:
            self.message_label.setText("Section expanded successfully.")
            self.refresh()
            self.section_updated.emit()
        else:
            self.message_label.setText("Could not expand section.")

    def _on_add_roof_clicked(self) -> None:
        section = self._get_selected_section()
        if section is None:
            return

        success = add_roof(self.club, section.name)
        if success:
            self.message_label.setText("Roof added successfully.")
            self.refresh()
            self.section_updated.emit()
        else:
            self.message_label.setText("Could not add roof.")

    def _on_improve_quality_clicked(self) -> None:
        section = self._get_selected_section()
        if section is None:
            return

        success = improve_section_quality(self.club, section.name)
        if success:
            self.message_label.setText("Section quality improved successfully.")
            self.refresh()
            self.section_updated.emit()
        else:
            self.message_label.setText("Could not improve section quality.")