import os
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QSizePolicy,
    QGridLayout,
    QFileDialog,
)
from PyQt6.QtCore import Qt, QTimer
from package.communications.communication import Communication
from package.models.telemetry import OnOff, TimeSource
from package.ui.control_panel.control_section import ControlSection
from package.constants import Colours


class CommandControl(ControlSection):
    SELECT_FILE_STYLESHEET = f"background-color: {Colours.LIGHT_GREY.value}; color: {Colours.BLACK.value}"
    SELECTED_FILE_STYLESHEET = f"background-color: {Colours.LIGHT_GREY.value}; color: {Colours.BLACK.value}; font-size: 10pt; font-weight: normal;"

    def __init__(self, communication: Communication):
        super().__init__()
        self.communication = communication
        self.file_contents = None

        self.__initialize_buttons()
        self.__setup_layout()

    def __initialize_buttons(self) -> None:
        self.enable_store = self.__create_button(
            "Enable Store", self.__press_enable_store, set_checked=True
        )
        self.disable_store = self.__create_button(
            "Disable Store", self.__press_disable_store
        )
        self.set_gcs_time = self.__create_button(
            "GCS Time", self.__press_set_gcs_time, set_checkable=False
        )
        self.set_gps_time = self.__create_button(
            "GPS Time", self.__press_set_gps_time, set_checkable=False
        )
        self.payload_telemetry_on = self.__create_button(
            "On", self.__press_payload_telemetry_on
        )
        self.payload_telemetry_off = self.__create_button(
            "Off", self.__press_payload_telemetry_off, set_checked=True
        )
        self.send_simulated_pressure = self.__create_button(
            "Send Pressure",
            self.__press_send_simulated_pressure,
            set_checkable=False,
        )
        self.select_simulated_pressure_file = self.__create_button(
            "Select File",
            self.__press_select_simulated_pressure_file,
            set_checkable=False,
        )
        self.select_simulated_pressure_file.setStyleSheet(
            CommandControl.SELECT_FILE_STYLESHEET
        )
        self.calibrate_altitude = self.__create_button(
            "Set To Zero", self.__press_calibrate_altitude, set_checkable=False
        )
        self.mechanism_actuation_on = self.__create_button(
            "On", self.__press_mechanism_actuation_on
        )
        self.mechanism_actuation_off = self.__create_button(
            "Off", self.__press_mechanism_actuation_off, set_checked=True
        )

    def __setup_layout(self) -> None:
        command_controls = {
            "Store": [self.enable_store, self.disable_store],
            "Payload Telemetry": [
                self.payload_telemetry_on,
                self.payload_telemetry_off,
            ],
            "Set Time": [self.set_gcs_time, self.set_gps_time],
            "Simulated Pressure": [
                self.select_simulated_pressure_file,
                self.send_simulated_pressure,
            ],
            "Calibrate Altitude": [self.calibrate_altitude],
            "Mech. Actuation": [
                self.mechanism_actuation_on,
                self.mechanism_actuation_off,
            ],
        }

        layout = QGridLayout()
        layout.setSpacing(10)
        layout.setVerticalSpacing(15)

        for row, (title, buttons) in enumerate(command_controls.items()):
            layout.addWidget(
                title_label := QLabel(title),
                row,
                0,
                Qt.AlignmentFlag.AlignLeft,
            )
            title_label.setSizePolicy(
                QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum
            )

            for column, button in enumerate(buttons):
                if button == self.calibrate_altitude:
                    layout.addWidget(
                        button,
                        row,
                        column + 1,
                        1,
                        layout.columnCount(),
                        Qt.AlignmentFlag.AlignVCenter
                        | Qt.AlignmentFlag.AlignHCenter,
                    )
                else:
                    layout.addWidget(
                        button, row, column + 1, Qt.AlignmentFlag.AlignVCenter
                    )

        layout.setColumnStretch(0, 0)
        for col in range(1, layout.columnCount()):
            layout.setColumnStretch(col, 1)

        self.setLayout(layout)

    def __create_button(
        self,
        text: str,
        callback: callable,
        set_checked: bool = False,
        set_checkable: bool = True,
    ) -> QPushButton:
        button = QPushButton(text)
        ControlSection.build_button(
            button,
            callback,
            set_checked=set_checked,
            set_checkable=set_checkable,
        )
        button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding
        )
        return button

    @staticmethod
    def __flash_button(
        button: QPushButton, selecting_file: bool = False
    ) -> None:
        if selecting_file:
            button.setStyleSheet("")
        button.setProperty("class", "flash-button")
        button.style().unpolish(button)
        button.style().polish(button)

        QTimer.singleShot(
            500,
            lambda: CommandControl.__remove_flash_class(
                button, selecting_file
            ),
        )

    @staticmethod
    def __remove_flash_class(
        button: QPushButton, selecting_file: bool = False
    ) -> None:
        if selecting_file:
            button.setStyleSheet(CommandControl.SELECT_FILE_STYLESHEET)
        button.setProperty("class", "")
        button.style().unpolish(button)
        button.style().polish(button)

    def __press_enable_store(self) -> None:
        self.enable_store.setChecked(True)
        self.disable_store.setChecked(False)

        self.communication.enable_store()

    def __press_disable_store(self) -> None:
        self.enable_store.setChecked(False)
        self.disable_store.setChecked(True)

        self.communication.disable_store()

    def __press_payload_telemetry_on(self) -> None:
        self.payload_telemetry_on.setChecked(True)
        self.payload_telemetry_off.setChecked(False)

        self.communication.payload_telemetry(OnOff.ON)

    def __press_payload_telemetry_off(self) -> None:
        self.payload_telemetry_on.setChecked(False)
        self.payload_telemetry_off.setChecked(True)
        self.communication.payload_telemetry(OnOff.OFF)

    def __press_set_gcs_time(self) -> None:
        CommandControl.__flash_button(self.set_gcs_time)
        self.communication.set_time(TimeSource.GCS)

    def __press_set_gps_time(self) -> None:
        CommandControl.__flash_button(self.set_gps_time)
        self.communication.set_time(TimeSource.GPS)

    def __press_send_simulated_pressure(self) -> None:
        if not self.file_contents:
            return

        CommandControl.__flash_button(self.send_simulated_pressure)
        self.communication.parse_simulate_pressure_file(self.file_contents)
        self.select_simulated_pressure_file.setText("Select File")

    def __press_calibrate_altitude(self) -> None:
        CommandControl.__flash_button(self.calibrate_altitude)
        self.communication.calibrate_altitude()

    def __press_mechanism_actuation_on(self) -> None:
        self.mechanism_actuation_on.setChecked(True)
        self.mechanism_actuation_off.setChecked(False)

        self.communication.mechanism_actuation(OnOff.ON)

    def __press_mechanism_actuation_off(self) -> None:
        self.mechanism_actuation_on.setChecked(False)
        self.mechanism_actuation_off.setChecked(True)

        self.communication.mechanism_actuation(OnOff.OFF)

    def __press_select_simulated_pressure_file(self) -> None:
        CommandControl.__flash_button(
            self.select_simulated_pressure_file, True
        )

        options = QFileDialog.Option.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Simulated Pressure File",
            "",
            "Text Files (*.txt);;All Files (*)",
            options=options,
        )

        if not file_name:
            return

        try:
            with open(file_name, "r") as file:
                self.file_contents = file.read()
                self.select_simulated_pressure_file.setText(
                    os.path.basename(file_name)
                )
                self.select_simulated_pressure_file.setStyleSheet(
                    CommandControl.SELECTED_FILE_STYLESHEET
                )
        except Exception as e:
            print(f"Failed to read file {file_name}: {e}")
