#!/usr/bin/env bash

# Initialize swww if not running
swww query 2>/dev/null || swww init

# Directory containing wallpapers
export WALLPAPER_DIR="$HOME/Pictures/Wallpapers/Favorite"
export POSITIONS=("left" "right" "bottom" "top" "center" "top-left" "top-right" "bottom-left" "bottom-right")

# Get list of all monitors using hyprctl
monitors=$(hyprctl monitors | grep Monitor | awk '{print $2}')

# For each monitor, set a random wallpaper
for monitor in $monitors; do
    # Get random wallpaper and position
    wallpaper=$(ls $WALLPAPER_DIR | shuf -n 1)
    position=${POSITIONS[$RANDOM % ${#POSITIONS[@]}]}
    
    # Set wallpaper for current monitor
    swww img --outputs $monitor \
             --transition-type "grow" \
             --transition-pos $position \
             "$WALLPAPER_DIR/$wallpaper"
done
