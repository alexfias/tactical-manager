from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from tactical_manager.ui.gui.pages.board_page import BoardPage
from tactical_manager.ui.gui.pages.finance_page import FinancePage
from tactical_manager.ui.gui.pages.stadium_page import StadiumPage
from tactical_manager.ui.gui.widgets.club_overview_widget import ClubOverviewWidget


class PlaceholderClubSection(QWidget):
    def __init__(self, title: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)

        label = QLabel(f"{title} coming soon")
        label.setProperty("sectionTitle", True)

        info = QLabel("This section has not been implemented yet.")
        info.setWordWrap(True)

        layout.addWidget(label)
        layout.addWidget(info)
        layout.addStretch()


class ClubPage(QWidget):
    def __init__(self, club, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.club = club

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(14)

        title = QLabel("Club")
        title.setProperty("sectionTitle", True)

        self.overview_widget = ClubOverviewWidget(self.club)
        self.finance_page = FinancePage(self.club)
        self.infrastructure_page = StadiumPage(self.club)
        self.support_page = PlaceholderClubSection("Support")
        self.board_page = BoardPage(self.club)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.overview_widget)
        self.stack.addWidget(self.finance_page)
        self.stack.addWidget(self.infrastructure_page)
        self.stack.addWidget(self.support_page)
        self.stack.addWidget(self.board_page)

        self.overview_button = QPushButton("Overview")
        self.finance_button = QPushButton("Finances")
        self.infrastructure_button = QPushButton("Infrastructure")
        self.support_button = QPushButton("Support")
        self.board_button = QPushButton("Board")

        self.overview_button.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.overview_widget)
        )
        self.finance_button.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.finance_page)
        )
        self.infrastructure_button.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.infrastructure_page)
        )
        self.support_button.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.support_page)
        )
        self.board_button.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.board_page)
        )

        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.overview_button)
        nav_layout.addWidget(self.finance_button)
        nav_layout.addWidget(self.infrastructure_button)
        nav_layout.addWidget(self.support_button)
        nav_layout.addWidget(self.board_button)
        nav_layout.addStretch()

        main_layout.addWidget(title)
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.stack, 1)

    def refresh(self) -> None:
        if hasattr(self.overview_widget, "refresh"):
            self.overview_widget.refresh()

        if hasattr(self.finance_page, "refresh"):
            self.finance_page.refresh()

        if hasattr(self.infrastructure_page, "refresh"):
            self.infrastructure_page.refresh()

        if hasattr(self.support_page, "refresh"):
            self.support_page.refresh()

        if hasattr(self.board_page, "refresh"):
            self.board_page.refresh()