from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtCore import QSize

from package.models.telemetry import Telemetry
from .graph import Graph
import pyqtgraph as pg


class GraphView(pg.GraphicsView):

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("GraphView")

        layout = self.build_layout()
        self.setCentralItem(layout)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self.setMaximumSize(QSize(int(1440 * 0.7), int(900 * 0.8)))
        self.showMaximized()

    def build_layout(self) -> pg.GraphicsLayout:
        layout = pg.GraphicsLayout()

        self.altitude = Graph("Altitude / m", ["Altitude"])
        self.temperature = Graph("Temperature / °C", ["Temperature"])
        self.pressure = Graph("Pressure / kPa", ["Pressure"])
        self.voltage = Graph("Voltage / V", ["Voltage"])
        self.gyro = Graph("Gyro / °s<sup>-2</sup>", ["Roll", "Pitch", "Yaw"])
        self.acceleration = Graph(
            "Acceleration / °s<sup>-2</sup>", ["Roll", "Pitch", "Yaw"]
        )
        self.magnetometer = Graph("Magnetometer / G", ["Roll", "Pitch", "Yaw"])
        self.gyro_rot_rate = Graph(
            "Gyro Rot. Rate / °s<sup>-1</sup>",
            ["Gyro Rot. Rate"],
        )

        self.graph_layout = [
            [self.altitude, self.temperature, self.pressure, self.voltage],
            [
                self.gyro,
                self.acceleration,
                self.magnetometer,
                self.gyro_rot_rate,
            ],
        ]

        for i, row in enumerate(self.graph_layout):
            for j, graph in enumerate(row):
                layout.addItem(graph, i, j)

        return layout

    def update(self, telemetry: Telemetry) -> None:
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
