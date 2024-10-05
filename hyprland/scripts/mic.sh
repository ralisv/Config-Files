#!/usr/bin/env bash

AUDIO_SOURCE="@DEFAULT_AUDIO_SOURCE@"

toggle_mute() {
    wpctl set-mute "$AUDIO_SOURCE" toggle
    update_eww
}

get_status() {
    local status=$(wpctl get-volume "$AUDIO_SOURCE")
    echo "$status" | sed 's/Volume:/Mic:/'
}

update_eww() {
    local status=$(get_status)
    eww --config ~/Config-Files/hyprland/eww update "mic-settings=$status"
}

case "$1" in
    toggle)
        toggle_mute
        ;;
    get)
        get_status
        ;;
    *)
        echo "Usage: $0 {toggle|get}"
        exit 1
        ;;
esac