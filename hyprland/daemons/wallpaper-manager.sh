#!/usr/bin/env bash

swww-daemon 2>/dev/null

# Get the directory of the current script
DIR=$(dirname "$0")
SCRIPT_DIR="$DIR/../scripts"

while true; do
    # Call the pick-random-wallpaper.sh script using the determined script directory
    "$SCRIPT_DIR/../scripts/pick-random-wallpaper.sh"
    sleep 1800
done
