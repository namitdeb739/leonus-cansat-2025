if __name__ == "__main__":
    import sys
    import argparse
    from package.app import App

    parser = argparse.ArgumentParser(
        description="Cansat Telemetry & Ground Control"
    )
    parser.add_argument(
        "dev_type", type=str, choices=["laptop", "monitor"], help="Device type"
    )
    args = parser.parse_args()

    app = App(sys.argv, args.dev_type)

    try:
        sys.exit(app.run())
    except KeyboardInterrupt:
        app.on_exit()
