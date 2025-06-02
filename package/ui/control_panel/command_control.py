import os
from typing import Any
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QSizePolicy,
    QGridLayout,
    QFileDialog,
)
from PyQt6.QtCore import Qt
from package.communications.communication import Communication
from package.exceptions.SenderNotInitialisedException import (
    SenderNotInitialisedException,
)
from package.models.telemetry import OnOff, TimeSource
from package.ui.control_panel.control_section import ControlSection
from package.constants import Mechanism
from PyQt6.QtWidgets import QComboBox


class CommandControl(ControlSection):
    SELECT_FILE_BUTTON = "select-file-button"
    SELECTED_FILE_BUTTON = "selected-file-button"
    MECHANISM_SELECTION = "mechanism-combobox"

    def __init__(self, communication: Communication):
        super().__init__()
        self.mode_control = None
        self.communication = communication
        self.file_contents = None

        self.__initialize_buttons()
        self.__setup_layout()

    def __initialize_buttons(self) -> None:
        self.__initialise_start_and_reset_button()
        self.__initialise_store_buttons()
        self.__initialise_set_time_buttons()
        self.__initialise_payload_telemetry_buttons()
        self.__initialise_simulated_pressure_buttons()
        self.__initialise_calibration_buttons()
        self.__initialise_mechanism_actuation_buttons()

        self.activatable_buttons = [
            self.start_button,
            # self.calibrate_imu,
            self.payload_telemetry_on,
            self.payload_telemetry_off,
            self.set_gcs_time,
            self.set_gps_time,
            # self.send_simulated_pressure,
            self.calibrate_altitude,
            self.mechanism_actuation_on,
            self.mechanism_actuation_off,
            self.reset_eeprom,
        ]

    def __initialise_start_and_reset_button(self) -> None:
        self.start_button = self.__create_button(
            "Start",
            self.__press_start,
        )
        self.reset_eeprom = self.__create_button(
            "Reset EEPROM",
            self.__press_reset_eeprom,
        )

        ControlSection.deactivate_button(self.start_button)
        ControlSection.deactivate_button(
            self.reset_eeprom,
        )

    def __initialise_mechanism_actuation_buttons(self) -> None:
        self.mechanism_selection = QComboBox()
        self.mechanism_selection.addItems(
            [mechanism.value for mechanism in Mechanism]
        )
        self.mechanism_selection.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding
        )
        self.mechanism_selection.setProperty(
            CommandControl.CLASS,
            CommandControl.MECHANISM_SELECTION,
        )
        self.mechanism_selection.currentTextChanged.connect(
            self.__on_mechanism_selection_changed
        )

        self.mechanism_states: dict[str, OnOff] = {}
        for i in range(self.mechanism_selection.count()):
            self.mechanism_states[self.mechanism_selection.itemText(i)] = (
                OnOff.OFF
            )

        self.mechanism_actuation_on = self.__create_button(
            "On",
            self.__press_mechanism_actuation_on,
        )
        self.mechanism_actuation_off = self.__create_button(
            "Off",
            self.__press_mechanism_actuation_off,
        )
        ControlSection.deactivate_button(
            self.mechanism_actuation_on,
        )
        ControlSection.deactivate_button(
            self.mechanism_actuation_off,
        )
        ControlSection.check_button(
            self.mechanism_actuation_off,
        )

    def __initialise_calibration_buttons(self) -> None:
        self.calibrate_altitude = self.__create_button(
            "Set Alt. To Zero",
            self.__press_calibrate_altitude,
        )
        # self.calibrate_imu = self.__create_button(
        #     "Calibrate IMU",
        #     self.__calibrate_imu,
        # )
        ControlSection.deactivate_button(
            self.calibrate_altitude,
        )
        # ControlSection.deactivate_button(
        #     self.calibrate_imu,
        # )

    def __initialise_simulated_pressure_buttons(self) -> None:
        self.send_simulated_pressure = self.__create_button(
            "Send Pressure",
            self.__press_send_simulated_pressure,
        )
        self.select_simulated_pressure_file = self.__create_button(
            "Select File",
            self.__press_select_simulated_pressure_file,
        )
        self.select_simulated_pressure_file.setProperty(
            CommandControl.CLASS, CommandControl.SELECT_FILE_BUTTON
        )
        ControlSection.deactivate_button(
            self.send_simulated_pressure,
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
        ControlSection.check_button(self.payload_telemetry_off)
        ControlSection.deactivate_button(
            self.payload_telemetry_on,
        )
        ControlSection.deactivate_button(
            self.payload_telemetry_off,
        )

    def __initialise_set_time_buttons(self) -> None:
        self.set_gcs_time = self.__create_button(
            "GCS Time",
            self.__press_set_gcs_time,
        )
        self.set_gps_time = self.__create_button(
            "GPS Time",
            self.__press_set_gps_time,
        )
        ControlSection.deactivate_button(
            self.set_gcs_time,
        )
        ControlSection.deactivate_button(
            self.set_gps_time,
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
        ControlSection.check_button(self.enable_store)

    def __setup_layout(self) -> None:
        command_controls = {
            "Start/Reset": [self.start_button, self.reset_eeprom],
            "Payload Telemetry": [
                self.payload_telemetry_on,
                self.payload_telemetry_off,
            ],
            "Set Time": [self.set_gcs_time, self.set_gps_time],
            "Simulated Pressure": [
                self.select_simulated_pressure_file,
                self.send_simulated_pressure,
            ],
            "Calibrate": [self.calibrate_altitude],
            self.mechanism_selection: [
                self.mechanism_actuation_on,
                self.mechanism_actuation_off,
            ],
            "Store": [self.enable_store, self.disable_store],
        }

        layout = QGridLayout()
        layout.setSpacing(10)
        layout.setVerticalSpacing(15)

        self.__setup_button_grid(command_controls, layout)

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
            self.__populate_button_row(
                layout,
                row,
                buttons,
                max([len(b) for b in command_controls.values()]),
            )

    def __populate_button_row(
        self,
        layout: QGridLayout,
        row: int,
        buttons: list[QPushButton],
        columnCount: int,
    ) -> None:
        for column, button in enumerate(buttons):
            layout.addWidget(
                button,
                row,
                column + 1,
                1,
                1 if len(buttons) > 1 else columnCount,
                Qt.AlignmentFlag.AlignCenter,
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

    def activate_all_buttons(self) -> None:
        for button in self.activatable_buttons:
            if (
                ControlSection.is_button_checked(self.payload_telemetry_on)
                or self.mode_control.is_simulation_mode()
            ) and button == self.reset_eeprom:
                continue

            ControlSection.activate_button(button)

    def deactivate_all_buttons(self) -> None:
        for button in self.activatable_buttons:
            ControlSection.deactivate_button(button)

    def __press_enable_store(self) -> None:
        ControlSection.check_button(self.enable_store)
        ControlSection.uncheck_button(self.disable_store)

        self.communication.enable_store()

    def __press_disable_store(self) -> None:
        ControlSection.uncheck_button(self.enable_store)
        ControlSection.check_button(self.disable_store)

        self.communication.disable_store()

    def __press_payload_telemetry_on(self) -> None:
        try:
            self.communication.payload_telemetry(OnOff.ON)
            ControlSection.check_button(self.payload_telemetry_on)
            ControlSection.uncheck_button(self.payload_telemetry_off)
            ControlSection.deactivate_button(self.reset_eeprom)
        except SenderNotInitialisedException:
            return

    def __press_payload_telemetry_off(self) -> None:
        try:
            self.communication.payload_telemetry(OnOff.OFF)
            ControlSection.uncheck_button(self.payload_telemetry_on)
            ControlSection.check_button(self.payload_telemetry_off)
            ControlSection.activate_button(self.reset_eeprom)
        except SenderNotInitialisedException:
            return

    def __press_set_gcs_time(self) -> None:
        try:
            self.communication.set_time(TimeSource.GCS)
            ControlSection.flash_button(self.set_gcs_time)
        except SenderNotInitialisedException:
            return

    def __press_set_gps_time(self) -> None:
        try:
            self.communication.set_time(TimeSource.GPS)
            ControlSection.flash_button(self.set_gps_time)
        except SenderNotInitialisedException:
            return

    def __press_send_simulated_pressure(self) -> None:
        if not self.file_contents:
            return

        try:
            self.communication.parse_simulate_pressure_file(self.file_contents)
            ControlSection.flash_button(self.send_simulated_pressure)
            self.select_simulated_pressure_file.setText("Select File")
            ControlSection.change_property(
                self.select_simulated_pressure_file,
                CommandControl.CLASS,
                CommandControl.SELECT_FILE_BUTTON,
            )
        except SenderNotInitialisedException:
            return

    def __press_calibrate_altitude(self) -> None:
        try:
            self.communication.calibrate_altitude()
            ControlSection.flash_button(self.calibrate_altitude)
        except SenderNotInitialisedException:
            return

    def __press_reset_eeprom(self) -> None:
        if ControlSection.is_button_checked(self.payload_telemetry_on):
            self.communication.logger.log(
                "Cannot reset EEPROM while telemetry is on."
            )
            return

        try:
            self.communication.reset_eeprom()
            ControlSection.flash_button(self.reset_eeprom)
        except SenderNotInitialisedException:
            return

    def __on_mechanism_selection_changed(self, mechanism: str) -> None:
        if mechanism not in self.mechanism_states:
            return

        if self.mechanism_states[mechanism] == OnOff.ON:
            ControlSection.activate_button(self.mechanism_actuation_off)
            ControlSection.deactivate_button(self.mechanism_actuation_on)
        else:
            ControlSection.activate_button(self.mechanism_actuation_on)
            ControlSection.deactivate_button(self.mechanism_actuation_off)

    def __press_mechanism_actuation_on(self) -> None:
        try:
            self.communication.mechanism_actuation(
                self.mechanism_selection.currentText(), OnOff.ON
            )
            ControlSection.check_button(self.mechanism_actuation_on)
            ControlSection.uncheck_button(self.mechanism_actuation_off)
            self.mechanism_states[self.mechanism_selection.currentText()] = (
                OnOff.ON
            )
        except SenderNotInitialisedException:
            return

    def __press_mechanism_actuation_off(self) -> None:
        try:
            self.communication.mechanism_actuation(
                self.mechanism_selection.currentText(), OnOff.OFF
            )
            ControlSection.check_button(self.mechanism_actuation_off)
            ControlSection.uncheck_button(self.mechanism_actuation_on)
            self.mechanism_states[self.mechanism_selection.currentText()] = (
                OnOff.OFF
            )
        except SenderNotInitialisedException:
            return

    def __press_select_simulated_pressure_file(self) -> None:
        ControlSection.flash_button(self.select_simulated_pressure_file, True)

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
                ControlSection.change_property(
                    self.select_simulated_pressure_file,
                    CommandControl.CLASS,
                    CommandControl.SELECTED_FILE_BUTTON,
                )
        except Exception as e:
            print(f"Failed to read file {file_name}: {e}")

    def __press_start(self) -> None:
        try:
            self.communication.start()
            ControlSection.flash_button(self.start_button)
        except SenderNotInitialisedException:
            return

    def set_mode_control(self, mode_control: ControlSection) -> None:
        self.mode_control = mode_control

    def activate_simulated_pressure(self) -> None:
        ControlSection.activate_button(self.send_simulated_pressure)

    def deactivate_simulated_pressure(self) -> None:
        ControlSection.deactivate_button(self.send_simulated_pressure)

    def activate_reset(self):
        ControlSection.activate_button(self.reset_eeprom)

    def deactivate_reset(self):
        ControlSection.deactivate_button(self.reset_eeprom)

    # def __calibrate_imu(self) -> None:
    #     try:
    #         self.communication.calibrate_imu()
    #         ControlSection.flash_button(self.calibrate_imu)
    #     except SenderNotInitialisedException:
    #         return
