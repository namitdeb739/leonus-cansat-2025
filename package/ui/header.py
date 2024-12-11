from PyQt6.QtCore import Qt, QTimer, QTime
from PyQt6.QtWidgets import QLabel, QWidget, QHBoxLayout
from PyQt6.QtWidgets import QSpacerItem, QSizePolicy

from package.models.app_info import AppInfo


class Header(QWidget):

    def __init__(self, app_info: AppInfo) -> None:
        super().__init__()
        self.setObjectName("Header")

        layout = self.build_layout(app_info)
        self.setLayout(layout)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        # TODO: Use telemetry timer instead
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.timeout.connect(self.update_packet)
        timer.start(1000)
        self.update_time()
        self.update_packet()

    # TODO: Use telemetry timer instead
    def update_time(self) -> None:
        self.time.setText(QTime.currentTime().toString("hh:mm:ss"))

    # TODO: Replace with telemetry packet
    def update_packet(self) -> None:
        self.packet += 1
        self.packet_label.setText(f"Packet: {self.packet}")

    def build_layout(self, app_info: AppInfo) -> QHBoxLayout:
        layout = QHBoxLayout()

        Header.add_label_with_space(
            layout,
            f"Team ID: {app_info.team_info.team_id}",
            Qt.AlignmentFlag.AlignLeft,
            15,
            QSizePolicy.Policy.Minimum,
        )

        Header.add_label_with_space(
            layout,
            f"{app_info.team_info.team_name} {app_info.title}",
            Qt.AlignmentFlag.AlignLeft,
            layout.maximumSize().width(),
            QSizePolicy.Policy.Maximum,
        )

        # TODO: Use telemetry packet instead
        self.packet = 0
        self.packet_label = QLabel(f"Packet: {0}")
        layout.addWidget(
            self.packet_label, alignment=Qt.AlignmentFlag.AlignRight
        )
        layout.addSpacerItem(
            QSpacerItem(
                15,
                20,
                QSizePolicy.Policy.Minimum,
                QSizePolicy.Policy.Minimum,
            )
        )

        # TODO: Use telemetry timer instead
        self.time = QLabel(QTime.currentTime().toString("hh:mm:ss"))
        layout.addWidget(
            self.time,
            Qt.AlignmentFlag.AlignRight,
        )

        return layout

    @staticmethod
    def add_label_with_space(
        layout: QHBoxLayout,
        label: str,
        alignment: Qt.AlignmentFlag,
        space_width: int | None,
        space_policy: QSizePolicy.Policy | None,
    ) -> None:
        layout.addWidget(QLabel(label), alignment=alignment)
        layout.addSpacerItem(
            QSpacerItem(
                space_width,
                20,
                space_policy,
                QSizePolicy.Policy.Minimum,
            )
        )
