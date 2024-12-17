#!/usr/bin/env python3

import subprocess
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional, Tuple

from utils import send_notification, update_eww

BAT_DIR = Path("/sys/class/power_supply/BAT0/")
STATUS_FILE = BAT_DIR / "status"
CAPACITY_FILE = BAT_DIR / "capacity"
POWER_NOW_FILE = BAT_DIR / "power_now"
ENERGY_NOW_FILE = BAT_DIR / "energy_now"
ENERGY_FULL_FILE = BAT_DIR / "energy_full"

SCRIPT_DIR = Path(__file__).parent.resolve()
EWW_CONFIG = Path("~/Config-Files/hyprland/eww").expanduser()

LOG_PREFIX = "power-monitor: "


class BatteryState(Enum):
    CHARGING = "Charging"
    DISCHARGING = "Discharging"
    FULL = "Full"
    NOT_CHARGING = "Not charging"
    UNKNOWN = "Unknown"


@dataclass
class BatteryStatus:
    state: BatteryState
    capacity: int
    power_now: int
    energy_now: int
    energy_full: int


class NotificationManager:
    def __init__(self):
        # Previous state tracking
        self.prev_status: Optional[BatteryStatus] = None

        # Notification state tracking
        self.full_battery_notified = False
        self.low_battery_notified = False
        self.critical_battery_notified = False

        # Notification timing configuration
        self.notification_cooldown = 1
        self.last_notification_time = 0

    def can_send_notification(self) -> bool:
        """Check if enough time has passed since the last notification"""
        current_time = time.time()
        if current_time - self.last_notification_time < self.notification_cooldown:
            return False
        return True

    def send_notification_with_cooldown(
        self, urgency: str, timeout: int, title: str, message: str
    ) -> None:
        """Send notification if cooldown period has passed"""
        if self.can_send_notification():
            send_notification(urgency, timeout, title, message)
            self.last_notification_time = time.time()
            log(f"Notification sent: {title} - {message}")

    def handle_state_change(self, current_status: BatteryStatus) -> None:
        """Handle notifications for battery state changes"""
        if not self.prev_status:
            return

        if current_status.state != self.prev_status.state:
            if current_status.state == BatteryState.CHARGING:
                self.send_notification_with_cooldown(
                    "normal",
                    5000,
                    "Battery is now charging",
                    f"Current capacity: {current_status.capacity}%",
                )
                # Reset battery warnings when charging starts
                self.low_battery_notified = False
                self.critical_battery_notified = False

            elif current_status.state == BatteryState.DISCHARGING:
                self.send_notification_with_cooldown(
                    "normal",
                    5000,
                    "Battery is now discharging",
                    f"Current capacity: {current_status.capacity}%",
                )

    def handle_capacity_warnings(self, current_status: BatteryStatus) -> None:
        """Handle notifications for battery capacity levels"""
        if current_status.state != BatteryState.DISCHARGING:
            return

        # Critical battery warning (<=10%)
        if current_status.capacity <= 10 and not self.critical_battery_notified:
            self.send_notification_with_cooldown(
                "critical",
                20000,
                "Battery critically low",
                f"Battery is at {current_status.capacity}%",
            )
            self.critical_battery_notified = True
            self.low_battery_notified = True

        # Low battery warning (<=20%)
        elif current_status.capacity <= 20 and not self.low_battery_notified:
            self.send_notification_with_cooldown(
                "normal",
                10000,
                "Battery low",
                f"Battery is at {current_status.capacity}%",
            )
            self.low_battery_notified = True

        # Reset warnings if battery level increases
        elif current_status.capacity > 20:
            self.low_battery_notified = False
            self.critical_battery_notified = False

    def handle_full_battery(self, current_status: BatteryStatus) -> None:
        """Handle notifications for full or near-full battery"""
        if (
            current_status.capacity >= 85
            and current_status.state == BatteryState.CHARGING
            and not self.full_battery_notified
        ):
            self.send_notification_with_cooldown(
                "normal",
                5000,
                "Battery almost fully charged",
                f"Current capacity: {current_status.capacity}%",
            )
            self.full_battery_notified = True
        elif current_status.capacity < 80:
            self.full_battery_notified = False

    def update(self, current_status: BatteryStatus) -> None:
        """Main update method to handle all notification scenarios"""
        self.handle_state_change(current_status)
        self.handle_capacity_warnings(current_status)
        self.handle_full_battery(current_status)

        # Update previous status
        self.prev_status = current_status


def log(message: str):
    """Log a message with a predefined prefix."""
    print(f"{LOG_PREFIX}{message}")


def read_file(file_path: Path) -> str:
    return file_path.read_text().strip()


def prepend_zero_if_single_digit(number: int) -> str:
    return f"0{number}" if 0 <= number <= 9 else str(number)


def calculate_remaining_time(energy_diff: int, power_now: int) -> Tuple[int, int]:
    remaining_time_hours = energy_diff // power_now
    remaining_time_minutes = (energy_diff % power_now * 60) // power_now
    return remaining_time_hours, remaining_time_minutes


def format_time(hours: int, minutes: int) -> str:
    return (
        f"{prepend_zero_if_single_digit(hours)}:{prepend_zero_if_single_digit(minutes)}"
    )


def get_status_report(status: BatteryStatus) -> str:
    power_watts = status.power_now / 1_000_000  # Convert microwatts to watts

    if status.state == BatteryState.CHARGING:
        if status.power_now == 0:
            return f"{status.state.value}, {status.capacity}%"
        hours, minutes = calculate_remaining_time(
            status.energy_full - status.energy_now, status.power_now
        )
        time_formatted = format_time(hours, minutes)
        return f"{status.state.value}, {time_formatted} to fully charged, {status.capacity}%, +{power_watts:.2f}W"

    elif status.state == BatteryState.DISCHARGING:
        if status.power_now == 0:
            return f"{status.state.value}, {status.capacity}%"
        hours, minutes = calculate_remaining_time(status.energy_now, status.power_now)
        time_formatted = format_time(hours, minutes)
        return f"{status.state.value}, {time_formatted} remaining, {status.capacity}%, -{power_watts:.2f}W"

    else:
        return f"{status.state.value}, {status.capacity}%, {power_watts:.2f}W"


def read_battery_status() -> BatteryStatus:
    """Read current battery status from system files"""
    return BatteryStatus(
        state=BatteryState(read_file(STATUS_FILE)),
        capacity=int(read_file(CAPACITY_FILE)),
        power_now=int(read_file(POWER_NOW_FILE)),
        energy_now=int(read_file(ENERGY_NOW_FILE)),
        energy_full=int(read_file(ENERGY_FULL_FILE)),
    )


def power_monitor() -> None:
    log("Monitoring for power changes...")
    notification_manager = NotificationManager()

    while True:
        try:
            current_status = read_battery_status()
            if current_status:
                # Update notifications
                notification_manager.update(current_status)

                # Update system status
                status_report = get_status_report(current_status)
                update_eww({"battery-info": status_report})
                log(f"Status report: {status_report}")

            time.sleep(1)
        except Exception as e:
            log(f"Error in monitor loop: {e}")
            time.sleep(5)  # Wait longer on error


if __name__ == "__main__":
    power_monitor()
