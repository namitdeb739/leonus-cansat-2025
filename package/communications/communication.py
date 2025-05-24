import time
from serial import SerialException
from package import constants
from package.communications.sender import Sender
from package.communications.receiver import Receiver
from digi.xbee.devices import XBeeDevice
from digi.xbee.exception import (
    InvalidOperatingModeException,
)
import serial.tools.list_ports
from package.communications.store import Store
from package.exceptions.SenderNotInitialisedException import (
    SenderNotInitialisedException,
)
from package.models.telemetry import (
    OnOff,
    SimulationMode,
    Telemetry,
    TimeSource,
)
from package.ui.log.log import Log


class Communication:
    BAUD_RATE = 9600
    REMOTE_NODE_ID = "PAYLOAD"
    SENDER_NOT_INITIALISED_MESSAGE = (
        "Sender is not initialised or not connected. Cannot %s."
    )

    def __init__(self) -> None:
        self.device = None
        self.remote_device = None
        self.sender = None
        self.receiver = None
        self.logger = None

        self.store = Store()

    def initialise_connection(self, port: str) -> None:
        self.__initialise_device(port)
        self.initialise_remote_device()

        if not self.device:
            self.logger.log(
                "Device not initialised. Cannot establish connection."
            )
            return
        self.__initialise_receiver()

        if not self.remote_device:
            self.logger.log(
                "Remote device not found. Cannot establish connection."
            )
            return
        self.__initialise_sender()

    def __initialise_receiver(self) -> None:
        self.logger.log("Initialising receiver...")
        self.receiver = Receiver(self.device)
        self.receiver.set_logger(self.logger)

    def __initialise_sender(self) -> None:
        self.logger.log("Initialising sender...")
        self.sender = Sender(self.device, self.remote_device)
        self.sender.set_logger(self.logger)

    def __initialise_device(self, port: str) -> None:
        self.logger.log("Initialising device...")
        self.device = XBeeDevice(port, Communication.BAUD_RATE)
        try:
            self.device.open()
            self.logger.log(f"Device opened on port: {port}")
        except InvalidOperatingModeException as e:
            self.logger.log(f"Error opening device: {e}")
            return

    def initialise_remote_device(self) -> None:
        if not self.device.is_open():
            self.logger.log(
                "Device is not open. Cannot initialise remote device."
            )
            return

        self.logger.log("Initialising remote device...")

        # network = self.device.get_network()
        # network.start_discovery_process()
        # self.logger.log(f"Network devices: {network.get_devices()}")

        self.remote_device = self.device.get_network().discover_device(
            Communication.REMOTE_NODE_ID
        )
        if self.remote_device:
            self.logger.log(
                f"Remote device found: {self.remote_device.get_node_id()}"
            )
        else:
            self.logger.log("Remote device not found.")
            # self.device.close()

    def connect_remote_device(self) -> None:
        self.initialise_remote_device()
        self.__initialise_sender()

    def close(self) -> None:
        self.logger.log("Closing device...")
        if self.device and self.device.is_open():
            self.device.close()

        self.logger.log("Closing store...")
        self.store.close(
            self.receiver.time_recieved_first_packet if self.receiver else None
        )

    @staticmethod
    def find_ports() -> list[str]:
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def set_logger(self, logger: Log) -> None:
        self.logger = logger
        self.store.set_logger(logger)

    def device_is_connected(self) -> bool:
        return self.device and self.device.is_open()

    def remote_device_is_connected(self) -> bool:
        return self.remote_device is not None

    def receive(self) -> Telemetry:

        try:
            if not self.device or not self.device.is_open():
                self.logger.log("Device is not open. Cannot receive data.")

                return None

            if not self.remote_device:
                self.logger.log(
                    "Remote device is not found. Cannot receive data."
                )

                return None

            if not self.receiver:
                self.logger.log(
                    "Receiver is not initialised. Cannot receive data."
                )

                return None

            return self.receiver.receive()
        except (OSError, SerialException) as e:
            self.logger.log(f"Error receiving data: {e}")
            self.device.close()

            return None

    def has_simulated_pressure(self) -> bool:
        if not self.sender:
            self.logger.log(
                Communication.SENDER_NOT_INITIALISED_MESSAGE
                % "check simulated pressure"
            )
            return False

        return self.sender.has_simulated_pressure()

    def start(self) -> None:
        if not self.sender:
            self.logger.log(
                Communication.SENDER_NOT_INITIALISED_MESSAGE % "start"
            )
            raise SenderNotInitialisedException()

        self.sender.start()

    def enable_store(self) -> None:
        self.logger.log("Enabling telemetry storage...")
        self.store.enable()

    def disable_store(self) -> None:
        self.logger.log("Disabling telemetry storage...")
        self.store.disable()

    def payload_telemetry(self, on_off: OnOff) -> None:
        if not self.sender:
            self.logger.log(
                Communication.SENDER_NOT_INITIALISED_MESSAGE % "send telemetry"
            )
            raise SenderNotInitialisedException()

        self.sender.payload_telemetry(on_off)

    def set_time(self, time_source: TimeSource) -> None:
        if not self.sender:
            self.logger.log(
                Communication.SENDER_NOT_INITIALISED_MESSAGE % "set time"
            )
            raise SenderNotInitialisedException()

        time_str = (
            time_source.value
            if time_source == TimeSource.GPS
            else time.strftime("%H:%M:%S", time.localtime())
        )
        self.sender.set_time(time_str)

    def calibrate_altitude(self) -> None:
        if not self.sender:
            self.logger.log(
                Communication.SENDER_NOT_INITIALISED_MESSAGE
                % "calibrate altitude"
            )
            raise SenderNotInitialisedException()

        self.sender.calibrate_altitude()

    def reset_eeprom(self) -> None:
        if not self.sender:
            self.logger.log(
                Communication.SENDER_NOT_INITIALISED_MESSAGE % "reset eeprom"
            )
            raise SenderNotInitialisedException()

        self.sender.reset_eeprom()

    def mechanism_actuation(self, device: str, on_off: OnOff) -> None:
        if not self.sender:
            self.logger.log(
                Communication.SENDER_NOT_INITIALISED_MESSAGE
                % "send send mechanism actuation"
            )
            raise SenderNotInitialisedException()

        self.sender.mechanism_actuation(device, on_off)

    def parse_simulate_pressure_file(self, file_contents: str) -> None:
        if not self.sender:
            self.logger.log(
                Communication.SENDER_NOT_INITIALISED_MESSAGE
                % "parse simulated pressure file"
            )
            raise SenderNotInitialisedException()

        simulated_pressure_commands = [
            pressure_command.split(",")[0]
            + ", "
            + str(constants.APP_INFO.team_id())
            + ", "
            + pressure_command.split(",")[2]
            + ", "
            + pressure_command.split(",")[3]
            for pressure_command in file_contents.splitlines()
            if pressure_command.strip() != "" and pressure_command[0] != "#"
        ]

        self.sender.set_simulated_pressure_commands(
            simulated_pressure_commands
        )

    def simulation_mode_control(self, mode: SimulationMode) -> None:
        if not self.sender:
            self.logger.log(
                Communication.SENDER_NOT_INITIALISED_MESSAGE
                % "control simulation mode"
            )
            raise SenderNotInitialisedException()

        self.sender.simulation_mode_control(mode)

    def send_next_simulated_pressure(self) -> None:
        if not self.sender:
            self.logger.log(
                Communication.SENDER_NOT_INITIALISED_MESSAGE
                % "send next simulated pressure"
            )
            return

        if not self.sender.has_simulated_pressure():
            return

        self.sender.send_next_simulated_pressure()

    def save(self, telemetry: Telemetry) -> None:
        self.store.write(telemetry)

    def sender_initialised(self) -> bool:
        return self.sender is not None and self.sender.is_initialised()
