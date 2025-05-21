from math import nan
from typing import Iterable
import numpy as np
import pyqtgraph as pg
from package.constants import Colours


class Graph(pg.PlotItem):
    LINE_COLOUR_ORDER = [Colours.RED, Colours.GREEN, Colours.NUS_BLUE]
    TIME_VIEW = 120
    PEN_WIDTH = 3
    LABEL_FONT_SIZE = "12pt"
    LABEL_DEFAULT_TEXT = "NIL"
    X_RANGE_PADDING = 1.25
    Y_RANGE_PADDING = 1.25
    LABEL_VERTICAL_SPACING = -0.2
    LABEL_HORIZONTAL_SPACING = 0.06
    LABEL_VERTICAL_OFFSET = -0.5
    LABEL_HORIZONTAL_OFFSET = 0.1

    def __init__(self, title: str, line_names: Iterable[str]) -> None:
        super().__init__(
            name=title,
            title=self.__format_title(title),
            viewBox=pg.ViewBox(border=Colours.RICH_BLACK.value),
        )

        self.setSizePolicy(
            pg.QtWidgets.QSizePolicy.Policy.Expanding,
            pg.QtWidgets.QSizePolicy.Policy.Expanding,
        )

        self.pointer = 0
        self.num_lines = len(line_names)
        self.line_names = list(line_names)
        self.graph_plots = []
        self.graph_data = []
        self.graph_value_labels = []

        self.getViewBox().setXRange(
            self.pointer, self.pointer + Graph.TIME_VIEW
        )
        self.__initialize_lines()

    def __format_title(self, title: str) -> str:
        return f"<h5><b>{title}</b></h5>"

    def __initialize_lines(self) -> None:
        for i, line_name in enumerate(self.line_names):
            self.__create_line(line_name, i)

    def __create_line(self, line_name: str, index: int) -> None:
        colour = (
            Graph.LINE_COLOUR_ORDER[index]
            if self.num_lines > 1
            else Colours.NUS_BLUE
        )

        plot = self.plot(
            pen=pg.mkPen(colour.value, width=Graph.PEN_WIDTH), name=line_name
        )
        self.graph_plots.append(plot)

        data = np.array([])
        self.graph_data.append(data)
        plot.setData(data)

        label = self.__create_value_label(line_name, colour, index)
        self.graph_value_labels.append(label)

    def __create_value_label(
        self, line_name: str, colour: Colours, index: int
    ) -> pg.LabelItem:
        label = pg.LabelItem(
            f"{line_name}: {Graph.LABEL_DEFAULT_TEXT}",
            color=colour.value,
            size=Graph.LABEL_FONT_SIZE,
        )
        label.setParentItem(self.graphicsItem())
        label.anchor(
            itemPos=(
                1,
                Graph.LABEL_VERTICAL_OFFSET
                + index * Graph.LABEL_VERTICAL_SPACING,
            ),
            parentPos=(
                1,
                Graph.LABEL_HORIZONTAL_OFFSET
                + index * Graph.LABEL_HORIZONTAL_SPACING,
            ),
        )
        return label

    def update(self, values: list[float]) -> None:
        if any(len(data) > Graph.TIME_VIEW for data in self.graph_data):
            self.pointer += 1

        self.__update_view_range()
        self.__update_lines(values)

    def __update_view_range(self) -> None:
        self.getViewBox().setXRange(
            self.pointer, self.pointer + Graph.TIME_VIEW
        )

        y_min = min(
            0,
            min(
                (data[-Graph.TIME_VIEW :].min() if len(data) > 0 else 0)
                for data in self.graph_data
            ),
        )
        y_max = max(
            (data[-Graph.TIME_VIEW :].max() if len(data) > 0 else 100)
            for data in self.graph_data
        )

        self.getViewBox().setYRange(
            y_min * Graph.Y_RANGE_PADDING, y_max * Graph.Y_RANGE_PADDING
        )

    def __update_lines(self, values: list[float]) -> None:
        for i, value in enumerate(values):
            self.graph_data[i] = np.append(self.graph_data[i], float(value))
            self.graph_plots[i].setData(self.graph_data[i])
            self.graph_value_labels[i].setText(
                f"{self.line_names[i]}: {value if value != nan else "NaN"}"
            )
