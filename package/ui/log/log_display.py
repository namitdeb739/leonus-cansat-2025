from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from .log import Log


class LogDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.__initialize_ui()

    def __initialize_ui(self) -> None:
        self.__setup_layout()

    def __setup_layout(self) -> None:
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        self.setSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed
        )

        frame = self.__create_frame()
        layout.addWidget(frame, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)

    def __create_frame(self) -> QFrame:
        frame = QFrame()
        frame.setSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding
        )
        frame.setContentsMargins(0, 0, 0, 0)

        frame_layout = QHBoxLayout()
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(5)

        self.log = Log()

        frame_layout.addWidget(self.log)

        frame.setLayout(frame_layout)
        return frame
