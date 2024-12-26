#!/usr/bin/env bash

output=$(df -h / | tail -1)

total=$(echo $output | awk '{print $2}')
available=$(echo $output | awk '{print $4}')
percent_used=$(echo $output | awk '{print $5}')

percent_free=$((100 - ${percent_used%\%}))

echo "$percent_free% free, $available / $total"