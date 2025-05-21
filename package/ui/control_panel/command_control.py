import os
from typing import Any
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QSizePolicy,
    QGridLayout,
    QFileDialog,
)
from PyQt6.QtCore import Qt, QTimer
from pyparsing import C
from package.communications.communication import Communication
from package.exceptions.SenderNotInitialisedException import (
    SenderNotInitialisedException,
)
from package.models.telemetry import OnOff, TimeSource
from package.ui.control_panel.control_section import ControlSection
from package.constants import Colours, Mechanism
from PyQt6.QtWidgets import QComboBox


class CommandControl(ControlSection):
    SELECT_FILE_STYLESHEET = f"background-color: {Colours.LIGHT_GREY.value}; color: {Colours.BLACK.value}"
    SELECTED_FILE_STYLESHEET = f"background-color: {Colours.LIGHT_GREY.value}; color: {Colours.BLACK.value}; font-size: 10pt; font-weight: normal;"
    MECHANISM_COMBOBOX_STYLESHEET = (
        f"background-color: {Colours.LIGHT_GREY.value}; "
        f"color: {Colours.BLACK.value}; "
        "selection-background-color: #b0c4de; "
        "border: 1px solid #aaa; "
        "padding: 2px 6px;"
        "border-radius: 4px;"
        "font-weight: bold;"
    )
    CLASS = "class"
    FLASH_BUTTON = "flash-button"
    CHECK_BUTTON = "check-button"

    def __init__(self, communication: Communication):
        super().__init__()
        self.communication = communication
        self.file_contents = None

        self.__initialize_buttons()
        self.__setup_layout()

    def __initialize_buttons(self) -> None:
        self.__initialise_store_buttons()
        self.__initialise_set_time_buttons()
        self.__initialise_payload_telemetry_buttons()
        self.__initialise_simulated_pressure_buttons()
        self.__initialise_calibration_and_reset_buttons()
        self.__initialise_mechanism_actuation_buttons()

    def __initialise_mechanism_actuation_buttons(self) -> None:
        self.mechanism_selection = QComboBox()
        self.mechanism_selection.addItems(
            [mechanism.value for mechanism in Mechanism]
        )
        self.mechanism_selection.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding
        )
        self.mechanism_selection.setStyleSheet(
            CommandControl.MECHANISM_COMBOBOX_STYLESHEET
        )
        self.mechanism_actuation_on = self.__create_button(
            "On",
            self.__press_mechanism_actuation_on,
        )
        self.mechanism_actuation_off = self.__create_button(
            "Off",
            self.__press_mechanism_actuation_off,
        )

    def __initialise_calibration_and_reset_buttons(self) -> None:
        self.calibrate_altitude = self.__create_button(
            "Set Alt. To Zero",
            self.__press_calibrate_altitude,
        )

        self.reset_eeprom = self.__create_button(
            "Reset EEPROM",
            lambda: self.__press_reset_eeprom(),
        )

    def __initialise_simulated_pressure_buttons(self) -> None:
        self.send_simulated_pressure = self.__create_button(
            "Send Pressure",
            self.__press_send_simulated_pressure,
        )
        self.select_simulated_pressure_file = self.__create_button(
            "Select File",
            self.__press_select_simulated_pressure_file,
        )
        self.select_simulated_pressure_file.setStyleSheet(
            CommandControl.SELECT_FILE_STYLESHEET
        )

    def __initialise_payload_telemetry_buttons(self) -> None:
        self.payload_telemetry_on = self.__create_button(
            "On",
            self.__press_payload_telemetry_on,
        )
        self.payload_telemetry_off = self.__create_button(
            "Off",
            self.__press_payload_telemetry_off,
        )
        CommandControl.__check_button(self.payload_telemetry_off)

    def __initialise_set_time_buttons(self) -> None:
        self.set_gcs_time = self.__create_button(
            "GCS Time",
            self.__press_set_gcs_time,
        )
        self.set_gps_time = self.__create_button(
            "GPS Time",
            self.__press_set_gps_time,
        )

    def __initialise_store_buttons(self) -> None:
        self.enable_store = self.__create_button(
            "Enable Store",
            self.__press_enable_store,
        )
        self.disable_store = self.__create_button(
            "Disable Store",
            self.__press_disable_store,
        )
        CommandControl.__check_button(self.enable_store)

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
            "Calibrate/Reset": [self.calibrate_altitude, self.reset_eeprom],
            self.mechanism_selection: [
                self.mechanism_actuation_on,
                self.mechanism_actuation_off,
            ],
        }

        layout = QGridLayout()
        layout.setSpacing(10)
        layout.setVerticalSpacing(15)

        self.__setup_button_grid(command_controls, layout)

        # layout.setColumnStretch(0, 0)
        # for col in range(1, layout.columnCount()):
        #     layout.setColumnStretch(col, 1)

        self.setLayout(layout)

    def __setup_button_grid(
        self,
        command_controls: dict[Any, list[QPushButton]],
        layout: QGridLayout,
    ) -> None:
        for row, (title, buttons) in enumerate(command_controls.items()):
            layout.addWidget(
                (
                    title
                    if title == self.mechanism_selection
                    else QLabel(title)
                ),
                row,
                0,
                Qt.AlignmentFlag.AlignLeft,
            )
            self.__populate_button_row(layout, row, buttons)

    def __populate_button_row(
        self, layout: QGridLayout, row: int, buttons: list[QPushButton]
    ) -> None:
        for column, button in enumerate(buttons):
            layout.addWidget(
                button, row, column + 1, Qt.AlignmentFlag.AlignVCenter
            )

    def __create_button(
        self,
        text: str,
        callback: callable,
    ) -> QPushButton:
        button = QPushButton(text)
        ControlSection.build_button(
            button,
            callback,
        )
        button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding
        )
        return button

    @staticmethod
    def __check_button(button: QPushButton) -> None:
        button.setProperty(CommandControl.CLASS, CommandControl.CHECK_BUTTON)
        button.style().unpolish(button)
        button.style().polish(button)

    @staticmethod
    def __uncheck_button(button: QPushButton) -> None:
        button.setProperty(CommandControl.CLASS, "")
        button.style().unpolish(button)
        button.style().polish(button)

    @staticmethod
    def __flash_button(
        button: QPushButton, selecting_file: bool = False
    ) -> None:
        if selecting_file:
            button.setStyleSheet("")
        button.setProperty(CommandControl.CLASS, CommandControl.FLASH_BUTTON)
        button.style().unpolish(button)
        button.style().polish(button)

        QTimer.singleShot(
            500,
            lambda: CommandControl.__remove_flash(button, selecting_file),
        )

    @staticmethod
    def __remove_flash(
        button: QPushButton, selecting_file: bool = False
    ) -> None:
        if selecting_file:
            button.setStyleSheet(CommandControl.SELECT_FILE_STYLESHEET)
        button.setProperty(CommandControl.CLASS, "")
        button.style().unpolish(button)
        button.style().polish(button)

    def __press_enable_store(self) -> None:
        CommandControl.__check_button(self.enable_store)
        CommandControl.__uncheck_button(self.disable_store)

        self.communication.enable_store()

    def __press_disable_store(self) -> None:
        CommandControl.__uncheck_button(self.enable_store)
        CommandControl.__check_button(self.disable_store)

        self.communication.disable_store()

    def __press_payload_telemetry_on(self) -> None:
        try:
            self.communication.payload_telemetry(OnOff.ON)
            CommandControl.__check_button(self.payload_telemetry_on)
            CommandControl.__uncheck_button(self.payload_telemetry_off)
        except SenderNotInitialisedException:
            return

    def __press_payload_telemetry_off(self) -> None:
        try:
            self.communication.payload_telemetry(OnOff.OFF)
            CommandControl.__uncheck_button(self.payload_telemetry_on)
            CommandControl.__check_button(self.payload_telemetry_off)
        except SenderNotInitialisedException:
            return

    def __press_set_gcs_time(self) -> None:
        try:
            self.communication.set_time(TimeSource.GCS)
            CommandControl.__flash_button(self.set_gcs_time)
        except SenderNotInitialisedException:
            return

    def __press_set_gps_time(self) -> None:
        try:
            self.communication.set_time(TimeSource.GPS)
            CommandControl.__flash_button(self.set_gps_time)
        except SenderNotInitialisedException:
            return

    def __press_send_simulated_pressure(self) -> None:
        if not self.file_contents:
            return

        try:
            self.communication.parse_simulate_pressure_file(self.file_contents)
            CommandControl.__flash_button(self.send_simulated_pressure)
            self.select_simulated_pressure_file.setText("Select File")
        except SenderNotInitialisedException:
            return

    def __press_calibrate_altitude(self) -> None:
        try:
            self.communication.calibrate_altitude()
            CommandControl.__flash_button(self.calibrate_altitude)
        except SenderNotInitialisedException:
            return

    def __press_reset_eeprom(self) -> None:
        try:
            self.communication.reset_eeprom()
            CommandControl.__flash_button(self.reset_eeprom)
        except SenderNotInitialisedException:
            return

    def __press_mechanism_actuation_on(self) -> None:
        try:
            self.communication.mechanism_actuation(
                self.mechanism_selection.currentText(), OnOff.ON
            )
            CommandControl.__flash_button(self.mechanism_actuation_on)
        except SenderNotInitialisedException:
            return

    def __press_mechanism_actuation_off(self) -> None:
        try:
            self.communication.mechanism_actuation(
                self.mechanism_selection.currentText(), OnOff.OFF
            )
            CommandControl.__flash_button(self.mechanism_actuation_off)
        except SenderNotInitialisedException:
            return

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
