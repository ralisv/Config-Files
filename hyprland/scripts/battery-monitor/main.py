#!/usr/bin/env python3

BATTERY_DIRECTORY_PATH = "/sys/class/power_supply/BAT0"
CAPACITY_FILENAME = "capacity"
STATUS_FILENAME = "status"
ENERGY_NOW_FILENAME = "energy_now"

from pathlib import Path
from select import POLLPRI, poll


def main():
    poller = poll()

    files = [
        (Path(BATTERY_DIRECTORY_PATH) / filename).open()
        for filename in [CAPACITY_FILENAME, STATUS_FILENAME, ENERGY_NOW_FILENAME]
    ]

    fd_map = {file.fileno(): file for file in files}

    for file in fd_map.keys():
        poller.register(file, POLLPRI)

    for _ in range(10):
        modified_files = poller.poll(60_000)

        for fd, event in modified_files:
            file = fd_map[fd]
            print(f"{file.name}: {file.read().strip()} : {event}")


if __name__ == "__main__":
    main()
