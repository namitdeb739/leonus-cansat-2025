from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from package.communications.communication import Communication
from package.communications.sender import Sender
from package.exceptions.SenderNotInitialisedException import SenderNotInitialisedException
from package.models.telemetry import SimulationMode
from package.ui.control_panel.control_section import ControlSection


class ModeControl(ControlSection):
    CLASS = "class"
    CHECK_BUTTON = "check-button"

    def __init__(self, communication: Communication) -> None:
        super().__init__()
        self.communication = communication

        self.activate_flight_mode = self.__create_button(
            "Activate Flight Mode",
            self.__press_activate_flight_mode,
            set_checked=True,
        )
        self.enable_simulation_mode = self.__create_button(
            "Enable Simulation Mode", self.__press_enable_simulation_mode
        )
        self.activate_simulation_mode = self.__create_button(
            "Activate Simulation Mode",
            self.__press_activate_simulation_mode,
            lock=True,
        )

        self.__setup_layout()

    def __setup_layout(self) -> None:
        simulation = QWidget()
        simulation.setLayout(simulation_layout := QVBoxLayout())
        simulation_layout.setContentsMargins(0, 0, 0, 0)
        simulation_layout.addWidget(
            self.enable_simulation_mode,
            alignment=Qt.AlignmentFlag.AlignVCenter,
        )
        simulation_layout.addSpacerItem(QSpacerItem(0, 10))
        simulation_layout.addWidget(
            self.activate_simulation_mode,
            alignment=Qt.AlignmentFlag.AlignVCenter,
        )

        widgets = [self.activate_flight_mode, simulation]
        self.__build_layout("Mode", widgets)

    def __build_layout(self, title: str, widgets: list[QWidget]) -> None:
        layout = QVBoxLayout()
        layout.addWidget(title_label := QLabel(title))

        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        layout.addWidget(buttons := QWidget())
        buttons.setLayout(buttons_layout := QHBoxLayout())
        buttons.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum
        )
        buttons_layout.setContentsMargins(0, 0, 0, 0)

        for widget in widgets:
            buttons_layout.addWidget(widget)

        self.setLayout(layout)

    def __create_button(
        self,
        text: str,
        callback: callable,
        set_checked: bool = False,
        lock: bool = False,
    ) -> QPushButton:
        button = QPushButton(text)
        ControlSection.build_button(
            button, callback, lock=lock
        )
        button.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding
        )
        if set_checked:
            self.__check_button(button)

        return button

    @staticmethod
    def __check_button(button: QPushButton) -> None:
        button.setProperty(ModeControl.CLASS, ModeControl.CHECK_BUTTON)
        button.style().unpolish(button)
        button.style().polish(button)

    @staticmethod
    def __uncheck_button(button: QPushButton) -> None:
        button.setProperty(ModeControl.CLASS, "")
        button.style().unpolish(button)
        button.style().polish(button)

    def __press_activate_flight_mode(self) -> None:
        try:
            self.communication.simulation_mode_control(SimulationMode.DISABLE)
            ModeControl.__check_button(self.activate_flight_mode)
            ModeControl.__uncheck_button(self.activate_simulation_mode)
            ModeControl.__uncheck_button(self.enable_simulation_mode)
            self.activate_simulation_mode.setEnabled(False)
        except SenderNotInitialisedException:
            return

    def __press_enable_simulation_mode(self) -> None:
        try:
            self.communication.simulation_mode_control(SimulationMode.ENABLE)
            ModeControl.__check_button(self.enable_simulation_mode)
            self.activate_simulation_mode.setEnabled(True)
        except SenderNotInitialisedException:
            return

    def __press_activate_simulation_mode(self) -> None:
        try:
            self.communication.simulation_mode_control(SimulationMode.ACTIVATE)
            ModeControl.__check_button(self.activate_simulation_mode)
            ModeControl.__uncheck_button(self.activate_flight_mode)
        except SenderNotInitialisedException:
            return

    def is_simulation_mode(self) -> bool:
        return (
            self.enable_simulation_mode.isChecked()
            and self.activate_simulation_mode.isChecked()
            and not self.activate_flight_mode.isChecked()
        )
