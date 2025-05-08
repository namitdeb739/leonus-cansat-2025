import queue
from digi.xbee.devices import XBeeDevice
from package.models.telemetry import Telemetry, PrincipalAxesCoordinate, GPS
from package.ui.log.log import Log


class Receiver:
    DATA_START_INDEX, DATA_END_INDEX = 1, -2
    FIELD_COUNT = 27

    def __init__(self, device: XBeeDevice) -> None:
        self.device = device
        self.data_queue: queue.Queue[str] = queue.Queue()
        self.packet_count = -1
        self.logger = None
        self.device.add_data_received_callback(
            lambda xbee_message: self.__data_received_callback(
                xbee_message.data.decode()
            )
        )

    def __data_received_callback(self, data: str) -> None:
        try:
            raw_data = data.data.decode()[
                Receiver.DATA_START_INDEX : Receiver.DATA_END_INDEX
            ]
            self.data_queue.put(raw_data)
        except OSError as e:
            if self.logger:
                self.logger.log(f"OS error in data callback: {e}")
        except Exception as e:
            if self.logger:
                self.logger.log(f"Error in data callback: {e}")

    def __parse_data(self, data: str) -> Telemetry:
        if not data:
            return None

        fields = data.split(",")

        if len(fields) != Receiver.FIELD_COUNT:
            self.logger.log(
                f"Invalid data format. Expected {Receiver.FIELD_COUNT} fields, got {len(fields)}"
            )
            return None

        try:
            team_id = int(fields[0])
            mission_time = fields[1]
            packet_count = int(fields[2])
            mode = fields[3]
            state = fields[4]
            altitude = float(fields[5])
            temperature = float(fields[6])
            pressure = float(fields[7])
            voltage = float(fields[8])
            gyro_r, gyro_p, gyro_y = map(float, fields[9:12])
            accel_r, accel_p, accel_y = map(float, fields[12:15])
            mag_r, mag_p, mag_y = map(float, fields[15:18])
            auto_gyro_rotation_rate = float(fields[18])
            gps_time = fields[19]
            gps_altitude = float(fields[20])
            gps_latitude = float(fields[21])
            gps_longitude = float(fields[22])
            gps_sats = int(fields[23])
            cmd_echo = fields[24]
            descent_rate = float(fields[25])
            geographic_heading = int(fields[26])

            return Telemetry(
                team_id=team_id,
                mission_time=mission_time,
                packet_count=packet_count,
                mode=mode,
                state=state,
                altitude=altitude,
                temperature=temperature,
                pressure=pressure,
                voltage=voltage,
                gyro=PrincipalAxesCoordinate(
                    roll=gyro_r, pitch=gyro_p, yaw=gyro_y
                ),
                acceleration=PrincipalAxesCoordinate(
                    roll=accel_r, pitch=accel_p, yaw=accel_y
                ),
                magnetometer=PrincipalAxesCoordinate(
                    roll=mag_r, pitch=mag_p, yaw=mag_y
                ),
                auto_gyro_rotation_rate=auto_gyro_rotation_rate,
                gps=GPS(
                    time=gps_time,
                    altitude=gps_altitude,
                    latitude=gps_latitude,
                    longitude=gps_longitude,
                    sats=gps_sats,
                ),
                cmd_echo=cmd_echo,
                descent_rate=descent_rate,
                geographic_heading=geographic_heading,
            )
        except (ValueError, TypeError) as e:
            if self.logger:
                self.logger.log(f"Error parsing telemetry data: {e}")
            return None

    def receive(self) -> Telemetry:
        if not self.device.is_open():
            if self.logger:
                self.logger.log("Device is not open. Cannot receive data.")
            return None

        try:
            raw_data = self.data_queue.get_nowait()
        except queue.Empty:
            if self.logger:
                self.logger.log("No data available in the queue.")
            return None

        telemetry = self.__parse_data(raw_data)
        if telemetry and telemetry.packet_count == self.packet_count:
            if self.logger:
                self.logger.log(
                    "No new data received (packet count unchanged)."
                )
            return None

        self.packet_count = telemetry.packet_count
        return telemetry

    def set_logger(self, logger: Log) -> None:
        self.logger = logger
