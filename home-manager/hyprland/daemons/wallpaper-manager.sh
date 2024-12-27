#!/usr/bin/env bash

swww-daemon 2>/dev/null

while true; do
    ./pick-random-wallpaper.sh
    sleep 1800
done
