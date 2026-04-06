from __future__ import annotations

from PySide6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from tactical_manager.core.models import Club


def money_text(value: float) -> str:
    return f"€{value:,.0f}"


class FinanceSummaryWidget(QWidget):
    def __init__(self, club: Club):
        super().__init__()
        self.club = club

        self.cash_label = QLabel()
        self.monthly_result_label = QLabel()
        self.season_result_label = QLabel()
        self.wage_bill_label = QLabel()
        self.transfer_budget_label = QLabel()

        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        grid = QGridLayout()

        grid.addWidget(self._make_card("Cash", self.cash_label), 0, 0)
        grid.addWidget(self._make_card("Monthly Result", self.monthly_result_label), 0, 1)
        grid.addWidget(self._make_card("Season Result", self.season_result_label), 0, 2)
        grid.addWidget(self._make_card("Wage Bill", self.wage_bill_label), 1, 0)
        grid.addWidget(self._make_card("Transfer Budget", self.transfer_budget_label), 1, 1)

        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 1)

        layout = QVBoxLayout(self)
        layout.addLayout(grid)
        layout.addStretch()

    def _make_card(self, title: str, value_label: QLabel) -> QGroupBox:
        box = QGroupBox(title)
        layout = QVBoxLayout(box)
        value_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(value_label)
        return box

    def refresh(self) -> None:
        finance = self.club.finance

        self.cash_label.setText(money_text(getattr(finance, "cash", 0.0)))
        self.monthly_result_label.setText(money_text(getattr(finance, "monthly_result", 0.0)))
        self.season_result_label.setText(money_text(getattr(finance, "season_result", 0.0)))
        self.wage_bill_label.setText(money_text(getattr(finance, "wage_bill", 0.0)))
        self.transfer_budget_label.setText(money_text(getattr(finance, "transfer_budget", 0.0)))