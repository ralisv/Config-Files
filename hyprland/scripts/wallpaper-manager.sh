#!/usr/bin/env bash

swww init

export WALLPAPER_DIR="$HOME/Pictures/Wallpapers/2560x1600"
export POSITIONS=("left" "right" "bottom" "top" "center" "top-left" "top-right" "bottom-left" "bottom-right")  # Add more transition types as needed

while true; do
    wallpaper=$(ls $WALLPAPER_DIR | shuf -n 1)

    position=${POSITIONS[$RANDOM % ${#POSITIONS[@]}]}

    swww img --transition-type "grow" --transition-pos $position $WALLPAPER_DIR/$wallpaper

    # Wait for half an hour before the next iteration
    sleep 1800
done
