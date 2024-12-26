#!/usr/bin/env python3

import atexit
import concurrent.futures
import os
import signal
import sys
import time
from functools import partial

from audio import audio_monitor
from power import power_monitor
from vpn import vpn_monitor

LOCK_FILE = "/tmp/sysmonitor.lock"
MAX_RETRIES = 3
RETRY_DELAY = 3  # seconds


def create_lock_file():
    if os.path.exists(LOCK_FILE):
        print("Another instance is already running.")
        sys.exit()
    print("Creating lock file.")
    open(LOCK_FILE, "w").close()


def remove_lock_file():
    if os.path.exists(LOCK_FILE):
        print("Cleaning up lock file.")
        os.remove(LOCK_FILE)


def signal_handler(signum, frame):
    print(f"Signal {signum} received, cleaning up...")
    remove_lock_file()
    sys.exit(0)


def monitor_wrapper(monitor_func, name):
    retry_count = 0
    while True:
        try:
            return monitor_func()
        except Exception as e:
            retry_count += 1
            if retry_count > MAX_RETRIES:
                print(f"{name} failed after {MAX_RETRIES} retries: {e}")
                raise
            print(
                f"{name} failed, retrying in {RETRY_DELAY} seconds... ({retry_count}/{MAX_RETRIES})"
            )
            time.sleep(RETRY_DELAY)


def main():
    create_lock_file()
    atexit.register(remove_lock_file)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    monitors = {"audio": audio_monitor, "power": power_monitor, "vpn": vpn_monitor}

    while True:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(monitor_wrapper, func, name): name
                for name, func in monitors.items()
            }

            for future in concurrent.futures.as_completed(futures):
                monitor_name = futures[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"Monitor {monitor_name} failed permanently: {e}")
                    # Resubmit the failed monitor
                    new_future = executor.submit(
                        monitor_wrapper, monitors[monitor_name], monitor_name
                    )
                    futures[new_future] = monitor_name


if __name__ == "__main__":
    main()
