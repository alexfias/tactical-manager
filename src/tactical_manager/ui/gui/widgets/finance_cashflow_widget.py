from __future__ import annotations

from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from tactical_manager.core.models import Club


def money_text(value: float) -> str:
    return f"€{value:,.0f}"


class FinanceCashflowWidget(QWidget):
    def __init__(self, club: Club):
        super().__init__()
        self.club = club

        self.revenue_table = QTableWidget()
        self.costs_table = QTableWidget()
        self.net_result_label = QLabel()

        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        revenue_box = QGroupBox("Revenue")
        revenue_layout = QVBoxLayout(revenue_box)
        revenue_layout.addWidget(self.revenue_table)

        costs_box = QGroupBox("Costs")
        costs_layout = QVBoxLayout(costs_box)
        costs_layout.addWidget(self.costs_table)

        tables_layout = QHBoxLayout()
        tables_layout.addWidget(revenue_box)
        tables_layout.addWidget(costs_box)

        result_box = QGroupBox("Net Cashflow")
        result_layout = QVBoxLayout(result_box)
        self.net_result_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        result_layout.addWidget(self.net_result_label)

        layout = QVBoxLayout(self)
        layout.addLayout(tables_layout)
        layout.addWidget(result_box)
        layout.addStretch()

    def _fill_table(self, table: QTableWidget, data: dict[str, float]) -> None:
        table.clear()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Category", "Amount"])
        table.setRowCount(len(data))

        for row, (name, value) in enumerate(data.items()):
            table.setItem(row, 0, QTableWidgetItem(name))
            table.setItem(row, 1, QTableWidgetItem(money_text(value)))

        table.resizeColumnsToContents()

    def refresh(self) -> None:
        finance = self.club.finance

        revenue = getattr(finance, "revenue", {
            "Ticket Sales": 0.0,
            "Sponsorship": 0.0,
            "Prize Money": 0.0,
            "Merchandise": 0.0,
            "Player Sales": 0.0,
        })

        costs = getattr(finance, "costs", {
            "Player Wages": 0.0,
            "Staff Wages": 0.0,
            "Maintenance": 0.0,
            "Scouting": 0.0,
            "Transfers": 0.0,
        })

        self._fill_table(self.revenue_table, revenue)
        self._fill_table(self.costs_table, costs)

        net_result = sum(revenue.values()) - sum(costs.values())
        self.net_result_label.setText(money_text(net_result))