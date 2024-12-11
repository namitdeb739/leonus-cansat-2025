from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtCore import QSize
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

        graph_layout = [
            [
                ("Altitude / m", ["Altitude"]),
                ("Temperature / °C", ["Temperature"]),
                ("Pressure / kPa", ["Pressure"]),
                ("Voltage / V", ["Voltage"]),
            ],
            [
                ("Gyro / °s<sup>-2</sup>", ["Roll", "Pitch", "Yaw"]),
                ("Acceleration / °s<sup>-2</sup>", ["Roll", "Pitch", "Yaw"]),
                ("Magnetometer / G", ["Roll", "Pitch", "Yaw"]),
                (
                    "Gyro Rot. Rate / °s<sup>-1</sup>",
                    ["Gyro Rot. Rate"],
                ),
            ],
        ]

        for i, row in enumerate(graph_layout):
            for j, (graph, line_names) in enumerate(row):
                layout.addItem(Graph(graph, line_names), i, j)

        return layout
