#!/usr/bin/env bash

# File to store the current brightness level
BRIGHTNESS_FILE="/tmp/cached-current-brightness"

# Function to save the current brightness
save_brightness() {
    brightnessctl get > "$BRIGHTNESS_FILE"
}

# Function to restore the saved brightness
restore_brightness() {
    if [ -f "$BRIGHTNESS_FILE" ]; then
        brightness=$(cat "$BRIGHTNESS_FILE")
        brightnessctl set "$brightness"
        rm "$BRIGHTNESS_FILE"
    fi
}
# Function to decrease the brightness gradually
decrease_brightness_gradually() {
    while true; do
        brightnessctl set 1-
        sleep 0.1
    done
}

# Check command line argument
if [ "$1" = "save" ]; then
    save_brightness
elif [ "$1" = "restore" ]; then
    restore_brightness
elif [ "$1" = "decrease" ]; then
    decrease_brightness_gradually
else
    echo "Usage: gradual-brightness-decrease.sh [save|restore|decrease]"
    exit 1
fi