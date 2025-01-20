import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def generate_plots(date_time: str, csv_file: str) -> None:
    data = pd.read_csv(csv_file)

    start_time = pd.to_datetime(
        data["MISSION_TIME"].iloc[0], format="%H:%M:%S"
    )
    data["TIME_PASSED"] = (
        pd.to_datetime(data["MISSION_TIME"], format="%H:%M:%S") - start_time
    ).dt.total_seconds()

    plots_1_line = [
        "ALTITUDE",
        "TEMPERATURE",
        "PRESSURE",
        "VOLTAGE",
        "AUTO_GYRO_ROTATION_RATE",
    ]

    plots_3_lines = [
        ["GYRO_R", "GYRO_P", "GYRO_Y"],
        ["ACCEL_R", "ACCEL_P", "ACCEL_Y"],
        ["MAG_R", "MAG_P", "MAG_Y"],
    ]

    for plot in plots_1_line:
        plt.figure()
        variable = " ".join(word.capitalize() for word in plot.split("_"))

        plt.plot(data["TIME_PASSED"], data[plot])
        plt.title(
            " ".join(word.capitalize() for word in plot.split("_"))
            + " over Time"
        )
        plt.xlabel("Time Passed (s)")
        plt.ylabel(variable)
        plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=10))
        plt.savefig(f"logs/{date_time}/{plot.lower()}.png")
        plt.close()

    for plot in plots_3_lines:
        plt.figure()
        legend_labels = []
        variable = " ".join(
            word.capitalize() for word in plot[0].split("_")[:-1]
        )
        if variable == "Accel":
            variable = "Acceleration"
        if variable == "Mag":
            variable = "Magnetometer"

        for line in plot:
            plt.plot(data["TIME_PASSED"], data[line])
            if line.endswith("R"):
                legend_labels.append(variable + " Roll")
            elif line.endswith("P"):
                legend_labels.append(variable + " Pitch")
            elif line.endswith("Y"):
                legend_labels.append(variable + " Yaw")
            else:
                legend_labels.append(line)

        plt.title(variable + " over Time")
        plt.xlabel("Time Passed (s)")
        plt.ylabel(variable.capitalize())
        plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=10))
        plt.legend(legend_labels, loc="upper right")
        plt.savefig(f"logs/{date_time}/{variable.lower()}.png")
