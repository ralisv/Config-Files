#!/usr/bin/env python3

import atexit
import concurrent.futures
import os
import signal
import sys

from audio import audio_monitor
from power import power_monitor
from vpn import vpn_monitor

# Define the path for the lock file in the /tmp directory
LOCK_FILE = "/tmp/sysmonitor.lock"


def create_lock_file():
    """Create a lock file to prevent multiple instances."""
    if os.path.exists(LOCK_FILE):
        print("Another instance is already running.")
        sys.exit()
    else:
        print("Creating lock file.")
        open(LOCK_FILE, "w").close()


def remove_lock_file():
    """Remove the lock file upon exit."""
    if os.path.exists(LOCK_FILE):
        print("Cleaning up lock file.")
        os.remove(LOCK_FILE)


def signal_handler(signum, frame):
    """Handle termination signals to clean up the lock file."""
    print(f"Signal {signum} received, cleaning up...")
    remove_lock_file()
    sys.exit(0)


def main():
    # Create a lock file and register its removal on exit
    create_lock_file()
    atexit.register(remove_lock_file)

    # Register signal handlers for termination signals
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # Run all monitor functions in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(audio_monitor),
            executor.submit(power_monitor),
            executor.submit(vpn_monitor),
        ]

        # Wait for all futures to complete
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()
