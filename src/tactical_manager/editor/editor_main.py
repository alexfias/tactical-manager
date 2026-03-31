from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from tactical_manager.editor.main_window import ClubEditorWindow


def main() -> None:
    app = QApplication(sys.argv)

    data_dir = Path("data/clubs")
    window = ClubEditorWindow(clubs_dir=data_dir)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()