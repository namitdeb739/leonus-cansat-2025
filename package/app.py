import atexit
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from package.communication import Communication
from package.models.app_info import AppInfo
from package.ui.main_window import MainWindow
import os
import pyqtgraph as pg
from package.config import Colours
import package.plotter as plotter


class App(QApplication):
    def __init__(self, sys_argv, dev_type: str) -> None:
        super().__init__(sys_argv)
        self.load_stylesheet()

        self.main_window = MainWindow(
            AppInfo(1, "LeoNUS", "Cansat Telemetry & Ground Control")
        )
        self.main_window.setDevTypeGeometry(dev_type)

        self.communication = Communication()
        atexit.register(self.on_exit)

    def load_stylesheet(self) -> None:
        stylesheet = os.path.join(
            os.path.dirname(__file__), "./styles/styles.css"
        )
        with open(stylesheet, "r") as file:
            self.setStyleSheet(file.read())

        pg.setConfigOption("background", Colours.SILVER.value)
        pg.setConfigOption("foreground", Colours.RICH_BLACK.value)

    def update(self) -> None:
        data = self.communication.recieve()
        telemetry = self.communication.parse_data(data)
        self.main_window.update(telemetry)

    def run(self) -> int:
        self.main_window.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

        return self.exec()

    def on_exit(self) -> None:
        plotter.generate_plots(
            self.communication.start_time, self.communication.csv_file
        )
