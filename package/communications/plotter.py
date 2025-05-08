from numpy import var
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import shutil
import os

from package.constants import (
    TelemetryFieldsCSVHeadings,
    TelemetryUnits,
)


class Plotter:
    LOGS_DIR = "logs/"
    TIME_FORMAT = "%H:%M:%S"
    NBINS = 10
    PLOTS_1_LINE = [
        TelemetryFieldsCSVHeadings.ALTITUDE.value,
        TelemetryFieldsCSVHeadings.TEMPERATURE.value,
        TelemetryFieldsCSVHeadings.PRESSURE.value,
        TelemetryFieldsCSVHeadings.VOLTAGE.value,
        TelemetryFieldsCSVHeadings.AUTO_GYRO_ROTATION_RATE.value,
    ]
    PLOTS_3_LINES = [
        [
            TelemetryFieldsCSVHeadings.GYRO_R.value,
            TelemetryFieldsCSVHeadings.GYRO_P.value,
            TelemetryFieldsCSVHeadings.GYRO_Y.value,
        ],
        [
            TelemetryFieldsCSVHeadings.ACCEL_R.value,
            TelemetryFieldsCSVHeadings.ACCEL_P.value,
            TelemetryFieldsCSVHeadings.ACCEL_Y.value,
        ],
        [
            TelemetryFieldsCSVHeadings.MAG_R.value,
            TelemetryFieldsCSVHeadings.MAG_P.value,
            TelemetryFieldsCSVHeadings.MAG_Y.value,
        ],
    ]

    def __init__(self, date_time: str, csv_file: str) -> None:
        self.csv_file = csv_file
        self.data = None
        self.log_dir = f"{Plotter.LOGS_DIR}{date_time}/"

    def __load_data(self) -> bool:
        self.data = pd.read_csv(self.csv_file)
        if self.data.empty:
            print("No data found in the CSV file.")
            if os.path.exists(self.log_dir):
                shutil.rmtree(self.log_dir)
            return False

        self.data["TIME_PASSED"] = (
            pd.to_datetime(
                self.data[TelemetryFieldsCSVHeadings.MISSION_TIME.value],
                format="%H:%M:%S",
            )
            - pd.to_datetime(
                self.data[TelemetryFieldsCSVHeadings.MISSION_TIME.value].iloc[
                    0
                ],
                format="%H:%M:%S",
            )
        ).dt.total_seconds()

        return True

    def generate_plots(self) -> None:
        if not self.__load_data():
            return

        print("Generating plots...")
        for plot in Plotter.PLOTS_1_LINE:
            self._plot_single_line(plot)

        for plot in Plotter.PLOTS_3_LINES:
            self._plot_three_lines(plot)

    def _plot_single_line(self, plot: str) -> None:
        plt.figure()
        variable = " ".join(word.capitalize() for word in plot.split("_"))

        plt.plot(self.data["TIME_PASSED"], self.data[plot])
        plt.title(f"{variable} over Time")
        plt.xlabel(f"Time Passed/s")
        plt.ylabel(f"{variable}/{self.__get_unit(plot)}")
        plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=self.NBINS))
        plt.savefig(f"{self.log_dir}{variable.lower()}.png")
        plt.close()

    def _plot_three_lines(self, plot: list) -> None:
        plt.figure()
        legend_labels = []
        variable = " ".join(
            word.capitalize() for word in plot[0].split("_")[:-1]
        )
        if variable == "Accel":
            variable = "Acceleration"
        elif variable == "Mag":
            variable = "Magnetometer"

        for line in plot:
            plt.plot(self.data["TIME_PASSED"], self.data[line])
            if line.endswith("R"):
                legend_labels.append(f"{variable} Roll")
            elif line.endswith("P"):
                legend_labels.append(f"{variable} Pitch")
            elif line.endswith("Y"):
                legend_labels.append(f"{variable} Yaw")
            else:
                legend_labels.append(line)

        plt.title(f"{variable} over Time")
        plt.xlabel(f"Time Passed/s")
        plt.ylabel(f"{variable}/{self.__get_unit(plot[0])}")
        plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=self.NBINS))
        plt.legend(legend_labels, loc="upper right")
        plt.savefig(f"{self.log_dir}{variable.lower()}.png")
        plt.close()

    def __get_unit(self, field: str) -> str:
        if field not in [
            member.value for member in TelemetryFieldsCSVHeadings
        ]:
            return ""

        if field == TelemetryFieldsCSVHeadings.ALTITUDE.value:
            return TelemetryUnits.ALTITUDE.value
        elif field == TelemetryFieldsCSVHeadings.TEMPERATURE.value:
            return TelemetryUnits.TEMPERATURE.value
        elif field == TelemetryFieldsCSVHeadings.PRESSURE.value:
            return TelemetryUnits.PRESSURE.value
        elif field == TelemetryFieldsCSVHeadings.VOLTAGE.value:
            return TelemetryUnits.VOLTAGE.value
        elif field in [
            TelemetryFieldsCSVHeadings.GYRO_R.value,
            TelemetryFieldsCSVHeadings.GYRO_P.value,
            TelemetryFieldsCSVHeadings.GYRO_Y.value,
        ]:
            return TelemetryUnits.GYRO.value
        elif field in [
            TelemetryFieldsCSVHeadings.ACCEL_R.value,
            TelemetryFieldsCSVHeadings.ACCEL_P.value,
            TelemetryFieldsCSVHeadings.ACCEL_Y.value,
        ]:
            return TelemetryUnits.ACCELERATION.value
        elif field in [
            TelemetryFieldsCSVHeadings.MAG_R.value,
            TelemetryFieldsCSVHeadings.MAG_P.value,
            TelemetryFieldsCSVHeadings.MAG_Y.value,
        ]:
            return TelemetryUnits.MAGNETOMETER.value
        elif field == TelemetryFieldsCSVHeadings.AUTO_GYRO_ROTATION_RATE.value:
            return TelemetryUnits.GYRO_ROTATION_RATE.value

        return ""
