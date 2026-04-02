from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QListWidget,
    QVBoxLayout,
)


class ClubSelectionDialog(QDialog):
    def __init__(self, club_names: list[str], parent=None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Choose Your Club")
        self.resize(400, 300)

        layout = QVBoxLayout(self)

        title = QLabel("Choose your club:")
        layout.addWidget(title)

        self.club_list = QListWidget()
        self.club_list.addItems(club_names)
        self.club_list.itemDoubleClicked.connect(self.accept)
        layout.addWidget(self.club_list)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        if club_names:
            self.club_list.setCurrentRow(0)

    def selected_club(self) -> str | None:
        item = self.club_list.currentItem()
        if item is None:
            return None
        return item.text()