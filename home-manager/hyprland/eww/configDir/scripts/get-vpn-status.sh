#!/usr/bin/env bash

# Run the mullvad status command and capture its output
status_output=$(mullvad status)

# Extract the last line of the output
last_line=$(echo "$status_output" | tail -n 1)

# Check if the last line contains a colon
if [[ $last_line == *":"* ]]; then
    # If it does, print everything after the first colon
    echo "${last_line#*:}" | xargs
else
    # If it doesn't, print the whole line
    echo "$last_line"
fi
