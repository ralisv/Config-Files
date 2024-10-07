#!/usr/bin/env bash

EWW=`which eww`

## Run eww daemon if not running already
if [[ ! `pidof eww` ]]; then
	${EWW} daemon
	sleep 1
fi

${EWW} --config=$HOME/Config-Files/hyprland/eww open info
