from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QComboBox,
    QFormLayout,
    QVBoxLayout,
)


class MatchSetupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Match Setup")
        self.setModal(True)

        layout = QVBoxLayout()
        form = QFormLayout()

        self.plan_combo = QComboBox()
        self.plan_combo.addItems(["defensive", "balanced", "attacking"])

        self.mentality_combo = QComboBox()
        self.mentality_combo.addItems(["defensive", "balanced", "attacking"])

        form.addRow("Match approach:", self.plan_combo)
        form.addRow("Mentality:", self.mentality_combo)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)
        self.setLayout(layout)

        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: white;
            }

            QLabel {
                color: white;
            }

            QComboBox {
                background-color: rgba(25, 25, 25, 230);
                color: white;
                border: 1px solid rgba(255, 255, 255, 40);
                border-radius: 6px;
                padding: 6px;
                min-height: 28px;
            }

            QPushButton {
                background-color: rgba(30, 30, 30, 220);
                color: white;
                border: 1px solid rgba(255, 255, 255, 35);
                border-radius: 8px;
                padding: 8px 12px;
                min-width: 90px;
            }

            QPushButton:hover {
                background-color: rgba(50, 50, 50, 230);
            }
        """)

    def get_values(self) -> tuple[str, str]:
        return self.plan_combo.currentText(), self.mentality_combo.currentText()