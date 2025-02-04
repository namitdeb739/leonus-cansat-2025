from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QSizePolicy,
    QVBoxLayout,
)
from package.communication import Communication
from package.models.telemetry import (
    GPS,
    Command,
    PrincipalAxesCoordinate,
    Telemetry,
    Mode,
    State,
)
from .graph_view.graph_view import GraphView
from .control_panel.control_panel import ControlPanel
from .telemetry_display.log import Log


class Body(QWidget):

    def __init__(self, communication: Communication) -> None:
        super().__init__()
        self.setObjectName("Body")

        # TODO: Fix initialisation
        telemetry = Telemetry(
            1,
            "00:00:00",
            1,
            Mode.FLIGHT,
            State.LAUNCH_PAD,
            100.4,
            37.5,
            1003,
            3.7,
            PrincipalAxesCoordinate(1.0, 2.0, 3.0),
            PrincipalAxesCoordinate(1.0, 2.0, 3.0),
            PrincipalAxesCoordinate(1.0, 2.0, 3.0),
            1.0,
            GPS("00:00:00", 750, 100, 10, 10),
            Command.command(
                Command.CommandType.SIMULATION_MODE_CONTROL, "ENABLE"
            ),
        )

        self.build_layout(telemetry, communication)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

    def build_layout(
        self, telemetry: Telemetry, communication: Communication
    ) -> None:
        layout = QHBoxLayout()

        layout.addWidget(sidebar := QWidget())
        sidebar.setLayout(sidebar_layout := QVBoxLayout())
        sidebar.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Expanding,
        )

        self.control_panel = ControlPanel(communication)
        sidebar_layout.addWidget(self.control_panel)
        self.control_panel.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum,
        )

        self.log = Log(telemetry)
        sidebar_layout.addWidget(self.log)
        self.log.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Expanding,
        )

        self.graph_view = GraphView()
        layout.addWidget(self.graph_view)

        self.setLayout(layout)

    def update(self, telemetry: Telemetry) -> None:
        self.log.update(telemetry)
        self.graph_view.update(telemetry)
