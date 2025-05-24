from re import S
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QSizePolicy,
    QVBoxLayout,
)
from package.communications.communication import Communication
from package.models.telemetry import (
    Telemetry,
)
from package.ui.log.log_display import LogDisplay
from package.ui.log.log import Log
from package.ui.telemetry.graph_view import GraphView
from .control_panel.control_panel import ControlPanel
from PyQt6.QtGui import QGuiApplication


class Body(QWidget):
    SIDEBAR_WIDTH_RATIO = 0.40
    HEIGHT_RATIO = 0.85

    def __init__(self, communication: Communication) -> None:
        super().__init__()
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.setMinimumHeight(
            int(
                QGuiApplication.primaryScreen().geometry().height()
                * Body.HEIGHT_RATIO
            )
        )

        self.control_panel = None
        self.log = None
        self.graph_view = None

        self.__setup_layout(communication)

    def __setup_layout(self, communication: Communication) -> None:
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        sidebar = self.__create_sidebar(communication)
        layout.addWidget(sidebar)
        sidebar.setMaximumWidth(
            int(
                QGuiApplication.primaryScreen().geometry().width()
                * Body.SIDEBAR_WIDTH_RATIO
            )
        )

        self.graph_view = GraphView()
        layout.addWidget(self.graph_view)

        self.setLayout(layout)

    def __create_sidebar(self, communication: Communication) -> QWidget:
        sidebar = QWidget()
        sidebar.setLayout(sidebar_layout := QVBoxLayout())
        sidebar.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding
        )

        self.control_panel = ControlPanel(communication)
        self.control_panel.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        sidebar_layout.addWidget(self.control_panel)

        self.log = LogDisplay()
        self.log.setSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding
        )
        sidebar_layout.addWidget(self.log)

        return sidebar

    def update(self, telemetry: Telemetry) -> None:
        self.log.update()
        self.graph_view.update(telemetry)

    def log_display(self) -> Log:
        return self.log.log

    def is_simulation_mode(self) -> bool:
        return self.control_panel.is_simulation_mode()

    def activate_command_control(self) -> None:
        self.control_panel.activate_command_control()

    def deactivate_command_control(self) -> None:
        self.control_panel.deactivate_command_control()
