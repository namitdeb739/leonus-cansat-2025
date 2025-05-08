import sys
import argparse
from package.app import App
from package.config import DevMode


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the application in different modes."
    )
    parser.add_argument(
        "--dev_mode",
        choices=["laptop", "monitor"],
        required=True,
        help="Specify the development mode: 'laptop' or 'monitor'.",
    )
    args = parser.parse_args()

    if args.dev_mode not in ["laptop", "monitor"]:
        print("Invalid dev_mode. Use 'laptop' or 'monitor'.")
        return 1

    app = App(sys.argv, DevMode(args.dev_mode))

    try:
        return app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted. Exiting gracefully.")
        app.on_exit()
        return 1


if __name__ == "__main__":
    sys.exit(main())
