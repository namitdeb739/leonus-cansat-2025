import logging
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, QRect
from package.communications.communication import Communication
from package.config import DevMode
from package.constants import GEOMETRY
from package.models.app_info import AppInfo
from package.models.telemetry import Telemetry
from package.ui.header import Header
from package.ui.body import Body
from package.ui.log.log import Log


class MainWindow(QMainWindow):

    def __init__(
        self,
        app_info: AppInfo,
        communication: Communication,
        geometry: tuple[int, int, int, int],
    ) -> None:
        super().__init__()
        self.app_info = app_info
        self.communication = communication

        self.__setup_window(geometry)
        self.__setup_layout()

    def update(self, telemetry: Telemetry) -> None:
        self.header.update(telemetry.header())
        self.body.update(telemetry)

    def __setup_window(self, geometry: tuple[int, int, int, int]) -> None:
        self.setWindowTitle(
            f"{self.app_info.team_name()} {self.app_info.title}"
        )
        try:
            self.setGeometry(QRect(*geometry))
        except TypeError:
            logging.error("Invalid geometry provided. Using default geometry.")
            self.setGeometry(QRect(*GEOMETRY[DevMode.LAPTOP.value]))

    def __setup_layout(self) -> None:
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(0)

        central_widget.setLayout(layout)

        self.header = Header(self.app_info, self.communication)
        self.body = Body(self.communication)

        layout.addWidget(self.header, alignment=Qt.AlignmentFlag.AlignVCenter)
        # layout.addSpacerItem(
        #     self.__create_spacer(10, QSizePolicy.Policy.Expanding)
        # )
        layout.addWidget(self.body, alignment=Qt.AlignmentFlag.AlignVCenter)
        # layout.addSpacerItem(
        #     self.__create_spacer(20, QSizePolicy.Policy.Expanding)
        # )
        layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMaximumSize)

        self.setCentralWidget(central_widget)

    # def __create_spacer(
    #     self, height: int, policy: QSizePolicy.Policy
    # ) -> QSpacerItem:
    #     return QSpacerItem(0, height, policy, QSizePolicy.Policy.Fixed)

    def logger(self) -> Log:
        return self.body.log_display()

    def update_device_connection_status(self, status: bool) -> None:
        self.header.update_device_connection_status(status)

    def update_remote_device_connection_status(self, status: bool) -> None:
        self.header.update_remote_device_connection_status(status)

    def is_simulation_mode(self) -> bool:
        return self.body.is_simulation_mode()

    def update_time(self) -> None:
        self.header.update_time()

    def activate_command_control(self) -> None:
        self.body.activate_command_control()

    def deactivate_command_control(self) -> None:
        self.body.deactivate_command_control()
