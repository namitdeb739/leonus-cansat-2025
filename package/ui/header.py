from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QWidget,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QPushButton,
    QDialog,
    QVBoxLayout,
    QListWidget,
    QDialogButtonBox,
)
from package.models.app_info import AppInfo
from package.communications.communication import Communication
from datetime import datetime


class Header(QWidget):
    def __init__(
        self, app_info: AppInfo, communication: Communication
    ) -> None:
        super().__init__()
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        self.setMaximumHeight(50)

        self.communication = communication

        self.team_id_label = QLabel()
        self.team_name_label = QLabel(
            f"{app_info.team_name()} {app_info.title}"
        )
        self.packet_label = QLabel()
        self.time_label = QLabel(datetime.now().strftime("%H:%M:%S"))
        self.device_connection_status_button = QPushButton("GCS")
        self.device_connection_status_button.setCheckable(True)
        self.device_connection_status_button.setChecked(False)
        self.device_connection_status_button.clicked.connect(
            self.__show_usb_selector
        )

        self.remote_device_connection = QPushButton("OBC")
        self.remote_device_connection.setCheckable(True)
        self.remote_device_connection.setChecked(False)
        self.remote_device_connection.setDisabled(True)
        self.remote_device_connection.clicked.connect(
            lambda: self.communication.connect_remote_device()
        )

        self.packet_count = -1

        self.__setup_layout(app_info)

    def __setup_layout(self, app_info: AppInfo) -> None:
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(
            self.team_id_label, alignment=Qt.AlignmentFlag.AlignLeft
        )
        layout.addSpacerItem(
            self.__create_spacer(10, QSizePolicy.Policy.Minimum)
        )
        layout.addWidget(
            self.team_name_label, alignment=Qt.AlignmentFlag.AlignLeft
        )
        layout.addSpacerItem(
            self.__create_spacer(
                layout.maximumSize().width(), QSizePolicy.Policy.Maximum
            )
        )
        layout.addWidget(
            self.packet_label, alignment=Qt.AlignmentFlag.AlignRight
        )
        layout.addSpacerItem(
            self.__create_spacer(10, QSizePolicy.Policy.Minimum)
        )
        layout.addWidget(
            self.time_label, alignment=Qt.AlignmentFlag.AlignRight
        )
        layout.addSpacerItem(
            self.__create_spacer(10, QSizePolicy.Policy.Minimum)
        )
        layout.addWidget(
            self.device_connection_status_button,
            alignment=Qt.AlignmentFlag.AlignRight,
        )
        layout.addSpacerItem(
            self.__create_spacer(10, QSizePolicy.Policy.Minimum)
        )
        layout.addWidget(
            self.remote_device_connection,
            alignment=Qt.AlignmentFlag.AlignRight,
        )

        self.setLayout(layout)

        self.__update_team_id(app_info.team_info.team_id)
        self.__update_packet()
        self.update_device_connection_status(False)

    def update(self, header: tuple[int, str, int]) -> None:
        team_id, _, packet = header
        self.__update_team_id(team_id)
        self.__update_packet()

    def __update_team_id(self, team_id: int) -> None:
        self.team_id_label.setText(f"Team ID: {team_id}")

    def update_time(self) -> None:
        self.time_label.setText(datetime.now().strftime("%H:%M:%S"))

    def __update_packet(self) -> None:
        self.packet_count = self.packet_count + 1
        self.packet_label.setText(f"# of Packets Recieved: {self.packet_count}")

    def update_device_connection_status(self, status: bool) -> None:
        self.device_connection_status_button.setChecked(status)

        if status:
            self.remote_device_connection.setDisabled(False)
        else:
            self.remote_device_connection.setDisabled(True)
            self.remote_device_connection.setChecked(False)

    def update_remote_device_connection_status(self, status: bool) -> None:
        self.remote_device_connection.setChecked(status)

    def __show_usb_selector(self) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle("Select USB Driver")
        dialog.setModal(True)

        layout = QVBoxLayout(dialog)
        usb_list = QListWidget()
        usb_ports = Communication.find_ports()
        usb_list.addItems(usb_ports)

        layout.addWidget(usb_list)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(
            lambda: self.__select_usb_driver(dialog, usb_list)
        )
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.exec()

    def __select_usb_driver(
        self, dialog: QDialog, usb_list: QListWidget
    ) -> None:
        selected_item = usb_list.currentItem()
        if selected_item:
            selected_port = selected_item.text()
            self.communication.initialise_connection(selected_port)
        dialog.accept()

    @staticmethod
    def __create_spacer(
        width: int, horizontal_size_policy: QSizePolicy.Policy
    ) -> QSpacerItem:
        return QSpacerItem(
            width, 20, horizontal_size_policy, QSizePolicy.Policy.Minimum
        )
