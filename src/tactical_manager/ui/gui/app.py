from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QSplashScreen

from tactical_manager.core.season import Season
from tactical_manager.ui.gui.main_window import GameWindow


def run_gui(season: Season) -> None:
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

    window = GameWindow(season)

    def start_main_window() -> None:
        window.show()
        splash.finish(window)

    QTimer.singleShot(1500, start_main_window)

    app.exec()