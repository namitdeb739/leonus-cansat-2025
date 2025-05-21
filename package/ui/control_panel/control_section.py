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
        lock: bool = False,
    ) -> None:
        button.setCheckable(False)
        button.clicked.connect(activation_function)
        button.setEnabled(not lock)
