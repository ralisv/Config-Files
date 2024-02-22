#!/usr/bin/env bash

bat_path="/sys/class/power_supply/BAT0/"

status=$(cat "$bat_path/status")
capacity=$(cat "$bat_path/capacity")

# power_now can be zero when the battery is fully charged or the charging status just changed
power_now=$(cat "$bat_path/power_now")

energy_now=$(cat "$bat_path/energy_now")
energy_full=$(cat "$bat_path/energy_full")

prepend_zero_if_single_digit() {
    local number="$1"
    if [ "$number" -ge 0 ] && [ "$number" -le 9 ]; then
        echo "0$number"
    else
        echo "$number"
    fi
}

if [ "$status" = "Charging" ]; then
    remaining_time_hours=$((($energy_full - $energy_now) / power_now))
    remaining_time_minutes=$((($energy_full - $energy_now) % power_now * 60 / power_now))
    remaining_time_string=$(prepend_zero_if_single_digit "$remaining_time_hours"):$(prepend_zero_if_single_digit "$remaining_time_minutes")
    echo "$status, $remaining_time_string to fully charged, $capacity%"
elif [ "$status" = "Discharging" ]; then
    remaining_time_hours=$(($energy_now / $power_now))
    remaining_time_minutes=$((($energy_now % $power_now) * 60 / $power_now))
    remaining_time_string=$(prepend_zero_if_single_digit "$remaining_time_hours"):$(prepend_zero_if_single_digit "$remaining_time_minutes")
    echo "$status, $remaining_time_string remaining, $capacity%"
else # Full
    echo "$status $capacity%"
fi
