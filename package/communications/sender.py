from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice

from package.models.telemetry import OnOff, SimulationMode
from package.ui.log.log import Log
from package.constants import APP_INFO


class Sender:
    def __init__(
        self, device: XBeeDevice, remote_device: RemoteXBeeDevice
    ) -> None:
        self.device = device
        self.remote_device = remote_device
        self.logger = None
        self.simulated_pressure_commands = None

    def send(self, data: str) -> None:
        if not self.device.is_open():
            self.logger.log("Device is not open. Cannot send data.")
            return

        if not self.remote_device:
            self.logger.log("Remote device is not found. Cannot send data.")
            return

        if not data or data.isspace():
            self.logger.log("Data is empty. Cannot send data.")
            return

        self.device.send_data(self.remote_device, f"<{data}>")

    def payload_telemetry(self, on_off: OnOff) -> None:
        message = f"CMD, {APP_INFO.team_id()}, CX, {on_off}"
        self.logger.log(f"Sending: {message}")
        self.send(message)

    def set_time(self, time: str) -> None:
        message = f"CMD, {APP_INFO.team_id()}, ST, {time}"
        self.logger.log(f"Sending: {message}")
        self.send(message)

    def simulation_mode_control(self, mode: SimulationMode) -> None:
        message = f"CMD, {APP_INFO.team_id()}, SIM, {mode}"
        self.logger.log(f"Sending: {message}")
        self.send(message)

    def simulate_pressure(self, pressure: float) -> None:
        message = f"CMD, {APP_INFO.team_id()}, SIMP, {pressure}"
        self.logger.log(f"Sending: {message}")
        self.send(message)

    def calibrate_altitude(self) -> None:
        message = f"CMD, {APP_INFO.team_id()}, CAL"
        self.logger.log(f"Sending: {message}")
        self.send(message)

    def mechanism_actuation(self, on_off: OnOff) -> None:
        message = f"CMD, {APP_INFO.team_id()}, MEC, {on_off}"
        self.logger.log(f"Sending: {message}")
        self.send(message)

    def set_logger(self, logger: Log) -> None:
        self.logger = logger

    def has_simulated_pressure(self) -> bool:
        return self.simulated_pressure_commands is not None

    def set_simulated_pressure_commands(self, simulated_pressure_commands: list[str]) -> None:
        self.simulated_pressure_commands = simulated_pressure_commands

    def send_next_simulated_pressure(self) -> None:
        if not self.simulated_pressure_commands:
            return

        message = self.simulated_pressure_commands.pop(0)
        self.logger.log(f"Sending: {message}")
        self.send(message)
