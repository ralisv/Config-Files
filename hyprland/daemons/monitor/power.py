#!/usr/bin/env python3

import subprocess
import time
from pathlib import Path
from typing import Tuple

from utils import send_notification, update_eww

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

LOG_PREFIX = "power-monitor: "


def log(message: str):
    """Log a message with a predefined prefix."""
    print(f"{LOG_PREFIX}{message}")


def prepend_zero_if_single_digit(number: int) -> str:
    return f"0{number}" if 0 <= number <= 9 else str(number)


def read_file(file_path: Path) -> str:
    return file_path.read_text().strip()


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
    power_watts = power_now / 1_000_000  # Convert microwatts to watts

    if status == "Charging":
        power_sign = "+"
        if power_now == 0:
            return f"{status}, {capacity}%"
        hours, minutes = calculate_remaining_time(energy_full - energy_now, power_now)
        time_formatted = format_time(hours, minutes)
        return f"{status}, {time_formatted} to fully charged, {capacity}%, {power_sign}{power_watts:.2f}W"

    elif status == "Discharging":
        power_sign = "-"
        if power_now == 0:
            return f"{status}, {capacity}%"
        hours, minutes = calculate_remaining_time(energy_now, power_now)
        time_formatted = format_time(hours, minutes)
        return f"{status}, {time_formatted} remaining, {capacity}%, {power_sign}{power_watts:.2f}W"

    else:
        power_sign = ""  # No sign for other states (e.g., "Full")
        return f"{status}, {capacity}%, {power_sign}{power_watts:.2f}W"


def power_monitor() -> None:
    log("Monitoring for power changes...")
    status = read_file(STATUS_FILE)
    energy_full = int(read_file(ENERGY_FULL_FILE))

    full_battery_note = False
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
        update_eww({"battery-info": status_report})

        log(f"Status report: {status_report}")

        if capacity >= 85 and not full_battery_note:
            send_notification(
                "normal",
                FULL_BATTERY_NOTE_TIME,
                "Battery almost fully charged",
                f"Current capacity: {capacity}%",
            )
            full_battery_note = True

            log("Battery fully charged notification sent.")

        if capacity < 80:
            full_battery_note = False

        if status != new_status:
            if status == "Discharging" and new_status == "Charging":
                send_notification(
                    "normal",
                    STATE_CHANGE_NOTE_TIME,
                    "Battery is now charging",
                    f"Current capacity: {capacity}%",
                )
                first_warning = False
                second_warning = False

                log("State change notification sent: Charging.")

            elif status == "Charging" and new_status == "Discharging":
                send_notification(
                    "normal",
                    STATE_CHANGE_NOTE_TIME,
                    "Battery is now discharging",
                    f"Current capacity: {capacity}%",
                )

                log("State change notification sent: Discharging.")

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

                log("Critical battery warning sent.")

            elif capacity <= 20 and not first_warning:
                send_notification(
                    "normal",
                    FIRST_WARNING_TIME,
                    "Battery low",
                    f"Battery is at {capacity}%",
                )
                first_warning = True

                log("Low battery warning sent.")

        time.sleep(1)  # Check every second


if __name__ == "__main__":
    power_monitor()
