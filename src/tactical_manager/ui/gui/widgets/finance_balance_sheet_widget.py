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


class FinanceBalanceSheetWidget(QWidget):
    def __init__(self, club: Club):
        super().__init__()
        self.club = club

        self.assets_table = QTableWidget()
        self.liabilities_table = QTableWidget()
        self.equity_label = QLabel()

        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        assets_box = QGroupBox("Assets")
        assets_layout = QVBoxLayout(assets_box)
        assets_layout.addWidget(self.assets_table)

        liabilities_box = QGroupBox("Liabilities")
        liabilities_layout = QVBoxLayout(liabilities_box)
        liabilities_layout.addWidget(self.liabilities_table)

        tables_layout = QHBoxLayout()
        tables_layout.addWidget(assets_box)
        tables_layout.addWidget(liabilities_box)

        equity_box = QGroupBox("Equity")
        equity_layout = QVBoxLayout(equity_box)
        self.equity_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        equity_layout.addWidget(self.equity_label)

        layout = QVBoxLayout(self)
        layout.addLayout(tables_layout)
        layout.addWidget(equity_box)
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

        assets = getattr(finance, "assets", {
            "Cash": getattr(finance, "cash", 0.0),
            "Squad Value": 0.0,
            "Stadium Value": 0.0,
        })

        liabilities = getattr(finance, "liabilities", {
            "Loans": 0.0,
            "Unpaid Transfers": 0.0,
        })

        self._fill_table(self.assets_table, assets)
        self._fill_table(self.liabilities_table, liabilities)

        equity = sum(assets.values()) - sum(liabilities.values())
        self.equity_label.setText(money_text(equity))