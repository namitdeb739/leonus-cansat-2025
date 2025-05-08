from ast import Constant
import csv
from io import TextIOWrapper
import time
from package import constants
from package.communications.plotter import Plotter
from package.models.telemetry import Telemetry
from package.ui.log.log import Log
import os


class Store:
    def __init__(self) -> None:
        self.start_time = time.strftime("%m%d_%H%M%S", time.localtime())
        self.file_path = (
            f"logs/{self.start_time}/Flight_{constants.APP_INFO.team_id()}.csv"
        )

        self.file = self.__open_file()
        self.writer = csv.writer(self.file)
        self.__write_header()
        self.enabled = False
        self.enable()

        self.logger = None
        self.plotter = Plotter(self.start_time, self.file_path)

    def __open_file(self) -> TextIOWrapper:
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        return open(self.file_path, mode="a", newline="",buffering=1)

    def __write_header(self) -> None:
        self.writer.writerow(
            [
                constants.TelemetryFieldsCSVHeadings.TEAM_ID.value,
                constants.TelemetryFieldsCSVHeadings.MISSION_TIME.value,
                constants.TelemetryFieldsCSVHeadings.PACKET_COUNT.value,
                constants.TelemetryFieldsCSVHeadings.MODE.value,
                constants.TelemetryFieldsCSVHeadings.STATE.value,
                constants.TelemetryFieldsCSVHeadings.ALTITUDE.value,
                constants.TelemetryFieldsCSVHeadings.TEMPERATURE.value,
                constants.TelemetryFieldsCSVHeadings.PRESSURE.value,
                constants.TelemetryFieldsCSVHeadings.VOLTAGE.value,
                constants.TelemetryFieldsCSVHeadings.GYRO_R.value,
                constants.TelemetryFieldsCSVHeadings.GYRO_P.value,
                constants.TelemetryFieldsCSVHeadings.GYRO_Y.value,
                constants.TelemetryFieldsCSVHeadings.ACCEL_R.value,
                constants.TelemetryFieldsCSVHeadings.ACCEL_P.value,
                constants.TelemetryFieldsCSVHeadings.ACCEL_Y.value,
                constants.TelemetryFieldsCSVHeadings.MAG_R.value,
                constants.TelemetryFieldsCSVHeadings.MAG_P.value,
                constants.TelemetryFieldsCSVHeadings.MAG_Y.value,
                constants.TelemetryFieldsCSVHeadings.AUTO_GYRO_ROTATION_RATE.value,
                constants.TelemetryFieldsCSVHeadings.GPS_TIME.value,
                constants.TelemetryFieldsCSVHeadings.GPS_ALTITUDE.value,
                constants.TelemetryFieldsCSVHeadings.GPS_LATITUDE.value,
                constants.TelemetryFieldsCSVHeadings.GPS_LONGITUDE.value,
                constants.TelemetryFieldsCSVHeadings.GPS_SATS.value,
                constants.TelemetryFieldsCSVHeadings.CMD_ECHO.value,
                constants.TelemetryFieldsCSVHeadings.DESC_RATE.value,
                constants.TelemetryFieldsCSVHeadings.GEOG_HEAD.value,
            ]
        )

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False

    def write(self, telemetry: Telemetry) -> None:
        if not self.enabled:
            return
        self.writer.writerow(
            [
                telemetry.team_id,
                telemetry.mission_time,
                telemetry.packet_count,
                telemetry.mode,
                telemetry.state,
                telemetry.altitude,
                telemetry.temperature,
                telemetry.pressure,
                telemetry.voltage,
                telemetry.gyro.roll,
                telemetry.gyro.pitch,
                telemetry.gyro.yaw,
                telemetry.acceleration.roll,
                telemetry.acceleration.pitch,
                telemetry.acceleration.yaw,
                telemetry.magnetometer.roll,
                telemetry.magnetometer.pitch,
                telemetry.magnetometer.yaw,
                telemetry.auto_gyro_rotation_rate,
                telemetry.gps.time,
                telemetry.gps.altitude,
                telemetry.gps.latitude,
                telemetry.gps.longitude,
                telemetry.gps.sats,
                telemetry.cmd_echo,
                telemetry.descent_rate,
                telemetry.geographic_heading,
            ]
        )

    def close(self) -> None:
        self.file.close()
        if (
            os.stat(self.file_path).st_size == 0
            or sum(1 for _ in open(self.file_path)) == 1
        ):
            os.remove(self.file_path)
            parent_dir = os.path.dirname(self.file_path)
            if not os.listdir(parent_dir):
                os.rmdir(parent_dir)
            return
        self.plotter.generate_plots()

    def set_logger(self, logger: Log) -> None:
        self.logger = logger
        self.logger.log(f"Telemetry data is being stored in {self.file_path}")
