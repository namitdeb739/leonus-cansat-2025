from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QGridLayout,
    QVBoxLayout,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from package.models.telemetry import Telemetry
from PyQt6.QtGui import QGuiApplication
from package.constants import TelemetryFields, TelemetryUnits


class TelemetryDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.telemetry = None
        self.labels: dict[str, QLabel] = {}
        self.__initialize_ui()

    def __initialize_ui(self) -> None:
        self.setMinimumWidth(
            int(QGuiApplication.primaryScreen().geometry().width() * 0.49)
        )

        main_layout = QVBoxLayout()

        title = QLabel("Telemetry")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        main_layout.addWidget(title)

        telemetry_data = self.__create_telemetry_labels()
        main_layout.addWidget(telemetry_data)

        self.setLayout(main_layout)

    def __create_telemetry_labels(self) -> QWidget:
        container = QWidget()
        container.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        container.setContentsMargins(0, 0, 0, 0)

        self.telemetry_fields: list[dict[TelemetryFields, str]] = [
            {
                TelemetryFields.TIME: (
                    f"UTC {self.telemetry.mission_time}"
                    if self.telemetry
                    else ""
                ),
                TelemetryFields.PACKET_COUNT: (
                    str(self.telemetry.packet_count) if self.telemetry else ""
                ),
                TelemetryFields.MODE: (
                    str(self.telemetry.mode) if self.telemetry else ""
                ),
                TelemetryFields.STATE: (
                    str(self.telemetry.state) if self.telemetry else ""
                ),
            },
            {
                TelemetryFields.ALTITUDE: (
                    f"{self.telemetry.altitude}{TelemetryUnits.ALTITUDE.value}"
                    if self.telemetry
                    else ""
                ),
                TelemetryFields.TEMPERATURE: (
                    f"{self.telemetry.temperature}{TelemetryUnits.TEMPERATURE.value}"
                    if self.telemetry
                    else ""
                ),
                TelemetryFields.PRESSURE: (
                    f"{self.telemetry.pressure}{TelemetryUnits.PRESSURE.value}"
                    if self.telemetry
                    else ""
                ),
                TelemetryFields.VOLTAGE: (
                    f"{self.telemetry.voltage}{TelemetryUnits.VOLTAGE.value}"
                    if self.telemetry
                    else ""
                ),
            },
            {
                TelemetryFields.GYRO: (
                    f"{self.telemetry.gyro}{TelemetryUnits.GYRO.value}"
                    if self.telemetry
                    else ""
                ),
                TelemetryFields.GYRO_ROTATION_RATE: (
                    f"{self.telemetry.auto_gyro_rotation_rate}{TelemetryUnits.GYRO_ROTATION_RATE.value}"
                    if self.telemetry
                    else ""
                ),
                TelemetryFields.ACCELERATION: (
                    f"{self.telemetry.acceleration}{TelemetryUnits.ACCELERATION.value}"
                    if self.telemetry
                    else ""
                ),
                TelemetryFields.MAGNETOMETER: (
                    f"{self.telemetry.magnetometer}{TelemetryUnits.MAGNETOMETER.value}"
                    if self.telemetry
                    else ""
                ),
            },
            {
                TelemetryFields.GPS_TIME: (
                    f"UTC {self.telemetry.gps.time}" if self.telemetry else ""
                ),
                TelemetryFields.GPS_LATITUDE: (
                    f"{self.telemetry.gps.latitude}{TelemetryUnits.GPS_LATITUDE.value}"
                    if self.telemetry
                    else ""
                ),
                TelemetryFields.GPS_LONGITUDE: (
                    f"{self.telemetry.gps.longitude}{TelemetryUnits.GPS_LONGITUDE.value}"
                    if self.telemetry
                    else ""
                ),
                TelemetryFields.GPS_ALTITUDE: (
                    f"{self.telemetry.gps.altitude}{TelemetryUnits.GPS_ALTITUDE.value}"
                    if self.telemetry
                    else ""
                ),
                TelemetryFields.GPS_SATELLITE_NUMBER: (
                    str(self.telemetry.gps.sats) if self.telemetry else ""
                ),
            },
            {
                TelemetryFields.COMMAND_ECHO: (
                    str(self.telemetry.cmd_echo) if self.telemetry else ""
                ),
                TelemetryFields.DESCENT_RATE: (
                    f"{self.telemetry.descent_rate}{TelemetryUnits.DESCENT_RATE.value}"
                    if self.telemetry
                    else ""
                ),
                TelemetryFields.GEOGRAPHIC_HEADING: (
                    f"{self.telemetry.geographic_heading}{TelemetryUnits.GEOGRAPHIC_HEADING.value}"
                    if self.telemetry
                    else ""
                ),
            },
        ]

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(2)
        grid.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        for i in range(
            max(len(field_set) for field_set in self.telemetry_fields)
        ):
            grid.setColumnMinimumWidth(i, self.minimumWidth() // 5)

        row = 0
        for field_set in self.telemetry_fields:
            col = 0
            for field, value in field_set.items():
                label = QLabel(self.__format_label(field, value))
                label.setAlignment(Qt.AlignmentFlag.AlignLeft)
                label.setSizePolicy(
                    QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum
                )
                grid.addWidget(
                    label, row, col, alignment=Qt.AlignmentFlag.AlignLeft
                )

                self.labels[field] = label
                col += 1
            row += 1

        container.setLayout(grid)

        return container

    def __format_label(self, field: TelemetryFields, value: str) -> str:
        return f"<b>{field.value}:</b> {value}"

    def update(self, telemetry: Telemetry) -> None:
        self.telemetry = telemetry

        self.labels[TelemetryFields.TIME].setText(
            self.__format_label(
                TelemetryFields.TIME, f"UTC {telemetry.mission_time}"
            )
        )
        self.labels[TelemetryFields.PACKET_COUNT].setText(
            self.__format_label(
                TelemetryFields.PACKET_COUNT, str(telemetry.packet_count)
            )
        )
        self.labels[TelemetryFields.MODE].setText(
            self.__format_label(TelemetryFields.MODE, str(telemetry.mode))
        )
        self.labels[TelemetryFields.STATE].setText(
            self.__format_label(TelemetryFields.STATE, str(telemetry.state))
        )

        self.labels[TelemetryFields.ALTITUDE].setText(
            self.__format_label(
                TelemetryFields.ALTITUDE,
                f"{telemetry.altitude}{TelemetryUnits.ALTITUDE.value}",
            )
        )
        self.labels[TelemetryFields.TEMPERATURE].setText(
            self.__format_label(
                TelemetryFields.TEMPERATURE,
                f"{telemetry.temperature}{TelemetryUnits.TEMPERATURE.value}",
            )
        )
        self.labels[TelemetryFields.PRESSURE].setText(
            self.__format_label(
                TelemetryFields.PRESSURE,
                f"{telemetry.pressure}{TelemetryUnits.PRESSURE.value}",
            )
        )
        self.labels[TelemetryFields.VOLTAGE].setText(
            self.__format_label(
                TelemetryFields.VOLTAGE,
                f"{telemetry.voltage}{TelemetryUnits.VOLTAGE.value}",
            )
        )

        self.labels[TelemetryFields.GYRO].setText(
            self.__format_label(
                TelemetryFields.GYRO,
                f"{telemetry.gyro}{TelemetryUnits.GYRO.value}",
            )
        )
        self.labels[TelemetryFields.GYRO_ROTATION_RATE].setText(
            self.__format_label(
                TelemetryFields.GYRO_ROTATION_RATE,
                f"{telemetry.auto_gyro_rotation_rate}{TelemetryUnits.GYRO_ROTATION_RATE.value}",
            )
        )
        self.labels[TelemetryFields.ACCELERATION].setText(
            self.__format_label(
                TelemetryFields.ACCELERATION,
                f"{telemetry.acceleration}{TelemetryUnits.ACCELERATION.value}",
            )
        )
        self.labels[TelemetryFields.MAGNETOMETER].setText(
            self.__format_label(
                TelemetryFields.MAGNETOMETER,
                f"{telemetry.magnetometer}{TelemetryUnits.MAGNETOMETER.value}",
            )
        )

        self.labels[TelemetryFields.GPS_TIME].setText(
            self.__format_label(
                TelemetryFields.GPS_TIME, f"UTC {telemetry.gps.time}"
            )
        )
        self.labels[TelemetryFields.GPS_LATITUDE].setText(
            self.__format_label(
                TelemetryFields.GPS_LATITUDE,
                f"{telemetry.gps.latitude}{TelemetryUnits.GPS_LATITUDE.value}",
            )
        )
        self.labels[TelemetryFields.GPS_LONGITUDE].setText(
            self.__format_label(
                TelemetryFields.GPS_LONGITUDE,
                f"{telemetry.gps.longitude}{TelemetryUnits.GPS_LONGITUDE.value}",
            )
        )
        self.labels[TelemetryFields.GPS_ALTITUDE].setText(
            self.__format_label(
                TelemetryFields.GPS_ALTITUDE,
                f"{telemetry.gps.altitude}{TelemetryUnits.GPS_ALTITUDE.value}",
            )
        )
        self.labels[TelemetryFields.GPS_SATELLITE_NUMBER].setText(
            self.__format_label(
                TelemetryFields.GPS_SATELLITE_NUMBER,
                str(telemetry.gps.sats),
            )
        )

        self.labels[TelemetryFields.COMMAND_ECHO].setText(
            self.__format_label(
                TelemetryFields.COMMAND_ECHO, str(telemetry.cmd_echo)
            )
        )
        self.labels[TelemetryFields.DESCENT_RATE].setText(
            self.__format_label(
                TelemetryFields.DESCENT_RATE,
                f"{telemetry.descent_rate}{TelemetryUnits.DESCENT_RATE.value}",
            )
        )
        self.labels[TelemetryFields.GEOGRAPHIC_HEADING].setText(
            self.__format_label(
                TelemetryFields.GEOGRAPHIC_HEADING,
                f"{telemetry.geographic_heading}{TelemetryUnits.GEOGRAPHIC_HEADING.value}",
            )
        )
