from math import log
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QScrollArea,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from datetime import datetime
from PyQt6.QtGui import QGuiApplication

from package import constants


class Log(QWidget):
    HEIGHT_RATIO = 0.40

    def __init__(self):
        super().__init__()
        self.most_recent_log = None
        self.__initialize_ui()

    def __initialize_ui(self) -> None:
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding
        )
        self.setMaximumHeight(
            int(
                QGuiApplication.primaryScreen().geometry().height()
                * Log.HEIGHT_RATIO
            )
        )
        self.scroll_area.verticalScrollBar().setFixedWidth(10)
        # self.scroll_area.verticalScrollBar().setStyleSheet(
        #     Log.SCROLL_AREA_SCROLLBAR_STYLE
        # )

        self.container = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(5)

        self.container.setLayout(self.main_layout)
        self.scroll_area.setWidget(self.container)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        title = QLabel("Log")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        main_layout.addWidget(title)

        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

    def __format_label(self, timestamp: str, message: str) -> QLabel:
        label = QLabel(f"<b>{timestamp}:</b> {message}")
        label.setWordWrap(True)
        return label, f"{timestamp}: {message}"

    def log(self, message: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_label, log_message = self.__format_label(timestamp, message)

        if self.most_recent_log and self.most_recent_log == log_message:
            self.most_recent_log = log_message
            return

        self.most_recent_log = log_message
        self.main_layout.addWidget(log_label)
        self.container.adjustSize()
        self.__adjust_scroll_bar()
        print(log_message)

    def __adjust_scroll_bar(self):
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )
        self.scroll_area.horizontalScrollBar().setVisible(False)
