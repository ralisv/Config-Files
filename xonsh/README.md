# Xonsh
This directory contains all configuration files for xonsh shell

## .xonshrc
Xonsh's startup file, modifies shell's behavior, appearance, implements new commands and prompt

## utils.py
Provides useful utilities

### remove
Moves files from arguments into trash bin directory, prints statuses of operation

### super_util
This is supposed to be used instead of traditional ls or git status, see for yourself what it does

## colors.py
Module which handles coloring

## trash.py
Module which implements trash management

### dump
Is called in certain intervals if the user wishes it, removes old untouched removed files from trash bin
