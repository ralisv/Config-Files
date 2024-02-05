#!/usr/bin/env bash

if [ $1 = "up" ]; then wpctl set-volume -l 1.5 @DEFAULT_AUDIO_SINK@ 5%+;
elif [ $1 = "down" ]; then wpctl set-volume -l 1.5 @DEFAULT_AUDIO_SINK@ 5%-;
elif [ $1 = "mute" ]; then wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle;
fi

export SOUND_SETTINGS_CACHE=`wpctl get-volume @DEFAULT_AUDIO_SINK@`
eww --config ~/Config-Files/hyprland/eww update "sound-settings=$SOUND_SETTINGS_CACHE"