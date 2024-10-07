#!/usr/bin/env bash

if [ -z "$1" ]; then
    echo "Usage: $0 {up|down|mute}"
    exit 1
fi

if [ "$1" = "up" ]; then 
    wpctl set-volume -l 1.5 @DEFAULT_AUDIO_SINK@ 5%+ && wpctl set-mute @DEFAULT_AUDIO_SINK@ 0
elif [ "$1" = "down" ]; then 
    wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-
elif [ "$1" = "mute" ]; then 
    wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle
elif [ "$1" = "get" ]; then 
    wpctl get-volume @DEFAULT_AUDIO_SINK@
else
    echo "Invalid argument: $1"
    echo "Usage: $0 {up|down|mute}"
    exit 1
fi
