from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from tactical_manager.core.models import Club
from tactical_manager.ui.gui.widgets.finance_summary_widget import FinanceSummaryWidget
from tactical_manager.ui.gui.widgets.finance_cashflow_widget import FinanceCashflowWidget
from tactical_manager.ui.gui.widgets.finance_balance_sheet_widget import FinanceBalanceSheetWidget


class FinancePage(QWidget):
    def __init__(self, club: Club):
        super().__init__()
        self.club = club

        self.summary_widget = FinanceSummaryWidget(club)
        self.cashflow_widget = FinanceCashflowWidget(club)
        self.balance_sheet_widget = FinanceBalanceSheetWidget(club)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.summary_widget)
        self.stack.addWidget(self.cashflow_widget)
        self.stack.addWidget(self.balance_sheet_widget)

        self.summary_button = QPushButton("Summary")
        self.cashflow_button = QPushButton("Cashflow")
        self.balance_sheet_button = QPushButton("Balance Sheet")

        self.summary_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.summary_widget))
        self.cashflow_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.cashflow_widget))
        self.balance_sheet_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.balance_sheet_widget))

        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.summary_button)
        nav_layout.addWidget(self.cashflow_button)
        nav_layout.addWidget(self.balance_sheet_button)
        nav_layout.addStretch()

        layout = QVBoxLayout(self)
        layout.addLayout(nav_layout)
        layout.addWidget(self.stack)

    def refresh(self) -> None:
        self.summary_widget.refresh()
        self.cashflow_widget.refresh()
        self.balance_sheet_widget.refresh()