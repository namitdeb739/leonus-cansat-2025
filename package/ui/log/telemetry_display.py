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
            f"<b>Acceleration:</b> \
                {self.telemetry.acceleration}ms<sup>-2</sup>"
        )
        self.magnetometer = QLabel(
            f"<b>Magnetometer:</b> {self.telemetry.magnetometer}G"
        )
        self.auto_gryro_rotation_rate = QLabel(
            f"<b>Auto Gyro Rotation Rate:</B> \
                {self.telemetry.auto_gyro_rotation_rate}°s<sup>-2</sup>"
        )
        self.gps = QLabel(
            f"<b>GPS (Time, Co-Ord., Alt., Sat. No.):</B> \
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
                        QSizePolicy.Policy.Minimum,
                        QSizePolicy.Policy.Minimum,
                    )
                    continue
                layout.addWidget(
                    label, i, j, alignment=Qt.AlignmentFlag.AlignLeft
                )
                label.setSizePolicy(
                    QSizePolicy.Policy.Minimum,
                    QSizePolicy.Policy.Minimum,
                )

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setLayout(layout)
