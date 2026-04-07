from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from tactical_manager.core.models import Club
from tactical_manager.core.stadium_logic import (
    average_quality,
    covered_capacity,
    total_capacity,
)
from tactical_manager.ui.gui.widgets.stadium_details_panel import StadiumDetailsPanel
from tactical_manager.ui.gui.widgets.stadium_widget import StadiumWidget


class StadiumPage(QWidget):
    def __init__(self, club: Club):
        super().__init__()
        self.club = club

        self._build_ui()
        self._connect_signals()
        self.refresh()

    def _build_ui(self) -> None:
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(16, 16, 16, 16)
        root_layout.setSpacing(12)

        title = QLabel("Stadium")
        title.setObjectName("page_title")
        root_layout.addWidget(title)

        self.summary_label = QLabel()
        self.summary_label.setObjectName("stadium_summary")
        self.summary_label.setWordWrap(True)
        root_layout.addWidget(self.summary_label)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(16)
        root_layout.addLayout(content_layout)

        self.stadium_widget = StadiumWidget(self.club.stadium)
        content_layout.addWidget(self.stadium_widget, 2)

        self.details_panel = StadiumDetailsPanel(self.club)
        content_layout.addWidget(self.details_panel, 1)

    def _connect_signals(self) -> None:
        self.stadium_widget.section_selected.connect(self.on_section_selected)
        self.details_panel.section_updated.connect(self.on_section_updated)

    def on_section_selected(self, section_name: str) -> None:
        self.details_panel.set_section(section_name)

    def on_section_updated(self) -> None:
        self.stadium_widget.refresh()
        self.refresh()

    def refresh(self) -> None:
        stadium = self.club.stadium

        total = total_capacity(stadium)
        covered = covered_capacity(stadium)
        avg_quality = average_quality(stadium)

        self.summary_label.setText(
            (
                f"Name: {stadium.name} | "
                f"Capacity: {total:,} | "
                f"Covered: {covered:,} | "
                f"Avg. Quality: {avg_quality:.1f} | "
                f"Floodlights: {'Yes' if stadium.floodlights else 'No'} | "
                f"Scoreboard: {'Yes' if stadium.scoreboard else 'No'}"
            )
        )