from enum import Enum
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFrame,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from .mode_control import ModeControl
from .command_control import CommandControl


class ControlPanel(QWidget):
    class LabelLocation(Enum):
        TOP = "TOP"
        LEFT = "LEFT"

    def __init__(self):
        super().__init__()
        self.setObjectName("ControlPanel")

        self.build_layout()

    def build_layout(self) -> None:
        self.setLayout(layout := QVBoxLayout())
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(
            frame := QFrame(), alignment=Qt.AlignmentFlag.AlignHCenter
        )
        frame.setLayout(frame_layout := QVBoxLayout())
        frame.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        frame_layout.addWidget(ModeControl())
        frame_layout.addWidget(CommandControl())
