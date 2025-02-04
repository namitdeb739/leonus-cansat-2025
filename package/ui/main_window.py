from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QRect
from package.communication import Communication
from package.models.app_info import AppInfo
from package.models.telemetry import Telemetry
from package.ui.header import Header
from enum import Enum
from package.ui.body import Body


class MainWindow(QMainWindow):
    class DevType(Enum):
        MONITOR = "monitor"
        LAPTOP = "laptop"

    def __init__(
        self, app_info: AppInfo, communication: Communication
    ) -> None:
        super().__init__()
        self.setObjectName("MainWindow")

        self.setWindowTitle(f"{app_info.team_info.team_name} {app_info.title}")

        central_widget, layout = QWidget(), QVBoxLayout()
        central_widget.setLayout(layout)
        self.header = Header(app_info)
        self.body = Body(communication)
        layout.addWidget(self.header, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.body, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMaximumSize)

        layout.setSpacing(0)

        self.setCentralWidget(central_widget)

    def setDevTypeGeometry(self, dev_type: str) -> None:
        dev_type = MainWindow.DevType(dev_type)
        if dev_type == MainWindow.DevType.MONITOR:
            geometry = QRect(1920, 0, 1440, 900)
        elif dev_type == MainWindow.DevType.LAPTOP:
            geometry = QRect(0, 0, 1440, 900)
        self.setGeometry(geometry)

    def update(self, telemetry: Telemetry) -> None:
        self.body.update(telemetry)
        self.header.update(telemetry.header())
