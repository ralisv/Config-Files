#!/usr/bin/env bash

sleep 1  # Wait a while to have a good look at the hyprland logo
swww init

# Get the directory of the current script
SCRIPT_DIR=$(dirname "$0")

while true; do
    # Call the pick-random-wallpaper.sh script using the determined script directory
    "$SCRIPT_DIR/pick-random-wallpaper.sh"
    sleep 1800
done