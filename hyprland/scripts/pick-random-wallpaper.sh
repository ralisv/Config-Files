#!/usr/bin/env bash

# If swww query fails,
swww query 2>/dev/null || swww init

export WALLPAPER_DIR="$HOME/Pictures/Wallpapers/2560x1600"
export POSITIONS=("left" "right" "bottom" "top" "center" "top-left" "top-right" "bottom-left" "bottom-right")  # Add more transition types as needed

wallpaper=$(ls $WALLPAPER_DIR | shuf -n 1)

position=${POSITIONS[$RANDOM % ${#POSITIONS[@]}]}

swww img --transition-type "grow" --transition-pos $position $WALLPAPER_DIR/$wallpaper
