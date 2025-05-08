from enum import Enum
from abc import ABC
from dataclasses import dataclass


class Mode(Enum):
    FLIGHT = "F"
    SIMULATION = "S"

    def __str__(self) -> str:
        if self == Mode.FLIGHT:
            return "Flight"
        elif self == Mode.SIMULATION:
            return "Simulation"


class State(Enum):
    LAUNCH_PAD = "LAUNCH_PAD"
    ASCENT = "ASCENT"
    APOGEE = "APOGEE"
    DESCENT = "DESCENT"
    PROBE_RELEASE = "PROBE_RELEASE"
    LANDED = "LANDED"

    def __str__(self) -> str:
        if self == State.LAUNCH_PAD:
            return "Launch Pad"
        elif self == State.ASCENT:
            return "Ascent"
        elif self == State.APOGEE:
            return "Apogee"
        elif self == State.DESCENT:
            return "Descent"
        elif self == State.PROBE_RELEASE:
            return "Probe Release"
        elif self == State.LANDED:
            return "Landed"


@dataclass
class PrincipalAxesCoordinate:
    roll: float
    pitch: float
    yaw: float

    def __str__(self) -> str:
        return f"({self.roll}, {self.pitch}, {self.yaw})"


@dataclass
class GPS:
    time: str
    altitude: float
    latitude: float
    longitude: float
    sats: int

    def __str__(self) -> str:
        return f"UTC {self.time}, ({self.latitude}°N, {self.longitude}°E), \
            {self.altitude}m, {self.sats}"


class Command(ABC):
    class CommandType(Enum):
        PAYLOAD_TELEMETRY = "CX"
        SET_TIME = "ST"
        SIMULATION_MODE_CONTROL = "SIM"
        SIMULATED_PRESSURE_DATA = "SIMP"
        CALIBRATE_ALTITUDE_TO_ZERO = "CAL"
        MECHANISM_ACTUATION = "MEC"

    type: CommandType

    def __init__(self, type: CommandType) -> None:
        self.type = type

    @staticmethod
    def command(type: CommandType, data: bool) -> None:
        if type == Command.CommandType.PAYLOAD_TELEMETRY:
            return PayloadTelemetryCommand(data)
        elif type == Command.CommandType.SET_TIME:
            return SetTimeCommand(data)
        elif type == Command.CommandType.SIMULATION_MODE_CONTROL:
            return SimulationModeControlCommand(data)
        elif type == Command.CommandType.SIMULATED_PRESSURE_DATA:
            return SimulatedPressureDataCommand(data)
        elif type == Command.CommandType.CALIBRATE_ALTITUDE_TO_ZERO:
            return CalibrateAltitudeToZeroCommand(data)
        elif type == Command.CommandType.MECHANISM_ACTUATION:
            return MechanismActuationCommand(data)


class OnOff(Enum):
    ON = "ON"
    OFF = "OFF"

    def __str__(self) -> str:
        return self.value

class TimeSource(Enum):
    GPS = "GPS"
    GCS = "GCS"

    def __str__(self) -> str:
        return self.value

@dataclass
class PayloadTelemetryCommand(Command):

    on_off: OnOff

    def __init__(self, on_off: str) -> None:
        super().__init__(Command.CommandType.PAYLOAD_TELEMETRY)
        self.on_off = OnOff(on_off)

    def __str__(self) -> str:
        return f"{self.type.value}{self.on_off}"


@dataclass
class SetTimeCommand(Command):
    time: str

    def __init__(self, time: str, gps_time: str | None) -> None:
        super().__init__(Command.CommandType.SET_TIME)
        if time == "GPS":
            self.time = gps_time
        else:
            self.time = time

    def __str__(self) -> str:
        return f"{self.type.value}{self.time}"


class SimulationMode(Enum):
    ENABLE = "ENABLE"
    ACTIVATE = "ACTIVATE"
    DISABLE = "DISABLE"

    def __str__(self) -> str:
        return self.value


@dataclass
class SimulationModeControlCommand(Command):

    mode: SimulationMode

    def __init__(self, mode: str) -> None:
        super().__init__(Command.CommandType.SIMULATION_MODE_CONTROL)
        self.mode = SimulationMode(mode)

    def __str__(self) -> str:
        return f"{self.type.value}{self.mode}"


@dataclass
class SimulatedPressureDataCommand(Command):
    pressure: int

    def __init__(self, pressure: int) -> None:
        super().__init__(Command.CommandType.SIMULATED_PRESSURE_DATA)
        self.pressure = pressure


@dataclass
class CalibrateAltitudeToZeroCommand(Command):
    def __init__(self) -> None:
        super().__init__(Command.CommandType.CALIBRATE_ALTITUDE_TO_ZERO)

    def __str__(self) -> str:
        return f"{self.type.value}"


@dataclass
class MechanismActuationCommand(Command):
    device: str
    on_off: OnOff

    def __init__(self, device: str, on_off: str) -> None:
        super().__init__(Command.CommandType.MECHANISM_ACTUATION)
        self.device = device
        self.on_off = OnOff(on_off)

    def __str__(self) -> str:
        return f"{self.type.value}{self.device}{self.on_off}"


@dataclass
class Telemetry:
    team_id: int
    mission_time: str
    packet_count: int
    mode: Mode
    state: State
    altitude: float
    temperature: float
    pressure: float
    voltage: float
    gyro: PrincipalAxesCoordinate
    acceleration: PrincipalAxesCoordinate
    magnetometer: PrincipalAxesCoordinate
    auto_gyro_rotation_rate: int
    gps: GPS
    cmd_echo: Command
    descent_rate: float
    geographic_heading: int

    def header(self) -> tuple[int, str, int]:
        return self.team_id, self.mission_time, self.packet_count

    def gps_time(self) -> str:
        return self.gps.time

    def gps_latitude(self) -> float:
        return self.gps.latitude

    def gps_longitude(self) -> float:
        return self.gps.longitude

    def gps_altitude(self) -> float:
        return self.gps.altitude

    def gps_sats(self) -> int:
        return self.gps.sats
