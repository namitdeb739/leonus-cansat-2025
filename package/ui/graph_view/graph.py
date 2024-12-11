from typing import Iterable
import numpy as np
import random
import pyqtgraph as pg
from package.config import Colours
from PyQt6.QtCore import QTimer


class Graph(pg.PlotItem):
    LINE_COLOUR_ORDER = [Colours.RED, Colours.GREEN, Colours.NUS_BLUE]

    def __init__(self, title: str, line_names: Iterable[str]) -> None:
        super().__init__(
            name=title,
            title=f"<h4><b>{title}</b></h4>",
            viewBox=pg.ViewBox(border=Colours.RICH_BLACK.value),
        )

        self.setSizePolicy(
            pg.QtWidgets.QSizePolicy.Policy.Expanding,
            pg.QtWidgets.QSizePolicy.Policy.Expanding,
        )

        self.pointer = 0
        self.getViewBox().setXRange(self.pointer, self.pointer + 20)

        self.num_lines = len(line_names)
        self.line_names = line_names
        self.graph_plots: list[pg.PlotDataItem] = []
        self.graph_data: list[int] = []
        self.graph_value_labels: list[pg.TextItem] = []
        for i, line_name in enumerate(line_names):
            self.init_line(line_name, i)

        # TODO: Use telemetry data instead
        timer = QTimer(self)
        timer.timeout.connect(self.update_rand)
        timer.start(1000)
        self.update_rand()

    def update(self, value: int) -> None:
        self.pointer += 1
        self.getViewBox().setXRange(self.pointer, self.pointer + 20)
        self.getViewBox().setYRange(0, self.graph_data[-1][-20:].max() * 1.25)

        for i in range(self.num_lines):
            self.graph_data[i] = np.append(
                self.graph_data[i],
                float(value),
            )
            self.graph_plots[i].setData(self.graph_data[i])

            self.graph_value_labels[i].setText(
                f"{self.line_names[i]}: {value}"
            )

    def update_rand(self) -> None:
        self.pointer += 1
        self.getViewBox().setXRange(self.pointer, self.pointer + 20)
        self.getViewBox().setYRange(0, self.graph_data[-1][-20:].max() * 1.25)

        for i in range(self.num_lines):
            self.graph_data[i] = np.append(
                self.graph_data[i],
                value := float(random.randint(0, 10)),
            )
            self.graph_plots[i].setData(self.graph_data[i])

            self.graph_value_labels[i].setText(
                f"{self.line_names[i]}: {value}"
            )

    def init_line(self, line_name: str, i: int) -> None:
        colour = (
            Graph.LINE_COLOUR_ORDER[i]
            if self.num_lines > 1
            else Colours.NUS_BLUE
        )
        self.graph_plots.append(
            plot := self.plot(
                pen=pg.mkPen(colour.value, width=3), name=line_name
            )
        )
        self.graph_data.append(data := np.random.randint(0, 10, 20))
        plot.setData(data)

        self.graph_value_labels.append(
            graph_value_label := pg.LabelItem(
                f"{line_name}: {data[-1]}", color=colour.value, size="12pt"
            )
        )
        graph_value_label.setParentItem(self.graphicsItem())
        graph_value_label.anchor(
            itemPos=(1, 0.1 + i * 0.15), parentPos=(1, 0.1 + i * 0.06)
        )
