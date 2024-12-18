import random
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from package.models.app_info import AppInfo
from package.models.telemetry import (
    GPS,
    Mode,
    PrincipalAxesCoordinate,
    State,
    Telemetry,
)
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

        self.packet = 0  # TODO: Remove

    def load_stylesheet(self) -> None:
        stylesheet = os.path.join(
            os.path.dirname(__file__), "./styles/styles.css"
        )
        with open(stylesheet, "r") as file:
            self.setStyleSheet(file.read())

        pg.setConfigOption("background", Colours.SILVER.value)
        pg.setConfigOption("foreground", Colours.RICH_BLACK.value)

    def update(self) -> None:
        self.packet += 1  # TODO: Remove
        telemetry = Telemetry(
            mission_time=time.strftime("%H:%M:%S", time.localtime()),
            packet_count=self.packet,
            mode=Mode.FLIGHT,
            state=State.ASCENT,
            altitude=(altitude := round(random.uniform(0, 1000), 1)),
            temperature=round(random.uniform(0, 100), 1),
            pressure=round(random.uniform(0, 1000), 1),
            voltage=round(random.uniform(0, 100), 1),
            gyro=PrincipalAxesCoordinate(
                roll=round(random.uniform(0, 360), 1),
                pitch=round(random.uniform(0, 360), 1),
                yaw=round(random.uniform(0, 360), 1),
            ),
            acceleration=PrincipalAxesCoordinate(
                roll=round(random.uniform(0, 360), 1),
                pitch=round(random.uniform(0, 360), 1),
                yaw=round(random.uniform(0, 360), 1),
            ),
            magnetometer=PrincipalAxesCoordinate(
                roll=round(random.uniform(0, 360), 1),
                pitch=round(random.uniform(0, 360), 1),
                yaw=round(random.uniform(0, 360), 1),
            ),
            auto_gyro_rotation_rate=round(random.uniform(0, 100), 1),
            gps=GPS(
                time=time.strftime("%H:%M:%S", time.localtime()),
                altitude=altitude,
                latitude=round(random.uniform(0, 360), 1),
                longitude=round(random.uniform(0, 360), 1),
                sats=random.randint(0, 100),
            ),
            cmd_echo=None,
        )
        self.main_window.update(telemetry)

    def run(self) -> int:
        self.main_window.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

        return self.exec()
