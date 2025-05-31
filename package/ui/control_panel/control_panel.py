from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFrame,
    QSizePolicy,
)
from PyQt6.QtCore import Qt

from package.communications.communication import Communication
from .mode_control import ModeControl
from .command_control import CommandControl


class ControlPanel(QWidget):
    def __init__(self, communication: Communication) -> None:
        super().__init__()
        # self.n = "hello"
        self.mode_control = None
        self.command_control = None

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.__setup_layout(communication)
        self.__set_control_cross_reference()

    def __setup_layout(self, communication: Communication) -> None:
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(10)

        frame = self.__create_frame(communication)
        layout.addWidget(frame, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)

    def __create_frame(self, communication: Communication) -> QFrame:
        frame = QFrame()
        frame.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(0, 10, 0, 10)
        frame_layout.setSpacing(10)

        self.mode_control = ModeControl(communication)
        frame_layout.addWidget(self.mode_control)

        self.command_control = CommandControl(communication)
        frame_layout.addWidget(self.command_control)

        frame.setLayout(frame_layout)
        return frame

    def is_simulation_mode(self) -> bool:
        return self.mode_control.is_simulation_mode()

    def activate(self) -> None:
        self.command_control.activate_all_buttons()
        self.mode_control.activate_all_buttons()

    def deactivate(self) -> None:
        self.command_control.deactivate_all_buttons()
        self.mode_control.deactivate_all_buttons()

    def __set_control_cross_reference(self) -> None:
        self.mode_control.set_command_control(self.command_control)
        self.command_control.set_mode_control(self.mode_control)
