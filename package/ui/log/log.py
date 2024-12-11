from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFrame,
    QSizePolicy,
)
from PyQt6.QtCore import Qt

from package.models.telemetry import Telemetry
from .telemetry_display import TelemetryDisplay


class Log(QWidget):
    def __init__(self, telemetry: Telemetry):
        super().__init__()
        self.setObjectName("Log")

        self.build_layout(telemetry)

    def build_layout(self, telemetry: Telemetry) -> None:
        layout = QVBoxLayout()

        layout.addWidget(
            frame := QFrame(), alignment=Qt.AlignmentFlag.AlignHCenter
        )
        frame.setLayout(frame_layout := QVBoxLayout())
        frame.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        frame.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)

        frame_layout.addWidget(
            title := QLabel("Telemetry"),
            alignment=Qt.AlignmentFlag.AlignHCenter,
        )

        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding
        )

        frame_layout.addWidget(TelemetryDisplay(telemetry))

        self.setLayout(layout)
