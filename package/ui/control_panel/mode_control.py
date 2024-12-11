from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QSizePolicy,
    QHBoxLayout,
    QSpacerItem,
)
from PyQt6.QtCore import Qt
from package.ui.control_panel.control_section import ControlSection


class ModeControl(ControlSection):
    def __init__(self):
        super().__init__()
        self.setObjectName("ModeControl")

        self.activate_flight_mode = QPushButton("Activate Flight Mode")
        ControlSection.build_button(
            self.activate_flight_mode,
            self.press_activate_flight_mode,
            set_checked=True,
        )
        self.activate_flight_mode.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding
        )

        self.enable_simulation_mode = QPushButton("Enable Simulation Mode")
        ControlSection.build_button(
            self.enable_simulation_mode,
            self.press_enable_simulation_mode,
        )

        self.activate_simulation_mode = QPushButton("Activate Simulation Mode")
        ControlSection.build_button(
            self.activate_simulation_mode,
            self.press_activate_simulation_mode,
            lock=True,
        )

        simulation = QWidget()
        simulation.setLayout(simulation_layout := QVBoxLayout())
        simulation_layout.setContentsMargins(0, 0, 0, 0)
        simulation_layout.addWidget(
            self.enable_simulation_mode, alignment=Qt.AlignmentFlag.AlignTop
        )
        simulation_layout.addSpacerItem(QSpacerItem(0, 10))
        simulation_layout.addWidget(
            self.activate_simulation_mode,
            alignment=Qt.AlignmentFlag.AlignBottom,
        )

        widgets = [self.activate_flight_mode, simulation]

        self.build_layout("Mode", widgets)

    def build_layout(self, title: str, widgets: list[QWidget]) -> None:
        layout = QVBoxLayout()
        layout.addWidget(title_label := QLabel(title))

        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        layout.addWidget(buttons := QWidget())
        buttons.setLayout(buttons_layout := QHBoxLayout())
        buttons.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        buttons_layout.setContentsMargins(0, 0, 0, 0)

        for widget in widgets:
            buttons_layout.addWidget(widget)

        self.setLayout(layout)

    def press_activate_flight_mode(self) -> None:
        self.activate_flight_mode.setChecked(True)
        self.enable_simulation_mode.setChecked(False)
        self.activate_simulation_mode.setChecked(False)
        self.activate_simulation_mode.setEnabled(False)

    def press_enable_simulation_mode(self) -> None:
        if self.enable_simulation_mode.isChecked():
            self.enable_simulation_mode.setChecked(True)
            self.activate_simulation_mode.setEnabled(True)
        else:
            self.enable_simulation_mode.setChecked(False)
            self.activate_simulation_mode.setEnabled(False)
            self.activate_simulation_mode.setChecked(False)
            self.activate_flight_mode.setChecked(True)

    def press_activate_simulation_mode(self) -> None:
        if self.activate_simulation_mode.isChecked():
            self.activate_simulation_mode.setChecked(True)
            self.activate_flight_mode.setChecked(False)
        else:
            self.activate_simulation_mode.setChecked(False)
            self.activate_flight_mode.setChecked(True)
