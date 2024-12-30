#!/usr/bin/env python3

import subprocess
import time
from datetime import datetime, timedelta
from itertools import cycle

# descent parameters
DESCENT_HOUR_START = 16
INITIAL_TEMP = 6000
MINIMUM_TEMP = 1000

TEMP_DECREASE_PER_STEP = 375
STEP_INTERVAL_MINUTES = 30


def calculate_temperature(hours: int, minutes: int) -> int:
    """Calculate the temperature at the given time based on descent parameters."""
    hours_since_start = hours - DESCENT_HOUR_START
    if hours_since_start < 0:
        return INITIAL_TEMP

    steps = (hours_since_start * 60 + minutes) // STEP_INTERVAL_MINUTES

    total_decrease = steps * TEMP_DECREASE_PER_STEP
    return max(INITIAL_TEMP - total_decrease, MINIMUM_TEMP)


SCHEDULE: dict[tuple[int, int], int | None] = {
    (5, 0): 5500,
    (6, 0): None,
    # linear temperature descent
    **{
        (h, m): calculate_temperature(h, m)
        for h in range(16, 23)
        for m in range(0, 60, STEP_INTERVAL_MINUTES)
    },
}

cyclic_schedule = cycle(SCHEDULE.items())


def shift_to_now() -> None:
    """Shift the schedule to the current time."""
    now = datetime.now()
    current = (now.hour, now.minute)

    # Advance cycle until we find the current position
    current_filter_i = -1
    for i, time_point in enumerate(SCHEDULE):
        if current < time_point:
            current_filter_i = i - 1 if i > 0 else len(SCHEDULE) - 1
            break

    # Shift the schedule
    for _ in range(current_filter_i):
        next(cyclic_schedule)


def set_temperature(temp: int) -> None:
    """Set the temperature of the screen."""
    try:
        subprocess.Popen(
            ["hyprsunset", "--temperature", str(temp)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.SubprocessError:
        pass


def kill_hyprsunset() -> None:
    """Kill all instances of hyprsunset."""
    try:
        subprocess.Popen(
            ["pkill", "hyprsunset"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.SubprocessError:
        pass


def set_filter(temp: int | None) -> None:
    """Set the filter based on the given temperature."""
    if temp is not None:
        print(f"Setting temperature to {temp}")
        set_temperature(temp)

    else:
        print("No filter; killing all hyprsunset instances")
        kill_hyprsunset()


def daemon_process():
    """The main daemon process."""
    shift_to_now()
    set_filter(next(cyclic_schedule)[1])

    for time_point, temp in cyclic_schedule:
        # Calculate sleep time until next change
        now = datetime.now().replace(microsecond=0)
        target = now.replace(
            hour=time_point[0], minute=time_point[1], second=0, microsecond=0
        )
        if target <= now:
            target += timedelta(days=1)
        to_wait = target - now

        print(f"Sleeping for {to_wait} until {target}")
        time.sleep((target - now).total_seconds())
        if temp is not None:
            print(f"Setting temperature to {temp}")
            set_temperature(temp)
        else:
            print("Killing all hyprsunset instances")
            kill_hyprsunset()


if __name__ == "__main__":
    try:
        daemon_process()
    except KeyboardInterrupt:
        pass
