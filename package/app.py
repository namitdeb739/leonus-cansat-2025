import atexit
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from package.communications.communication import Communication
from package.constants import APP_INFO, GEOMETRY
from package.models.telemetry import (
    Telemetry,
)
from package.ui.main_window import MainWindow
import os
import pyqtgraph as pg
from package.config import DevMode
from package.constants import Colours


class App(QApplication):

    STYLESHEET_PATH = "./styles/styles.css"
    ONE_SECOND = 1000
    TIMER_INTERVAL = 250

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

        self.update_call_count = 0

        atexit.register(self.on_exit)

        self.last_recieved_packet = 0

    def run(self) -> int:
        self.main_window.show()
        self.__setup_timer(App.TIMER_INTERVAL)

        return self.exec()

    def __setup_timer(self, interval: int) -> None:
        self.timer = QTimer()
        self.timer.timeout.connect(self.__update)
        self.timer.start(interval)

    def __update(self) -> None:
        if self.communication.sender_initialised():
            self.main_window.activate_control_panel()
        else:
            self.main_window.deactivate_control_panel()

        self.update_call_count = (self.update_call_count + 1) % (
            App.ONE_SECOND // App.TIMER_INTERVAL
        )
        self.main_window.update_time()

        if not self.__check_connection():
            return

        self.__receive_telemetry()

        if (
            self.__is_simulation_mode()
            and self.__has_simulated_pressure_commands()
            and self.update_call_count == 0
        ):
            self.__send_next_simulated_pressure()

    def __receive_telemetry(self) -> None:
        telemetry = self.__recieve_data()
        if telemetry is None:
            return

        if self.__package_drop_detected(telemetry):
            self.logger.log(
                f"Telemetry packet count mismatch: {self.last_recieved_packet} -> {telemetry.packet_count}. Missing packets {[i for i in range(self.last_recieved_packet + 1, telemetry.packet_count)]}"
            )

        if self.__package_backwards_detected(telemetry):
            self.logger.log(
                f"Telemetry packet count backwards: {self.last_recieved_packet} -> {telemetry.packet_count}. Resetting telemetry packet number."
            )

        self.main_window.update(telemetry)
        self.communication.save(telemetry)
        self.last_recieved_packet = telemetry.packet_count

    def __package_drop_detected(self, telemetry: Telemetry) -> bool:
        return telemetry.packet_count - self.last_recieved_packet > 1

    def __package_backwards_detected(self, telemetry: Telemetry) -> bool:
        return (
            telemetry.packet_count < self.last_recieved_packet
            and telemetry.packet_count != 0
        )

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
