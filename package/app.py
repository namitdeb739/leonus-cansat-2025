import atexit
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from package.communication import Communication
from package.models.app_info import AppInfo
from package.models.telemetry import OnOff
from package.ui.main_window import MainWindow
import os
import pyqtgraph as pg
from package.config import Colours
import package.plotter as plotter


class App(QApplication):

    def __init__(self, sys_argv, dev_type: str) -> None:
        super().__init__(sys_argv)
        self.load_stylesheet()

        self.app_info = AppInfo(
            3171, "LeoNUS", "Cansat Telemetry & Ground Control"
        )
        self.communication = Communication(self.app_info.team_info.team_id)
        self.main_window = MainWindow(
            self.app_info,
            self.communication,
        )
        self.main_window.setDevTypeGeometry(dev_type)

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
        if not self.communication.is_connected():
            print(f"{time.strftime('%H:%M:%S')} No connection")
            self.connection.connect()
            # self.main_window.update_connection_status(False)
            return

        data = self.communication.recieve()
        if data is None:
            print(f"{time.strftime('%H:%M:%S')} No data received")
            return
        telemetry = self.communication.parse_data(data)

        if telemetry is None:
            return

        self.main_window.update(telemetry)

        if (
            self.communication.simulated_pressure_file_data is not None
            or len(self.communication.simulated_pressure_file_data) > 0
        ):
            self.communication.send_simulated_pressure()

    def run(self) -> int:
        self.main_window.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(250)

        self.communication.payload_telemetry(OnOff.ON)

        return self.exec()

    def on_exit(self) -> None:
        print("Handling exit")
        self.communication.device.close()
        plotter.generate_plots(
            self.communication.start_time, self.communication.csv_file
        )
        self.timer.stop()
        self.quit()
