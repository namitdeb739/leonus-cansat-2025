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
    WIDTH_RATIO = 0.65

    def __init__(self):
        super().__init__()
        self.telemetry = None
        self.labels: dict[str, tuple[QLabel, QLabel]] = {}
        self.__initialize_ui()

    def __initialize_ui(self) -> None:
        self.setMinimumWidth(
            int(
                QGuiApplication.primaryScreen().geometry().width()
                * TelemetryDisplay.WIDTH_RATIO
            )
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
            },
            {
                TelemetryFields.GPS_SATELLITE_NUMBER: (
                    str(self.telemetry.gps.sats) if self.telemetry else ""
                ),
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
            2 * max(len(field_set) for field_set in self.telemetry_fields)
        ):
            adjustment = -200 if i % 2 == 0 or i == 3 else 200
            base_width = self.minimumWidth() // 8
            grid.setColumnMinimumWidth(
                i, base_width + (adjustment if i != 3 else -50)
            )

        row = 0
        for field_set in self.telemetry_fields:
            col = 0
            for field, value in field_set.items():
                field_label = QLabel(self.__bold_label(field))
                field_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
                field_label.setSizePolicy(
                    QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
                )
                grid.addWidget(
                    field_label, row, col, alignment=Qt.AlignmentFlag.AlignLeft
                )

                col += 1

                value_label = QLabel(value)
                value_label.setAlignment(Qt.AlignmentFlag.AlignRight)
                value_label.setSizePolicy(
                    QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum
                )
                grid.addWidget(
                    value_label,
                    row,
                    col,
                    alignment=Qt.AlignmentFlag.AlignRight,
                )
                # if field==TelemetryFields.ACCELERATION:
                value_label.setWordWrap(True)

                self.labels[field] = (field_label, value_label)
                col += 1

            row += 1

        container.setLayout(grid)

        return container

    def __bold_label(self, field: TelemetryFields) -> str:
        return (
            f"<b>{field.value}:</b>"
            if not TelemetryFields.is_principal_axes(field)
            else "".join(
                [
                    f"<b>{line}:</b><br>"
                    for line in TelemetryFields.principal_axes_str(
                        field
                    ).split("\n")
                ]
            )[: -len("<br>")]
        )

    def __update_label(
        self,
        field: TelemetryFields,
        value: str | tuple[str, str, str],
        unit: str,
    ) -> None:
        _, value_label = self.labels[
            (
                TelemetryFields(field.split()[0])
                if isinstance(field, str)
                else field
            )
        ]
        if isinstance(value, tuple):
            roll, pitch, yaw = value
            value_label.setText(
                f"{roll}{unit}\n{pitch}{unit}\n{yaw}{unit}"
                if (roll and pitch and yaw)
                else ""
            )
        elif isinstance(value, str):
            value_label.setText(f"{value}{unit}" if value else "")

    def update(self, telemetry: Telemetry) -> None:
        self.telemetry = telemetry

        self.__update_label(
            TelemetryFields.TIME,
            f"UTC {telemetry.mission_time}",
            "",
        )
        self.__update_label(
            TelemetryFields.PACKET_COUNT,
            str(telemetry.packet_count),
            "",
        )
        self.__update_label(
            TelemetryFields.MODE,
            telemetry.display_mode(),
            "",
        )
        self.__update_label(
            TelemetryFields.STATE,
            telemetry.display_state(),
            "",
        )
        self.__update_label(
            TelemetryFields.ALTITUDE,
            f"{telemetry.display_number(telemetry.altitude)}",
            TelemetryUnits.ALTITUDE.value,
        )
        self.__update_label(
            TelemetryFields.TEMPERATURE,
            f"{telemetry.display_number(telemetry.temperature)}",
            TelemetryUnits.TEMPERATURE.value,
        )
        self.__update_label(
            TelemetryFields.PRESSURE,
            f"{telemetry.display_number(telemetry.pressure)}",
            TelemetryUnits.PRESSURE.value,
        )
        self.__update_label(
            TelemetryFields.VOLTAGE,
            f"{telemetry.display_number(telemetry.voltage)}",
            TelemetryUnits.VOLTAGE.value,
        )
        self.__update_label(
            TelemetryFields.principal_axes_str(TelemetryFields.GYRO),
            telemetry.display_principal_axes_coordinate(telemetry.gyro),
            TelemetryUnits.GYRO.value,
        )
        self.__update_label(
            TelemetryFields.GYRO_ROTATION_RATE,
            f"{telemetry.display_number(telemetry.auto_gyro_rotation_rate)}",
            TelemetryUnits.GYRO_ROTATION_RATE.value,
        )
        self.__update_label(
            TelemetryFields.ACCELERATION,
            telemetry.display_principal_axes_coordinate(
                telemetry.acceleration
            ),
            TelemetryUnits.ACCELERATION.value,
        )
        self.__update_label(
            TelemetryFields.MAGNETOMETER,
            telemetry.display_principal_axes_coordinate(
                telemetry.magnetometer
            ),
            TelemetryUnits.MAGNETOMETER.value,
        )
        self.__update_label(
            TelemetryFields.GPS_TIME,
            f"UTC {telemetry.gps.time}",
            "",
        )
        self.__update_label(
            TelemetryFields.GPS_LATITUDE,
            f"{telemetry.display_number(telemetry.gps_latitude())}",
            TelemetryUnits.GPS_LATITUDE.value,
        )
        self.__update_label(
            TelemetryFields.GPS_LONGITUDE,
            f"{telemetry.display_number(telemetry.gps_longitude())}",
            TelemetryUnits.GPS_LONGITUDE.value,
        )
        self.__update_label(
            TelemetryFields.GPS_ALTITUDE,
            f"{telemetry.display_number(telemetry.gps_altitude())}",
            TelemetryUnits.GPS_ALTITUDE.value,
        )
        self.__update_label(
            TelemetryFields.GPS_SATELLITE_NUMBER,
            telemetry.display_number(telemetry.gps_sats()),
            "",
        )
        self.__update_label(
            TelemetryFields.COMMAND_ECHO,
            str(telemetry.cmd_echo),
            "",
        )
        self.__update_label(
            TelemetryFields.DESCENT_RATE,
            f"{telemetry.display_number(telemetry.descent_rate)}",
            TelemetryUnits.DESCENT_RATE.value,
        )
        self.__update_label(
            TelemetryFields.GEOGRAPHIC_HEADING,
            f"{telemetry.display_number(telemetry.geographic_heading)}",
            TelemetryUnits.GEOGRAPHIC_HEADING.value,
        )
