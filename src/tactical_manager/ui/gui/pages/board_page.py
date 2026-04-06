from __future__ import annotations

from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class BoardPage(QWidget):
    def __init__(self, club, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.club = club

        self.confidence_label = QLabel()
        self.chairman_label = QLabel()

        self.objectives_table = QTableWidget()
        self.objectives_table.setColumnCount(2)
        self.objectives_table.setHorizontalHeaderLabels(["Objective", "Status"])

        self.notes_label = QLabel()
        self.notes_label.setWordWrap(True)

        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        summary_box = QGroupBox("Board Summary")
        summary_form = QFormLayout(summary_box)
        summary_form.addRow("Board Confidence:", self.confidence_label)
        summary_form.addRow("Chairman:", self.chairman_label)

        objectives_box = QGroupBox("Objectives")
        objectives_layout = QVBoxLayout(objectives_box)
        objectives_layout.addWidget(self.objectives_table)

        notes_box = QGroupBox("Board Notes")
        notes_layout = QVBoxLayout(notes_box)
        notes_layout.addWidget(self.notes_label)

        layout.addWidget(summary_box)
        layout.addWidget(objectives_box)
        layout.addWidget(notes_box)
        layout.addStretch()

    def refresh(self) -> None:
        board = getattr(self.club, "board", None)

        confidence = getattr(board, "confidence", "Stable") if board else "Stable"
        chairman = getattr(board, "chairman_name", "Club Board") if board else "Club Board"
        objectives = getattr(board, "objectives", None) if board else None
        notes = getattr(
            board,
            "notes",
            "The board expects the club to perform solidly this season.",
        ) if board else "The board expects the club to perform solidly this season."

        if not objectives:
            objectives = [
                ("Finish in the top half", "In progress"),
                ("Reach the domestic cup second round", "In progress"),
                ("Stay within wage budget", "In progress"),
            ]

        self.confidence_label.setText(str(confidence))
        self.chairman_label.setText(str(chairman))
        self.notes_label.setText(str(notes))

        self.objectives_table.setRowCount(len(objectives))
        for row, (objective, status) in enumerate(objectives):
            self.objectives_table.setItem(row, 0, QTableWidgetItem(str(objective)))
            self.objectives_table.setItem(row, 1, QTableWidgetItem(str(status)))

        self.objectives_table.resizeColumnsToContents()