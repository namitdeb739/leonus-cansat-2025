import atexit
from datetime import datetime
import random
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from package import constants
from package.communications.communication import Communication
from package.constants import APP_INFO, GEOMETRY
from package.models.telemetry import (
    GPS,
    Command,
    Mode,
    OnOff,
    PrincipalAxesCoordinate,
    State,
    Telemetry,
)
from package.ui.main_window import MainWindow
import os
import pyqtgraph as pg
from package.config import DevMode
from package.constants import Colours


class App(QApplication):

    STYLESHEET_PATH = "./styles/styles.css"

    def __init__(self, sys_argv: list[str], dev_mode: DevMode) -> None:
        super().__init__(sys_argv)

        self.__set_stylesheet()

        self.communication = Communication()
        self.main_window = MainWindow(
            APP_INFO,
            self.communication,
            GEOMETRY[dev_mode.value],
        )
        self.logger = self.main_window.logger()

        self.logger.log("======================LEONUS======================")

        self.communication.set_logger(self.logger)
        self.logger.log("Enabling telemetry storage...")
        
        atexit.register(self.on_exit)

        # TEST ZONE
        self.packet_count = 0
        self.last = ""

    def run(self) -> int:
        self.main_window.show()
        self.__setup_timer(250)

        return self.exec()

    def __setup_timer(self, interval: int) -> None:
        self.timer = QTimer()
        self.timer.timeout.connect(self.__update)
        self.timer.start(interval)

    def __update(self) -> None:
        self.main_window.update_time()

        # TEST ZONE START
        if self.last == datetime.now().strftime("%H:%M:%S"):
            return
        self.last = datetime.now().strftime("%H:%M:%S")
        self.packet_count += 1
        t = Telemetry(
            team_id=APP_INFO.team_id(),
            mission_time=datetime.now().strftime("%H:%M:%S"),
            packet_count=self.packet_count,
            mode=random.choice(list(Mode)),
            state=random.choice(list(State)),
            altitude=round(random.uniform(0, 10000), 1),
            temperature=round(random.uniform(-50, 50), 1),
            pressure=round(random.uniform(900, 1100), 1),
            voltage=round(random.uniform(3.0, 4.2), 1),
            gyro=PrincipalAxesCoordinate(
                roll=round(random.uniform(-180, 180), 1),
                pitch=round(random.uniform(-180, 180), 1),
                yaw=round(random.uniform(-180, 180), 1),
            ),
            acceleration=PrincipalAxesCoordinate(
                roll=round(random.uniform(-10, 10), 1),
                pitch=round(random.uniform(-10, 10), 1),
                yaw=round(random.uniform(-10, 10), 1),
            ),
            magnetometer=PrincipalAxesCoordinate(
                roll=round(random.uniform(-100, 100), 1),
                pitch=round(random.uniform(-100, 100), 1),
                yaw=round(random.uniform(-100, 100), 1),
            ),
            auto_gyro_rotation_rate=random.randint(0, 360),
            gps=GPS(
                time=datetime.now().strftime("%H:%M:%S"),
                altitude=round(random.uniform(0, 10000), 1),
                latitude=round(random.uniform(-90, 90), 1),
                longitude=round(random.uniform(-180, 180), 1),
                sats=random.randint(0, 12),
            ),
            cmd_echo=Command.command(
                Command.CommandType.PAYLOAD_TELEMETRY, OnOff.ON
            ),
            descent_rate=round(random.uniform(0, 50), 1),
            geographic_heading=random.randint(0, 360),
        )

        self.main_window.update(t)
        self.communication.save(t)

        # TEST ZONE END

        if not self.__check_connection():
            return

        self.__receive_telemetry()

        if (
            self.__is_simulation_mode()
            and self.__has_simulated_pressure_commands()
        ):
            self.__send_next_simulated_pressure()

    def __receive_telemetry(self) -> None:
        telemetry = self.__recieve_data()
        if telemetry is None:
            return

        self.main_window.update(telemetry)
        self.communication.save(telemetry)

    def __check_connection(self) -> bool:
        if not self.communication.device_is_connected():
            self.logger.log("No connection to the device")
            self.main_window.update_device_connection_status(False)
            return False
        self.main_window.update_device_connection_status(True)

        if not self.communication.remote_device_is_connected():
            self.logger.log("No connection to the remote device")
            self.main_window.update_remote_device_connection_status(False)
            return False
        self.main_window.update_remote_device_connection_status(True)

        return True

    def __recieve_data(self) -> Telemetry | None:
        return self.communication.receive()

    def __is_simulation_mode(self) -> bool:
        return self.main_window.is_simulation_mode()

    def __has_simulated_pressure_commands(self) -> bool:
        return self.communication.has_simulated_pressure()

    def __send_next_simulated_pressure(self) -> None:
        self.communication.send_next_simulated_pressure()

    def __set_stylesheet(self) -> None:
        stylesheet = os.path.join(
            os.path.dirname(__file__), App.STYLESHEET_PATH
        )
        with open(stylesheet, "r") as file:
            self.setStyleSheet(file.read())

        pg.setConfigOption("background", Colours.SILVER.value)
        pg.setConfigOption("foreground", Colours.RICH_BLACK.value)

    def on_exit(self) -> None:
        self.logger.log("Exiting application")
        self.communication.close()
        self.timer.stop()
        self.quit()
