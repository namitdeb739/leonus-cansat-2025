from enum import Enum
from package.models.app_info import AppInfo

# Application Info
APP_INFO = AppInfo(
    team_id=3171,
    team_name="LeoNUS",
    title="Cansat Telemetry & Ground Control",
)

# Geometry settings for different device types
GEOMETRY = {
    "laptop": (0, 0, 1440, 900),
    "monitor": (1440, 0, 1920, 1080),
}


# Colours
class Colours(Enum):
    SILVER = "#fefefe"
    NUS_BLUE = "#003d7c"
    NUS_ORANGE = "#ef7c00"
    RICH_BLACK = "#020612"
    JORDY_BLUE = "#a4c3f5"
    RED = "#d32f2f"  # Red for Roll
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
    GYRO_ROTATION_RATE = "Gyro Rot. Rate"
    ACCELERATION = "Accel."
    MAGNETOMETER = "Magnet."
    GPS_TIME = "GPS Time"
    GPS_LATITUDE = "GPS Latitude"
    GPS_LONGITUDE = "GPS Longitude"
    GPS_ALTITUDE = "GPS Altitude"
    GPS_SATELLITE_NUMBER = "GPS Satellite Number"
    COMMAND_ECHO = "Command Echo"
    DESCENT_RATE = "Descent Rate"
    GEOGRAPHIC_HEADING = "Geographic Heading"


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
    DESC_RATE = "DESC_RATE"
    GEOG_HEAD = "GEOG_HEAD"


class TelemetryUnits(Enum):
    ALTITUDE = "m"  # Meters
    TEMPERATURE = "°C"  # Degrees Celsius
    PRESSURE = "kPa"  # Kilopascals
    VOLTAGE = "V"  # Volts
    GYRO = "°s⁻¹"  # Degrees per second
    GYRO_ROTATION_RATE = "°s⁻¹"  # Degrees per second
    ACCELERATION = "°s⁻²"  # Degrees per second squared
    MAGNETOMETER = "G"  # Gauss
    GPS_TIME = ""  # No unit for GPS time
    GPS_LATITUDE = "°N"  # Degrees North
    GPS_LONGITUDE = "°E"  # Degrees East
    GPS_ALTITUDE = "m"  # Meters
    GPS_SATELLITE_NUMBER = ""  # No unit for satellite count
    COMMAND_ECHO = ""  # No unit for command echo
    DESCENT_RATE = "ms⁻¹"  # Meters per second
    GEOGRAPHIC_HEADING = "°"  # Degrees
