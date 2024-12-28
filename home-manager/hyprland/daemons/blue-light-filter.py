#!/usr/bin/env python3

import subprocess
import time
from datetime import datetime, timedelta
from itertools import cycle

SCHEDULE: dict[tuple[int, int], int | None] = {
    (5, 0): 5500,
    (6, 0): None,

    (17, 0): 6000,
    (18, 0): 5500,
    (18, 30): 5000,
    (19, 0): 4500,
    (19, 30): 4250,
    (20, 0): 4000,
    (20, 30): 3750,
    (21, 0): 3500,
    (21, 30): 3250,
    (22, 0): 3000,
    (22, 30): 2800,
    (23, 0): 2700,
    (23, 30): 2600,
}

cyclic_schedule = cycle(SCHEDULE.items())


def shift_to_now() -> None:
    """Shift the schedule to the current time."""
    now = datetime.now()
    current = (now.hour, now.minute)

    # Advance cycle until we find the current position
    current_filter_i = 0
    for i, time_point in enumerate(SCHEDULE):
        if current < time_point:
            current_filter_i = i - 1
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
        now = datetime.now()
        target = now.replace(hour=time_point[0], minute=time_point[1], second=0)
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
