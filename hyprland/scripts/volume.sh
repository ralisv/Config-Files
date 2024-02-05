#!/usr/bin/env bash

if [ -z "$1" ]; then
    echo "Usage: $0 {up|down|mute}"
    exit 1
fi

if [ "$1" = "up" ]; then 
    wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+
elif [ "$1" = "down" ]; then 
    wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-
elif [ "$1" = "mute" ]; then 
    wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle
else
    echo "Invalid argument: $1"
    echo "Usage: $0 {up|down|mute}"
    exit 1
fi


export SOUND_SETTINGS_CACHE=`wpctl get-volume @DEFAULT_AUDIO_SINK@`
eww --config ~/Config-Files/hyprland/eww update "sound-settings=$SOUND_SETTINGS_CACHE"