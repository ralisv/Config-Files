#!/usr/bin/env bash

sleep 1  # Wait a while to have a good look at the hyprland logo
swww init

while true; do
    ./pick-random-wallpaper.sh
    sleep 1800
done
