import argparse
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler
import subprocess


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, command: str) -> None:
        self.command = command
        self.process = None
        self.restart_process()

    def restart_process(self) -> None:
        if self.process:
            self.process.terminate()
            self.process.wait()
        self.process = subprocess.Popen(self.command, shell=True)

    def on_any_event(self, event: FileSystemEvent) -> None:
        if event.src_path.endswith(".py") or event.src_path.endswith(".css"):
            self.restart_process()


def main():
    parser = argparse.ArgumentParser(
        description="Watch for file changes and restart the application."
    )
    parser.add_argument(
        "dev_type",
        choices=["laptop", "monitor"],
        help="Type of development environment",
    )
    args = parser.parse_args()

    path = "."
    command = f"{sys.executable} main.py {args.dev_type}"
    event_handler = ChangeHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(5000)
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
