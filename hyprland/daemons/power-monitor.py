#!/usr/bin/env python3

import subprocess
import time
from pathlib import Path
from typing import Tuple

BAT_DIR = Path("/sys/class/power_supply/BAT0/")
STATUS_FILE = BAT_DIR / "status"
CAPACITY_FILE = BAT_DIR / "capacity"
POWER_NOW_FILE = BAT_DIR / "power_now"
ENERGY_NOW_FILE = BAT_DIR / "energy_now"
ENERGY_FULL_FILE = BAT_DIR / "energy_full"

SCRIPT_DIR = Path(__file__).parent.resolve()

EWW_CONFIG = Path("~/Config-Files/hyprland/eww").expanduser()

FIRST_WARNING_TIME = 10_000
SECOND_WARNING_TIME = 100_000
FULL_BATTERY_NOTE_TIME = 5_000
STATE_CHANGE_NOTE_TIME = 5_000


def prepend_zero_if_single_digit(number: int) -> str:
    return f"0{number}" if 0 <= number <= 9 else str(number)


def read_file(file_path: Path) -> str:
    return file_path.read_text().strip()


def update_eww(status_report: str) -> None:
    subprocess.run(
        [
            "eww",
            "--config",
            EWW_CONFIG.as_posix(),
            "update",
            f"battery-info={status_report}",
        ]
    )


def send_notification(urgency: str, timeout: int, title: str, body: str) -> None:
    subprocess.run(["notify-send", "-u", urgency, "-t", str(timeout), title, body])


def calculate_remaining_time(energy_diff: int, power_now: int) -> Tuple[int, int]:
    remaining_time_hours = energy_diff // power_now
    remaining_time_minutes = (energy_diff % power_now * 60) // power_now
    return remaining_time_hours, remaining_time_minutes


def format_time(hours: int, minutes: int) -> str:
    return (
        f"{prepend_zero_if_single_digit(hours)}:{prepend_zero_if_single_digit(minutes)}"
    )


def get_status_report(
    status: str, capacity: int, power_now: int, energy_now: int, energy_full: int
) -> str:
    if status == "Charging":
        if power_now == 0:
            return f"{status}, {capacity}%"
        hours, minutes = calculate_remaining_time(energy_full - energy_now, power_now)
        time_formatted = format_time(hours, minutes)
        return f"{status}, {time_formatted} to fully charged, {capacity}%"

    elif status == "Discharging":
        if power_now == 0:
            return f"{status}, {capacity}%"
        hours, minutes = calculate_remaining_time(energy_now, power_now)
        time_formatted = format_time(hours, minutes)
        return f"{status}, {time_formatted} remaining, {capacity}%"

    else:
        return f"{status}, {capacity}%"


def main() -> None:
    status = read_file(STATUS_FILE)
    energy_full = int(read_file(ENERGY_FULL_FILE))

    first_warning = False
    second_warning = False

    while True:
        new_status = read_file(STATUS_FILE)
        capacity = int(read_file(CAPACITY_FILE))
        power_now = int(read_file(POWER_NOW_FILE))
        energy_now = int(read_file(ENERGY_NOW_FILE))

        status_report = get_status_report(
            new_status, capacity, power_now, energy_now, energy_full
        )
        update_eww(status_report)

        if status != new_status:
            if new_status == "Full":
                send_notification(
                    "normal", FULL_BATTERY_NOTE_TIME, "Battery fully charged", ""
                )

            elif status == "Discharging" and new_status == "Charging":
                send_notification(
                    "normal",
                    STATE_CHANGE_NOTE_TIME,
                    "Battery is now charging",
                    f"Current capacity: {capacity}%",
                )
                first_warning = False
                second_warning = False

            elif status == "Charging" and new_status == "Discharging":
                send_notification(
                    "normal",
                    STATE_CHANGE_NOTE_TIME,
                    "Battery is now discharging",
                    f"Current capacity: {capacity}%",
                )

        status = new_status

        if status == "Discharging":
            if capacity <= 10 and not second_warning:
                send_notification(
                    "critical",
                    SECOND_WARNING_TIME,
                    "Battery critically low",
                    f"Battery is at {capacity}%",
                )
                first_warning = True
                second_warning = True

            elif capacity <= 20 and not first_warning:
                send_notification(
                    "normal",
                    FIRST_WARNING_TIME,
                    "Battery low",
                    f"Battery is at {capacity}%",
                )
                first_warning = True

        time.sleep(1)  # Check every second


if __name__ == "__main__":
    main()
