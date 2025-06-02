from math import nan
from typing import Iterable
import numpy as np
import pyqtgraph as pg
from package.constants import Colours


class CommaAxis(pg.AxisItem):
    def tickStrings(
        self, values: list[float], scale: float, spacing: float
    ) -> list[str]:
        return [
            f"{int(value):,}" if value == int(value) else f"{value:,.1f}"
            for value in values
        ]


class Graph(pg.PlotItem):
    LINE_COLOUR_ORDER = [Colours.RED, Colours.GREEN, Colours.NUS_BLUE]
    TIME_VIEW = 120
    PEN_WIDTH = 3
    LEFT = "left"
    BOTTOM = "bottom"
    FONT = "Arial"
    LABEL_FONT_SIZE = "12pt"
    AXIS_FONT_SIZE = 12
    LABEL_DEFAULT_TEXT = "NIL"
    X_RANGE_PADDING = 1.25
    Y_RANGE_PADDING = 1.25
    LABEL_HORIZONTAL_SPACING = 0
    LABEL_HORIZONTAL_OFFSET = -0.5
    LABEL_VERTICAL_OFFSET = 30
    LABEL_VERTICAL_SPACING = 15

    def __init__(self, title: str, line_names: Iterable[str]) -> None:
        super().__init__(
            name=title,
            title=self.__format_title(title),
            viewBox=pg.ViewBox(border=Colours.RICH_BLACK.value),
            axisItems={
                Graph.BOTTOM: CommaAxis(orientation=Graph.BOTTOM),
                Graph.LEFT: CommaAxis(orientation=Graph.LEFT),
            },
        )

        self.getAxis(Graph.LEFT).setStyle(
            tickFont=pg.QtGui.QFont(Graph.FONT, Graph.AXIS_FONT_SIZE)
        )
        self.getAxis(Graph.BOTTOM).setStyle(
            tickFont=pg.QtGui.QFont(Graph.FONT, Graph.AXIS_FONT_SIZE)
        )

        self.setSizePolicy(
            pg.QtWidgets.QSizePolicy.Policy.Expanding,
            pg.QtWidgets.QSizePolicy.Policy.Expanding,
        )

        self.pointer = 0
        self.num_lines = len(line_names)
        self.line_names = list(line_names)
        self.graph_plots: list[pg.PlotDataItem] = []
        self.graph_data: list[np.ndarray] = []
        self.graph_value_labels: list[pg.LabelItem] = []

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
        self.__anchor_label(index, label)
        return label

    def __anchor_label(self, index: int, label: pg.LabelItem) -> None:
        label.anchor(
            itemPos=(1, 0),
            parentPos=(1, 0),
            offset=(
                Graph.LABEL_HORIZONTAL_OFFSET,
                Graph.LABEL_VERTICAL_OFFSET
                + index * Graph.LABEL_VERTICAL_SPACING,
            ),
        )

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
                f"{self.line_names[i]}: {f"{value:,}" if value != nan else "NaN"}"
            )

            self.__anchor_label(i, self.graph_value_labels[i])
