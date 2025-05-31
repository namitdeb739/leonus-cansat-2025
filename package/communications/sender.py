from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
from digi.xbee.exception import XBeeException
from package.models.telemetry import OnOff, SimulationMode
from package.ui.log.log import Log
from package.constants import APP_INFO


class Sender:
    MESSAGE = "CMD, {team_id}, {cmd}"

    def __init__(
        self,
        device: XBeeDevice,
        remote_device: RemoteXBeeDevice,
    ) -> None:
        self.device = device
        self.remote_device = remote_device
        self.logger = None
        self.simulated_pressure_commands = None

    @staticmethod
    def __make_message(cmd: str) -> str:
        return Sender.MESSAGE.format(
            team_id=APP_INFO.team_id(),
            cmd=cmd,
        )

    def __send(self, command: str) -> None:
        message = self.__make_message(command)

        if not self.device.is_open():
            self.logger.log("Device is not open. Cannot send data.")
            return

        if not self.remote_device:
            self.logger.log("Remote device is not found. Cannot send data.")
            return

        if not message or message.isspace():
            self.logger.log("Data is empty. Cannot send data.")
            return

        try:
            self.logger.log(f"Sending: {message}")
            self.device.send_data(self.remote_device, f"<{message}>")
        except XBeeException as e:
            self.logger.log(f"Error sending data: {e}")

    def start(self) -> None:
        self.__send("START")

    def payload_telemetry(self, on_off: OnOff) -> None:
        self.__send(f"CX, {on_off}")

    def set_time(self, time: str) -> None:
        self.__send(f"ST, {time}")

    def simulation_mode_control(self, mode: SimulationMode) -> None:
        self.simulated_pressure_commands = []
        self.__send(f"SIM, {mode}")

    def simulate_pressure(self, pressure: float) -> None:
        self.__send(f"SIMP, {pressure}")

    def calibrate_altitude(self) -> None:
        self.__send("CAL")

    def calibrate_imu(self) -> None:
        self.__send("CALIMU")

    def reset_eeprom(self) -> None:
        self.__send("RST")

    def mechanism_actuation(self, device: str, on_off: OnOff) -> None:
        self.__send(f"MEC, {device}, {on_off}")

    def send_next_simulated_pressure(self) -> None:
        if (
            not self.simulated_pressure_commands
            or len(self.simulated_pressure_commands) == 0
        ):
            return

        self.__send(self.simulated_pressure_commands.pop(0))

        if len(self.simulated_pressure_commands) == 0:
            self.logger.log("All simulated pressure commands have been sent.")

    def set_logger(self, logger: Log) -> None:
        self.logger = logger

    def has_simulated_pressure(self) -> bool:
        return (
            self.simulated_pressure_commands is not None
            and len(self.simulated_pressure_commands) > 0
        )

    def set_simulated_pressure_commands(
        self, simulated_pressure_commands: list[str]
    ) -> None:
        self.simulated_pressure_commands = simulated_pressure_commands

    def is_initialised(self) -> bool:
        return self.device.is_open() and self.remote_device is not None
