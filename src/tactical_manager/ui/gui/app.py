from __future__ import annotations

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QDialog, QMessageBox, QSplashScreen

from tactical_manager.core.season import Season
from tactical_manager.ui.gui.club_selection_dialog import ClubSelectionDialog
from tactical_manager.ui.gui.main_window import GameWindow


def run_gui(clubs: dict, fixtures: list, competition=None) -> None:
    app = QApplication([])

    pixmap = QPixmap("assets/splash.png")
    splash = QSplashScreen(pixmap)
    splash.setWindowFlag(Qt.FramelessWindowHint)
    splash.showMessage(
        "Tactical Manager\nLoading...",
        Qt.AlignCenter | Qt.AlignBottom,
        Qt.white,
    )
    splash.show()

    app.processEvents()

    def continue_startup() -> None:
        dialog = ClubSelectionDialog(list(clubs.keys()))
        splash.finish(dialog)

        if dialog.exec() != QDialog.Accepted:
            app.quit()
            return

        user_club = dialog.selected_club()
        if user_club is None:
            QMessageBox.warning(
                None,
                "No Club Selected",
                "Please select a club.",
            )
            app.quit()
            return

        season = Season(
            clubs=clubs,
            fixtures=fixtures,
            user_club=user_club,
        )

        window = GameWindow(season)
        window.show()

        app.main_window = window  # keep reference alive

    QTimer.singleShot(1500, continue_startup)

    app.exec()