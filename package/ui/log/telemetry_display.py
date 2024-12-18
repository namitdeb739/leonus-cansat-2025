from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout, QSizePolicy
from PyQt6.QtCore import Qt
from package.models.telemetry import Telemetry


class TelemetryDisplay(QWidget):
    def __init__(self, telemetry: Telemetry):
        super().__init__()
        self.setObjectName("TelemetryDisplay")

        self.telemetry = telemetry

        self.mission_time = QLabel(
            f"<b>Time:</b> UTC {self.telemetry.mission_time}"
        )
        self.packet_count = QLabel(
            f"<b>Packet Count:</b> {self.telemetry.packet_count}"
        )
        self.mode = QLabel(f"<b>Mode:</b> {self.telemetry.mode}")
        self.state = QLabel(f"<b>State:</b> {self.telemetry.state}")
        self.altitude = QLabel(f"<b>Altitude:</b> {self.telemetry.altitude}m")
        self.temperature = QLabel(
            f"<b>Temperature:</b> {self.telemetry.temperature}°C"
        )
        self.pressure = QLabel(
            f"<b>Pressure:</b> {self.telemetry.pressure}kPa"
        )
        self.voltage = QLabel(f"<b>Voltage:</b> {self.telemetry.voltage}V")
        self.gyro = QLabel(
            f"<b>Gyro:</b> {self.telemetry.gyro}°s<sup>-2</sup>"
        )
        self.acceleration = QLabel(
            f"<b>Acc.:</b> \
                {self.telemetry.acceleration}ms<sup>-2</sup>"
        )
        self.magnetometer = QLabel(
            f"<b>Mag.:</b> {self.telemetry.magnetometer}G"
        )
        self.auto_gryro_rotation_rate = QLabel(
            f"<b>Gyro Rot. Rate:</B> \
                {self.telemetry.auto_gyro_rotation_rate}°s<sup>-2</sup>"
        )
        self.gps = QLabel(
            f"<b>GPS:</b> \
                {self.telemetry.gps}"
        )
        self.cmd_echo: QLabel = QLabel(
            f"<b>Command Echo:</b> {self.telemetry.cmd_echo}"
        )

        self.build_layout()

    def build_layout(self) -> None:
        layout = QGridLayout()

        labels = [
            [self.mission_time, self.packet_count],
            [self.mode, self.state],
            [self.altitude, self.temperature],
            [self.pressure, self.voltage],
            [self.gyro, self.auto_gryro_rotation_rate],
            [self.acceleration, self.magnetometer],
            [self.gps],
            [self.cmd_echo],
        ]

        for i, row in enumerate(labels):
            for j, label in enumerate(row):
                if len(row) == 1:
                    layout.addWidget(
                        label, i, j, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft
                    )
                    label.setSizePolicy(
                        QSizePolicy.Policy.Maximum,
                        QSizePolicy.Policy.Minimum,
                    )
                    continue
                layout.addWidget(
                    label, i, j, alignment=Qt.AlignmentFlag.AlignLeft
                )
                label.setSizePolicy(
                    QSizePolicy.Policy.Fixed,
                    QSizePolicy.Policy.Minimum,
                )

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setLayout(layout)

    def update(self, telemetry: Telemetry) -> None:
        self.mission_time.setText(f"<b>Time:</b> UTC {telemetry.mission_time}")
        self.packet_count.setText(
            f"<b>Packet Count:</b> {telemetry.packet_count}"
        )
        self.mode.setText(f"<b>Mode:</b> {telemetry.mode}")
        self.state.setText(f"<b>State:</b> {telemetry.state}")
        self.altitude.setText(f"<b>Altitude:</b> {telemetry.altitude}m")
        self.temperature.setText(
            f"<b>Temperature:</b> {telemetry.temperature}°C"
        )
        self.pressure.setText(f"<b>Pressure:</b> {telemetry.pressure}kPa")
        self.voltage.setText(f"<b>Voltage:</b> {telemetry.voltage}V")
        self.gyro.setText(f"<b>Gyro:</b> {telemetry.gyro}°s<sup>-2</sup>")
        self.acceleration.setText(
            f"<b>Acc.:</b> \
                {telemetry.acceleration}ms<sup>-2</sup>"
        )
        self.magnetometer.setText(
            f"<b>Mag.:</b> {telemetry.magnetometer}G"
        )
        self.auto_gryro_rotation_rate.setText(
            f"<b>Gyro Rot. Rate:</B> \
                {telemetry.auto_gyro_rotation_rate}°s<sup>-2</sup>"
        )
        self.gps.setText(
            f"<b>GPS:</b> \
                {telemetry.gps}"
        )
        self.cmd_echo.setText(f"<b>Command Echo:</b> {telemetry.cmd_echo}")
