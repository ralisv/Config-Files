#!/usr/bin/env bash

EWW=`which eww`
CFG="$HOME/Config-Files/hyprland/eww"

## Run eww daemon if not running already
if [[ ! `pidof eww` ]]; then
	${EWW} daemon
	sleep 1
fi

## Open widgets 
run_eww() {
	${EWW} --config "$CFG" open info
}

## Launch or close widgets accordingly
run_eww
