from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QSizePolicy,
    QFrame,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt, QSize
from package.models.telemetry import Telemetry
from .graph import Graph
from .telemetry_display import TelemetryDisplay
from package.constants import TelemetryFields, TelemetryUnits
import pyqtgraph as pg


class GraphView(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.setMaximumSize(QSize(int(1440 * 0.7), int(900 * 0.8)))

        self._setup_layout()

    def _setup_layout(self) -> None:
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.graph_layout = self._create_graph_grid()
        layout.addWidget(self.graph_layout)

        frame = self.__create_telemetry_display()
        layout.addWidget(frame, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)

    def __create_telemetry_display(self) -> QFrame:
        frame = QFrame()
        frame.setSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding
        )
        frame.setContentsMargins(0, 0, 0, 0)

        frame_layout = QHBoxLayout()
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(5)

        self.telemetry_display = TelemetryDisplay()
        frame_layout.addWidget(self.telemetry_display)
        frame.setLayout(frame_layout)

        return frame

    def _create_graph_grid(self) -> pg.GraphicsLayoutWidget:
        graph_layout = pg.GraphicsLayoutWidget()

        self.altitude = Graph(
            f"{TelemetryFields.ALTITUDE.value}/{TelemetryUnits.ALTITUDE.value}",
            [TelemetryFields.ALTITUDE.value],
        )
        self.temperature = Graph(
            f"{TelemetryFields.TEMPERATURE.value}/{TelemetryUnits.TEMPERATURE.value}",
            [TelemetryFields.TEMPERATURE.value],
        )
        self.pressure = Graph(
            f"{TelemetryFields.PRESSURE.value}/{TelemetryUnits.PRESSURE.value}",
            [TelemetryFields.PRESSURE.value],
        )
        self.voltage = Graph(
            f"{TelemetryFields.VOLTAGE.value}/{TelemetryUnits.VOLTAGE.value}",
            [TelemetryFields.VOLTAGE.value],
        )
        self.gyro = Graph(
            f"{TelemetryFields.GYRO.value}/{TelemetryUnits.GYRO.value}",
            ["Roll", "Pitch", "Yaw"],
        )
        self.acceleration = Graph(
            f"{TelemetryFields.ACCELERATION.value}/{TelemetryUnits.ACCELERATION.value}",
            ["Roll", "Pitch", "Yaw"],
        )
        self.magnetometer = Graph(
            f"{TelemetryFields.MAGNETOMETER.value}/{TelemetryUnits.MAGNETOMETER.value}",
            ["Roll", "Pitch", "Yaw"],
        )
        self.gyro_rot_rate = Graph(
            f"{TelemetryFields.GYRO_ROTATION_RATE.value}/{TelemetryUnits.GYRO_ROTATION_RATE.value}",
            [TelemetryFields.GYRO_ROTATION_RATE.value],
        )

        graphs = [
            [self.altitude, self.temperature, self.pressure, self.voltage],
            [
                self.gyro,
                self.acceleration,
                self.magnetometer,
                self.gyro_rot_rate,
            ],
        ]

        for row_idx, row in enumerate(graphs):
            for col_idx, graph in enumerate(row):
                graph_layout.addItem(graph, row_idx, col_idx)

        return graph_layout

    def update(self, telemetry: Telemetry) -> None:
        self.telemetry_display.update(telemetry)

        self.altitude.update([telemetry.altitude])
        self.temperature.update([telemetry.temperature])
        self.pressure.update([telemetry.pressure])
        self.voltage.update([telemetry.voltage])
        self.gyro.update(
            [telemetry.gyro.roll, telemetry.gyro.pitch, telemetry.gyro.yaw]
        )
        self.acceleration.update(
            [
                telemetry.acceleration.roll,
                telemetry.acceleration.pitch,
                telemetry.acceleration.yaw,
            ]
        )
        self.magnetometer.update(
            [
                telemetry.magnetometer.roll,
                telemetry.magnetometer.pitch,
                telemetry.magnetometer.yaw,
            ]
        )
        self.gyro_rot_rate.update([telemetry.auto_gyro_rotation_rate])
