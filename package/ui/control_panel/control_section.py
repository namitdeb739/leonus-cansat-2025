from PyQt6.QtWidgets import (
    QPushButton,
    QWidget,
)


class ControlSection(QWidget):

    def __init__(self):
        super().__init__()

    def build_button(
        button: QPushButton,
        activation_function: callable,
        set_checkable: bool = True,
        set_checked: bool = False,
        lock: bool = False,
    ) -> None:
        button.setCheckable(set_checkable)
        button.setChecked(set_checked)
        button.clicked.connect(activation_function)
        button.setEnabled(not lock)
