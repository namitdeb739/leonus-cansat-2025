import argparse
import os
import package.plotter as plotter


def main():
    parser = argparse.ArgumentParser(
        description="Generate plots from a CSV file"
    )
    parser.add_argument("csv_file", type=str, help="Path to the CSV file")
    args = parser.parse_args()

    # Extract the parent directory name
    parent_dir = os.path.basename(os.path.dirname(args.csv_file))

    # Parse the last 6 characters as start_time
    start_time = parent_dir[-15:]

    print(f"Generating plots from {args.csv_file}")
    plotter.generate_plots(start_time, args.csv_file)


if __name__ == "__main__":
    main()
