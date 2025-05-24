from PyQt6.QtWidgets import (
    QPushButton,
    QWidget,
)
from PyQt6.QtCore import QTimer


class ControlSection(QWidget):
    CLASS = "class"
    FLASH_BUTTON = "flash-button"
    CHECK_BUTTON = "check-button"
    INACTIVE_BUTTON = "inactive-button"

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def build_button(
        button: QPushButton,
        activation_function: callable,
        lock: bool = False,
    ) -> None:
        button.setCheckable(False)
        button.clicked.connect(activation_function)
        button.setEnabled(not lock)

    @staticmethod
    def change_property(button: QPushButton, name: str, value: str) -> None:
        button.setProperty(name, value)
        button.style().unpolish(button)
        button.style().polish(button)

    @staticmethod
    def check_button(button: QPushButton) -> None:
        ControlSection.change_property(
            button,
            ControlSection.CLASS,
            ControlSection.CHECK_BUTTON,
        )

    @staticmethod
    def uncheck_button(button: QPushButton) -> None:
        ControlSection.change_property(
            button,
            ControlSection.CLASS,
            "",
        )

    @staticmethod
    def flash_button(
        button: QPushButton, selecting_file: bool = False
    ) -> None:
        ControlSection.change_property(
            button,
            ControlSection.CLASS,
            ControlSection.FLASH_BUTTON,
        )

        QTimer.singleShot(
            500,
            lambda: ControlSection.unflash_button(button, selecting_file),
        )

    @staticmethod
    def unflash_button(
        button: QPushButton, selecting_file: bool = False
    ) -> None:
        ControlSection.change_property(
            button,
            ControlSection.CLASS,
            "" if not selecting_file else ControlSection.FLASH_BUTTON,
        )

    @staticmethod
    def deactivate_button(button: QPushButton) -> None:
        current = button.property(ControlSection.CLASS) or ""
        classes = set(current.split())
        classes.add(ControlSection.INACTIVE_BUTTON)

        ControlSection.change_property(
            button,
            ControlSection.CLASS,
            " ".join(classes),
        )

    @staticmethod
    def activate_button(button: QPushButton) -> None:
        current = button.property(ControlSection.CLASS) or ""
        classes = set(current.split())
        classes.discard(ControlSection.INACTIVE_BUTTON)

        ControlSection.change_property(
            button,
            ControlSection.CLASS,
            " ".join(classes),
        )

    @staticmethod
    def is_button_checked(button: QPushButton) -> bool:
        return (
            button.property(ControlSection.CLASS)
            == ControlSection.CHECK_BUTTON
        )
