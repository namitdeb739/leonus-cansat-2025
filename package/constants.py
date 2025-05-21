from enum import Enum
from package.models.app_info import AppInfo


APP_INFO = AppInfo(
    team_id=3171,
    team_name="LeoNUS",
    title="Cansat Telemetry & Ground Control",
)


GEOMETRY = {
    "laptop": (0, 0, 1440, 900),
    "monitor": (1440, 0, 1920, 1080),
}


class Colours(Enum):
    SILVER = "#fefefe"
    NUS_BLUE = "#003d7c"
    NUS_ORANGE = "#ef7c00"
    RICH_BLACK = "#020612"
    JORDY_BLUE = "#a4c3f5"
    RED = "#d32f2f"
    GREEN = "#388e3c"
    LIGHT_GREY = "#f0f0f0"
    BLACK = "#000000"


class TelemetryFields(Enum):
    TIME = "Time"
    PACKET_COUNT = "Packet Count"
    MODE = "Mode"
    STATE = "State"
    ALTITUDE = "Altitude"
    TEMPERATURE = "Temperature"
    PRESSURE = "Pressure"
    VOLTAGE = "Voltage"
    GYRO = "Gyro"
    GYRO_ROTATION_RATE = "Gyro Rotation Rate"
    ACCELERATION = "Acceleration"
    MAGNETOMETER = "Magnetometer"
    GPS_TIME = "GPS Time"
    GPS_LATITUDE = "GPS Latitude"
    GPS_LONGITUDE = "GPS Longitude"
    GPS_ALTITUDE = "GPS Altitude"
    GPS_SATELLITE_NUMBER = "Satellite No."
    COMMAND_ECHO = "Command Echo"
    DESCENT_RATE = "Descent Rate"
    GEOGRAPHIC_HEADING = "Heading"


class TelemetryFieldsCSVHeadings(Enum):
    TEAM_ID = "TEAM_ID"
    MISSION_TIME = "MISSION_TIME"
    PACKET_COUNT = "PACKET_COUNT"
    MODE = "MODE"
    STATE = "STATE"
    ALTITUDE = "ALTITUDE"
    TEMPERATURE = "TEMPERATURE"
    PRESSURE = "PRESSURE"
    VOLTAGE = "VOLTAGE"
    GYRO_R = "GYRO_R"
    GYRO_P = "GYRO_P"
    GYRO_Y = "GYRO_Y"
    ACCEL_R = "ACCEL_R"
    ACCEL_P = "ACCEL_P"
    ACCEL_Y = "ACCEL_Y"
    MAG_R = "MAG_R"
    MAG_P = "MAG_P"
    MAG_Y = "MAG_Y"
    AUTO_GYRO_ROTATION_RATE = "AUTO_GYRO_ROTATION_RATE"
    GPS_TIME = "GPS_TIME"
    GPS_ALTITUDE = "GPS_ALTITUDE"
    GPS_LATITUDE = "GPS_LATITUDE"
    GPS_LONGITUDE = "GPS_LONGITUDE"
    GPS_SATS = "GPS_SATS"
    CMD_ECHO = "CMD_ECHO"
    BLANK = ""
    DESC_RATE = "DESC_RATE"
    GEOG_HEAD = "GEOG_HEAD"


class TelemetryUnits(Enum):
    ALTITUDE = "m"
    TEMPERATURE = "°C"
    PRESSURE = "kPa"
    VOLTAGE = "V"
    GYRO = "°s⁻¹"
    GYRO_ROTATION_RATE = "°s⁻¹"
    ACCELERATION = "°s⁻²"
    MAGNETOMETER = "G"
    GPS_TIME = ""
    GPS_LATITUDE = "°N"
    GPS_LONGITUDE = "°E"
    GPS_ALTITUDE = "m"
    GPS_SATELLITE_NUMBER = ""
    COMMAND_ECHO = ""
    DESCENT_RATE = "ms⁻¹"
    GEOGRAPHIC_HEADING = "°"


class Mechanism(Enum):
    CAM1 = "CAM1"
    CAM2 = "CAM2"
    GYRO = "GYRO"
