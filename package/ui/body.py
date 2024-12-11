from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QVBoxLayout

from package.models.telemetry import (
    GPS,
    Command,
    PricipalAxesCoordinate,
    Telemetry,
    Mode,
    State,
)
from .graph_view.graph_view import GraphView
from .control_panel.control_panel import ControlPanel
from .log.log import Log


class Body(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("Body")

        telemetry = Telemetry(
            "00:00:00",
            1,
            Mode.FLIGHT,
            State.LAUNCH_PAD,
            100.4,
            37.5,
            1003,
            3.7,
            PricipalAxesCoordinate(1.0, 2.0, 3.0),
            PricipalAxesCoordinate(1.0, 2.0, 3.0),
            PricipalAxesCoordinate(1.0, 2.0, 3.0),
            1.0,
            GPS("00:00:00", 750, 100, 10, 10),
            Command.command(
                Command.CommandType.SIMULATION_MODE_CONTROL, "ENABLE"
            ),
        )

        self.build_layout(telemetry)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

    def build_layout(self, telemetry: Telemetry) -> None:
        layout = QHBoxLayout()

        layout.addLayout(sidebar := QVBoxLayout())

        sidebar.addWidget(control_panel := ControlPanel())
        control_panel.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum,
        )
        sidebar.addWidget(log := Log(telemetry))
        log.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        layout.addWidget(GraphView())

        self.setLayout(layout)
