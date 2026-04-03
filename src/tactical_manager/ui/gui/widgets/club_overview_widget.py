from __future__ import annotations

from PySide6.QtWidgets import QTextEdit, QVBoxLayout, QWidget


class ClubOverviewWidget(QWidget):
    def __init__(self, club, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.club = club

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        layout.addWidget(self.output)
        self.refresh()

    def refresh(self) -> None:
        club = self.club

        lines = [
            "=== CLUB OVERVIEW ===",
            "",
            f"Club: {club.identity.name}",
            f"Country: {club.country}",
            f"Reputation: {club.identity.reputation}",
            "",
            "=== FINANCE ===",
            f"Balance: {club.finance.balance}",
            f"Transfer budget: {club.finance.transfer_budget}",
            f"Weekly wages: {club.finance.weekly_wages}",
            f"Wage budget: {club.finance.wage_budget}",
            "",
            "=== INFRASTRUCTURE ===",
            f"Stadium capacity: {club.infrastructure.stadium_capacity}",
            f"Ticket price: {club.infrastructure.ticket_price}",
            f"Training level: {club.infrastructure.training_level}",
            f"Youth level: {club.infrastructure.youth_level}",
            "",
            "=== SUPPORT ===",
            f"Fan confidence: {club.support.fan_confidence}",
            f"Fan base: {club.support.fan_base}",
            "",
            "=== BOARD ===",
            f"Target finish: {club.board.target_finish}",
            f"Max wage ratio: {club.board.max_wage_ratio}",
            f"Philosophy: {club.board.philosophy}",
        ]

        self.output.setPlainText("\n".join(str(x) for x in lines))