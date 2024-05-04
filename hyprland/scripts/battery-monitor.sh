#!/usr/bin/env bash

BAT_DIR="/sys/class/power_supply/BAT0/"
STATUS_FILE="$BAT_DIR/status"
CAPACITY_FILE="$BAT_DIR/capacity"
POWER_NOW_FILE="$BAT_DIR/power_now"
ENERGY_NOW_FILE="$BAT_DIR/energy_now"
ENERGY_FULL_FILE="$BAT_DIR/energy_full"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
LOG_FILE="$SCRIPT_DIR/battery-monitor.log"
touch $LOG_FILE

FIRST_WARNING_TIME=10
SECOND_WARNING_TIME=100

prepend_zero_if_single_digit() {
    local number="$1"
    if [ "$number" -ge 0 ] && [ "$number" -le 9 ]; then
        echo "0$number"
    else
        echo "$number"
    fi
}

status=$(cat "$STATUS_FILE")
capacity=$(cat "$CAPACITY_FILE")
power_now=$(cat "$POWER_NOW_FILE")
energy_now=$(cat "$ENERGY_NOW_FILE")
energy_full=$(cat "$ENERGY_FULL_FILE")

first_warning=false;
second_warning=false;

status_report=""

upower --monitor 2> >(tee -a "$LOG_FILE" >&2) | while read -r line; do
    # Update battery stats
    new_status=$(cat "$STATUS_FILE")
    capacity=$(cat "$CAPACITY_FILE")
    power_now=$(cat "$POWER_NOW_FILE")
    energy_now=$(cat "$ENERGY_NOW_FILE")
    
    # Update eww widget
    if [ $new_status = "Charging" ] && [ $power_now != "0" ]; then
        remaining_time_hours=$((($energy_full - $energy_now) / $power_now))
        remaining_time_minutes=$((($energy_full - $energy_now) % $power_now * 60 / $power_now))
        remaining_time_formatted=$(prepend_zero_if_single_digit $remaining_time_hours):$(prepend_zero_if_single_digit $remaining_time_minutes)
        
        status_report="$new_status, $remaining_time_formatted to fully charged, $capacity%"
        
        elif [ $new_status = "Discharging" ]  && [ $power_now != "0" ]; then
        remaining_time_hours=$(($energy_now / $power_now))
        remaining_time_minutes=$((($energy_now % $power_now) * 60 / $power_now))
        remaining_time_formatted=$(prepend_zero_if_single_digit $remaining_time_hours):$(prepend_zero_if_single_digit $remaining_time_minutes)
        
        status_report="$new_status, $remaining_time_formatted remaining, $capacity%"
        
        elif [ $new_status = "Not Charging" ] || [ $new_status = "Full" ]; then
        remaining_time_formatted="00:00"
        
        status_report="$new_status, $capacity%"
    fi
    eww --config ~/Config-Files/hyprland/eww update "battery-info=$status_report"
    
    # If the status has changed and it's become fully charged, send notification
    if [ $status != $new_status ]; then
        if [ $new_status = "Full" ]; then
            notify-send -t 5 "Battery fully charged"
            elif [ $new_status = "Charging" ]; then
            first_warning=false;
            second_warning=false;
        fi
    fi
    
    status=$new_status
    
    # Send notifications if battery is low, and only once
    if [ $status = "Discharging" ]; then
        if [ $capacity -le 10 ] && [ $second_warning = false ]; then
            notify-send -u critical -t $SECOND_WARNING_TIME "Battery critically low" "Battery is at $capacity%"
            first_warning=true;
            second_warning=true;
            elif [ $capacity -le 20 ] && [ $first_warning = false ]; then
            notify-send -u normal -t $FIRST_WARNING_TIME "Battery low" "Battery is at $capacity%"
            first_warning=true;
        fi
    fi
    
done
