import time
from xmlrpc.client import boolean
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QSizePolicy,
    QGridLayout,
    QLineEdit,
    QWidget,
    QVBoxLayout,
    QFileDialog,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QDoubleValidator
from package.communication import Communication
from package.models.telemetry import OnOff
from package.ui.control_panel.control_section import ControlSection


class CommandControl(ControlSection):
    SELECT_FILE_STYLESHEET = "background-color: #f0f0f0; color: #000000"

    def __init__(self, communication: Communication):
        super().__init__()
        self.setObjectName("CommandControl")

        self.communication = communication
        self.file_contents = None

        self.enable_store = QPushButton("Enable Store")
        ControlSection.build_button(self.enable_store, self.press_enable_store)
        self.disable_store = QPushButton("Disable Store")
        ControlSection.build_button(
            self.disable_store, self.press_disable_store, set_checked=True
        )

        self.set_gcs_time = QPushButton("GCS Time")
        ControlSection.build_button(
            self.set_gcs_time, self.press_set_gcs_time, set_checkable=False
        )
        self.set_gps_time = QPushButton("GPS Time")
        ControlSection.build_button(
            self.set_gps_time, self.press_set_gps_time, set_checkable=False
        )

        self.payload_telemetry_on = QPushButton("On")
        ControlSection.build_button(
            self.payload_telemetry_on,
            self.press_payload_telemetry_on,
            set_checked=True,
        )

        self.payload_telemetry_off = QPushButton("Off")
        ControlSection.build_button(
            self.payload_telemetry_off, self.press_payload_telemetry_off
        )

        self.send_simulated_pressure = QPushButton("Send Pressure")
        ControlSection.build_button(
            self.send_simulated_pressure,
            self.press_send_smulated_pressure,
            set_checkable=False,
        )

        self.select_simulated_pressure_file = QPushButton("Select File")
        ControlSection.build_button(
            self.select_simulated_pressure_file,
            self.press_select_simulated_pressure_file,
            set_checkable=False,
        )
        self.select_simulated_pressure_file.setStyleSheet(
            CommandControl.SELECT_FILE_STYLESHEET
        )

        self.simulated_pressure_input = QLineEdit()
        self.simulated_pressure_input.setPlaceholderText("Pressure")
        self.simulated_pressure_input.setValidator(
            QDoubleValidator(0.0, 100000.0, 1, self.simulated_pressure_input)
        )

        self.pressure_inputs = QWidget()
        self.pressure_inputs.setLayout(pressure_input_layout := QVBoxLayout())
        pressure_input_layout.addWidget(self.simulated_pressure_input)
        pressure_input_layout.addWidget(self.select_simulated_pressure_file)

        self.calibrate_altitude = QPushButton("Set To Zero")
        self.calibrate_altitude.setObjectName("CalibrateAltitude")
        ControlSection.build_button(
            self.calibrate_altitude,
            self.press_calibrate_altitude,
            set_checkable=False,
        )

        self.mechanism_actuation_on = QPushButton("On")
        ControlSection.build_button(
            self.mechanism_actuation_on,
            self.press_mechanism_actuation_on,
        )

        self.mechanism_actuation_off = QPushButton("Off")
        ControlSection.build_button(
            self.mechanism_actuation_off,
            self.press_mechanism_actuation_off,
            set_checked=True,
        )

        command_controls = {
            "Store": [self.enable_store, self.disable_store],
            "Set Time": [self.set_gcs_time, self.set_gps_time],
            "Payload Telemetry": [
                self.payload_telemetry_on,
                self.payload_telemetry_off,
            ],
            "Simulated Pressure": [
                self.pressure_inputs,
                self.send_simulated_pressure,
            ],
            "Calibrate Altitude": [self.calibrate_altitude],
            "Mechanism Actuation": [
                self.mechanism_actuation_on,
                self.mechanism_actuation_off,
            ],
        }

        self.build_layout(command_controls)

    def build_layout(
        self, command_controls: dict[str, list[QPushButton]]
    ) -> None:
        layout = QGridLayout()
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
                        2,
                        Qt.AlignmentFlag.AlignCenter,
                    )
                    continue

                layout.addWidget(
                    button, row, column + 1, Qt.AlignmentFlag.AlignCenter
                )
                # button.setSizePolicy(
                #     QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum
                # )

        layout.setColumnStretch(0, 0)
        for col in range(1, layout.columnCount()):
            layout.setColumnStretch(col, 1)

        self.setLayout(layout)

    @staticmethod
    def flash_button(
        button: QPushButton, selecting_file: boolean = False
    ) -> None:
        if selecting_file:
            button.setStyleSheet("")
        button.setProperty("class", "flash-button")
        button.style().unpolish(button)
        button.style().polish(button)

        QTimer.singleShot(
            500,
            lambda: CommandControl.remove_flash_class(button, selecting_file),
        )

    @staticmethod
    def remove_flash_class(
        button: QPushButton, selecting_file: boolean = False
    ) -> None:
        if selecting_file:
            button.setStyleSheet(CommandControl.SELECT_FILE_STYLESHEET)
        button.setProperty("class", "")
        button.style().unpolish(button)
        button.style().polish(button)

    def press_enable_store(self) -> None:
        self.enable_store.setChecked(True)
        self.disable_store.setChecked(False)
        self.communication.store_enabled = True

    def press_disable_store(self) -> None:
        self.enable_store.setChecked(False)
        self.disable_store.setChecked(True)
        self.communication.store_enabled = False

    def press_payload_telemetry_on(self) -> None:
        self.payload_telemetry_on.setChecked(True)
        self.payload_telemetry_off.setChecked(False)
        self.communication.payload_telemetry(OnOff.ON)

    def press_payload_telemetry_off(self) -> None:
        self.payload_telemetry_on.setChecked(False)
        self.payload_telemetry_off.setChecked(True)
        self.communication.payload_telemetry(OnOff.OFF)

    def press_set_gcs_time(self) -> None:
        CommandControl.flash_button(self.set_gcs_time)
        self.communication.set_time(
            time.strftime("%H:%M:%S", time.localtime())
        )

    def press_set_gps_time(self) -> None:
        CommandControl.flash_button(self.set_gps_time)
        self.communication.set_time("GPS")

    def press_send_smulated_pressure(self) -> None:
        if self.file_contents:
            # print(f"Simulated Pressure File: {self.file_contents}")
            CommandControl.flash_button(self.send_simulated_pressure)
            self.communication.simulate_pressure_file(self.file_contents)
            self.select_simulated_pressure_file.setText("Select File")
        else:
            pressure = self.simulated_pressure_input.text()
            # print(f"Simulated Pressure: {pressure}")
            CommandControl.flash_button(self.send_simulated_pressure)
            self.communication.simulate_pressure(pressure)
            self.simulated_pressure_input.clear()

    def press_calibrate_altitude(self) -> None:
        # print("Calibrate Altitude")
        CommandControl.flash_button(self.calibrate_altitude)
        self.communication.calibrate_altitude()

    def press_mechanism_actuation_on(self) -> None:
        self.mechanism_actuation_on.setChecked(True)
        self.mechanism_actuation_off.setChecked(False)
        self.communication.mechanism_actuation(OnOff.ON)

    def press_mechanism_actuation_off(self) -> None:
        self.mechanism_actuation_on.setChecked(False)
        self.mechanism_actuation_off.setChecked(True)
        self.communication.mechanism_actuation(OnOff.OFF)

    def press_select_simulated_pressure_file(self) -> None:
        CommandControl.flash_button(self.select_simulated_pressure_file, True)

        options = QFileDialog.Option.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Simulated Pressure File",
            "",
            "Text Files (*.txt);;All Files (*)",
            options=options,
        )
        if file_name:
            try:
                with open(file_name, "r") as file:
                    self.file_contents = file.read()
                    self.select_simulated_pressure_file.setText(file_name)
            except Exception as e:
                print(f"Failed to read file {file_name}: {e}")
