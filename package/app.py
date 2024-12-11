from PyQt6.QtWidgets import QApplication
from package.models.app_info import AppInfo
from package.ui.main_window import MainWindow
import os
import pyqtgraph as pg
from package.config import Colours


class App(QApplication):
    def __init__(self, sys_argv, dev_type: str) -> None:
        super().__init__(sys_argv)
        self.load_stylesheet()

        self.main_window = MainWindow(
            AppInfo(1, "LeoNUS", "Cansat Telemetry & Ground Control")
        )
        self.main_window.setDevTypeGeometry(dev_type)

    def load_stylesheet(self) -> None:
        stylesheet = os.path.join(
            os.path.dirname(__file__), "./styles/styles.css"
        )
        with open(stylesheet, "r") as file:
            self.setStyleSheet(file.read())

        pg.setConfigOption("background", Colours.SILVER.value)
        pg.setConfigOption("foreground", Colours.RICH_BLACK.value)

    def run(self) -> int:
        self.main_window.show()
        return self.exec()
