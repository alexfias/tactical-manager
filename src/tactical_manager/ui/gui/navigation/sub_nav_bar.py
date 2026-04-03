from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget


class SubNavBar(QWidget):
    tab_selected = Signal(str)

    def __init__(
        self,
        items: list[tuple[str, str]],
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.buttons: dict[str, QPushButton] = {}

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        for item_id, label in items:
            button = QPushButton(label)
            button.setCheckable(True)
            button.setMinimumHeight(40)
            button.setProperty("subnav", True)
            button.clicked.connect(
                lambda checked=False, iid=item_id: self.tab_selected.emit(iid)
            )
            self.buttons[item_id] = button
            layout.addWidget(button)

        layout.addStretch()

    def set_active(self, item_id: str) -> None:
        for iid, button in self.buttons.items():
            button.setChecked(iid == item_id)