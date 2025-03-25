import sys
from digi.xbee.devices import XBeeDevice
import csv
import os
import time

import serial
import serial.tools
import serial.tools.list_ports
from package.models.telemetry import (
    GPS,
    OnOff,
    PrincipalAxesCoordinate,
    SimulationMode,
    Telemetry,
)

# import random


class Communication:
    PORT = ""
    BAUD_RATE = 9600
    REMOTE_NODE_ID = "PAYLOAD"

    def __init__(self, team_id: int) -> None:
        Communication.PORT = Communication.find_port()

        self.telemetry_data_string = None

        self.packet_count = 0
        self.team_id = team_id
        self.start_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        self.csv_file = f"logs/{self.start_time}/Flight_{self.team_id}.csv"
        self.store_enabled = False

        self.simulated_pressure_file_data = []

        print("Setting up device")
        self.device = XBeeDevice(Communication.PORT, Communication.BAUD_RATE)

        self.device.open()
        xbee_network = self.device.get_network()
        self.remote_device = xbee_network.discover_device(
            Communication.REMOTE_NODE_ID
        )
        self.device.add_data_received_callback(
            lambda xbee_message: self.set_telemetry_data_string(
                xbee_message.data.decode()
            )
        )
        print(f"Device initialised: {self.remote_device}")

        self.initialise_csv()

    def recieve(self) -> str:
        """
        Data formatted as:
        TEAM_ID, MISSION_TIME, PACKET_COUNT, MODE, STATE, ALTITUDE,
        TEMPERATURE, PRESSURE, VOLTAGE, GYRO_R,GYRO_P,GYRO_Y, ACCEL_R,
        ACCEL_P,ACCEL_Y, MAG_R,MAG_P,MAG_Y, AUTO_GYRO_ROTATION_RATE,
        GPS_TIME, GPS_ALTITUDE, GPS_LATITUDE, GPS_LONGITUDE, GPS_SATS,
        CMD_ECHO [,,OPTIONAL_DATA]
        """

        try:
            """mission_time = time.strftime("%H:%M:%S", time.localtime())
            self.packet_count += 1
            mode = random.choice(["F", "S"])
            state = random.choice(
                [
                    "LAUNCH_PAD",
                    "ASCENT",
                    "APOGEE",
                    "DESCENT",
                    "PROBE_RELEASE",
                    "LANDED",
                ]
            )
            altitude = round(random.uniform(0, 1000), 1)
            temperature = round(random.uniform(0, 100), 1)
            pressure = round(random.uniform(0, 1000), 1)
            voltage = round(random.uniform(0, 100), 1)
            gyro_r = round(random.uniform(0, 360), 1)
            gyro_p = round(random.uniform(0, 360), 1)
            gyro_y = round(random.uniform(0, 360), 1)
            accel_r = round(random.uniform(0, 360), 1)
            accel_p = round(random.uniform(0, 360), 1)
            accel_y = round(random.uniform(0, 360), 1)
            mag_r = round(random.uniform(0, 360), 1)
            mag_p = round(random.uniform(0, 360), 1)
            mag_y = round(random.uniform(0, 360), 1)
            auto_gyro_rotation_rate = round(random.uniform(0, 100), 1)
            gps_time = mission_time
            gps_altitude = altitude
            gps_latitude = round(random.uniform(0, 360), 1)
            gps_longitude = round(random.uniform(0, 360), 1)
            gps_sats = random.randint(0, 100)
            cmd_echo = "" """

            return (
                self.telemetry_data_string
                if self.telemetry_data_string
                else None
            )

            """ return f"{self.team_id},\
            {mission_time},\
            {self.packet_count},\
            {mode},\
            {state},\
            {altitude},\
            {temperature},\
            {pressure},\
            {voltage},\
            {gyro_r},\
            {gyro_p},\
            {gyro_y},\
            {accel_r},\
            {accel_p},\
            {accel_y},\
            {mag_r},\
            {mag_p},\
            {mag_y},\
            {auto_gyro_rotation_rate},\
            {gps_time},\
            {gps_altitude},\
            {gps_latitude},\
            {gps_longitude},\
            {gps_sats},\
            {cmd_echo}" """
        except Exception as e:
            print(e)

    def parse_data(self, data: str) -> Telemetry:
        if data is None:
            print("Passing")
            return None

        fields = data.split(",")
        (
            team_id,
            mission_time,
            packet_count,
            mode,
            state,
            altitude,
            temperature,
            pressure,
            voltage,
            gyro_r,
            gyro_p,
            gyro_y,
            accel_r,
            accel_p,
            accel_y,
            mag_r,
            mag_p,
            mag_y,
            auto_gyro_rotation_rate,
            gps_time,
            gps_altitude,
            gps_latitude,
            gps_longitude,
            gps_sats,
            cmd_echo,
        ) = [field.strip() for field in fields]

        if self.telemetry_time and time.strptime(
            self.telemetry_time, "%H:%M:%S"
        ) >= time.strptime(mission_time, "%H:%M:%S"):
            print("Passing")
            return None

        telemetry = Telemetry(
            team_id=int(team_id),
            mission_time=mission_time,
            packet_count=int(packet_count),
            mode=mode,
            state=state,
            altitude=float(altitude),
            temperature=float(temperature),
            pressure=float(pressure),
            voltage=float(voltage),
            gyro=PrincipalAxesCoordinate(
                roll=float(gyro_r),
                pitch=float(gyro_p),
                yaw=float(gyro_y),
            ),
            acceleration=PrincipalAxesCoordinate(
                roll=float(accel_r),
                pitch=float(accel_p),
                yaw=float(accel_y),
            ),
            magnetometer=PrincipalAxesCoordinate(
                roll=float(mag_r),
                pitch=float(mag_p),
                yaw=float(mag_y),
            ),
            auto_gyro_rotation_rate=float(auto_gyro_rotation_rate),
            gps=GPS(
                time=gps_time,
                altitude=float(gps_altitude) if gps_altitude else 0,
                latitude=float(gps_latitude) if gps_latitude else 0,
                longitude=float(gps_longitude) if gps_longitude else 0,
                sats=int(gps_sats),
            ),
            cmd_echo=cmd_echo,
        )

        self.telemetry_time = mission_time

        if self.store_enabled:
            self.log_data(telemetry)

        return telemetry

    def initialise_csv(self) -> None:
        os.makedirs(os.path.dirname(self.csv_file), exist_ok=True)
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                header = [
                    "TEAM_ID",
                    "MISSION_TIME",
                    "PACKET_COUNT",
                    "MODE",
                    "STATE",
                    "ALTITUDE",
                    "TEMPERATURE",
                    "PRESSURE",
                    "VOLTAGE",
                    "GYRO_R",
                    "GYRO_P",
                    "GYRO_Y",
                    "ACCEL_R",
                    "ACCEL_P",
                    "ACCEL_Y",
                    "MAG_R",
                    "MAG_P",
                    "MAG_Y",
                    "AUTO_GYRO_ROTATION_RATE",
                    "GPS_TIME",
                    "GPS_ALTITUDE",
                    "GPS_LATITUDE",
                    "GPS_LONGITUDE",
                    "GPS_SATS",
                    "CMD_ECHO",
                ]
                writer.writerow(header)

    def log_data(self, data: Telemetry) -> None:
        with open(self.csv_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            row = [
                data.team_id,
                data.mission_time,
                data.packet_count,
                data.mode,
                data.state,
                data.altitude,
                data.temperature,
                data.pressure,
                data.voltage,
                data.gyro.roll,
                data.gyro.pitch,
                data.gyro.yaw,
                data.acceleration.roll,
                data.acceleration.pitch,
                data.acceleration.yaw,
                data.magnetometer.roll,
                data.magnetometer.pitch,
                data.magnetometer.yaw,
                data.auto_gyro_rotation_rate,
                data.gps.time,
                data.gps.altitude,
                data.gps.latitude,
                data.gps.longitude,
                data.gps.sats,
                data.cmd_echo,
            ]
            writer.writerow(row)

    def send(self, data: str) -> None:
        if self.remote_device is None:
            print("Could not find the other device")
            exit(1)

        print(f"SENDING: {data}")

        # for char in f"<{data}>":
        self.device.send_data(self.remote_device, f"<{data}>")

    def payload_telemetry(self, on_off: OnOff) -> None:
        send_string = f"CMD, {self.team_id}, CX, {on_off}"
        self.send(send_string)

    def set_time(self, time: str) -> None:
        send_string = f"CMD, {self.team_id}, ST, {time}"
        self.send(send_string)

    def simulation_mode_control(self, mode: SimulationMode) -> None:
        send_string = f"CMD, {self.team_id}, SIM, {mode}"
        self.send(send_string)

    def simulate_pressure(self, pressure: float) -> None:
        send_string = f"CMD, {self.team_id}, SIMP, {pressure}"
        self.send(send_string)

    def simulate_pressure_file(self, file_contents: str) -> None:
        self.simulated_pressure_file_data = [
            f"CMD, {self.team_id}, SIMP, {pressure}"
            for pressure in file_contents.splitlines()
        ]

    def send_simulated_pressure(self) -> None:
        if self.simulated_pressure_file_data:
            send_string = self.simulated_pressure_file_data.pop(0)
            self.send(send_string)

    def calibrate_altitude(self) -> None:
        send_string = f"CMD, {self.team_id}, CAL"
        self.send(send_string)

    def mechanism_actuation(self, on_off: OnOff) -> None:
        send_string = f"CMD, {self.team_id}, MEC, {on_off}"
        self.send(send_string)

    @staticmethod
    def find_port() -> str:
        return "/dev/tty.usbserial-D30DP553"
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "USB" in port.device:
                return port.device
        sys.exit("No USB port found")

    def set_telemetry_data_string(self, data: str) -> None:
        print(data)
        self.telemetry_data_string = data[1:-2] if data else None
