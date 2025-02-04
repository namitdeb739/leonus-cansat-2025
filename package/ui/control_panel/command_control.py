import time
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QSizePolicy,
    QGridLayout,
    QLineEdit,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIntValidator
from package.communication import Communication
from package.models.telemetry import OnOff
from package.ui.control_panel.control_section import ControlSection


class CommandControl(ControlSection):
    def __init__(self, communication: Communication):
        super().__init__()
        self.setObjectName("CommandControl")

        self.communication = communication

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

        self.simulated_pressure_input = QLineEdit()
        self.simulated_pressure_input.setPlaceholderText("Pressure")
        self.simulated_pressure_input.setValidator(
            QIntValidator(0, 100000, self.simulated_pressure_input)
        )

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
                self.simulated_pressure_input,
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

        layout.setColumnStretch(0, 0)
        for col in range(1, layout.columnCount()):
            layout.setColumnStretch(col, 1)

        self.setLayout(layout)

    @staticmethod
    def flash_button(button: QPushButton) -> None:
        button.setProperty("class", "flash-button")
        button.style().unpolish(button)
        button.style().polish(button)

        QTimer.singleShot(
            500, lambda: CommandControl.remove_flash_class(button)
        )

    @staticmethod
    def remove_flash_class(button: QPushButton) -> None:
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
        print("Set GCS Time")
        CommandControl.flash_button(self.set_gcs_time)
        self.communication.set_time(
            time.strftime("%H:%M:%S", time.localtime())
        )

    def press_set_gps_time(self) -> None:
        print("Set GPS Time")
        CommandControl.flash_button(self.set_gps_time)
        self.communication.set_time("GPS")

    def press_send_smulated_pressure(self) -> None:
        pressure = self.simulated_pressure_input.text()
        print(f"Simulated Pressure: {pressure}")
        CommandControl.flash_button(self.send_simulated_pressure)
        self.communication.simulate_pressure(pressure)
        self.simulated_pressure_input.clear()

    def press_calibrate_altitude(self) -> None:
        print("Calibrate Altitude")
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
