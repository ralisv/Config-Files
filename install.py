#!/usr/bin/env python3


import os
import platform
import sys

if platform.system() == "Linux":
    print("Linux system detected")

    INSTALL_SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(sys.argv[0]))
    USER_HOME_DIRECTORY = os.path.expanduser("~")

    SOURCE_TO_DESTINATION_SYMLINK_MAPPING = {
        f"{INSTALL_SCRIPT_DIRECTORY}/.bashrc": f"{USER_HOME_DIRECTORY}/.bashrc",
        f"{INSTALL_SCRIPT_DIRECTORY}/xonsh/.xonshrc": f"{USER_HOME_DIRECTORY}/.xonshrc",
        f"{INSTALL_SCRIPT_DIRECTORY}/.inputrc": f"{USER_HOME_DIRECTORY}/.inputrc",
        f"{INSTALL_SCRIPT_DIRECTORY}/vs-code/settings.json": f"{USER_HOME_DIRECTORY}/.config/Code/User/settings.json",
        f"{INSTALL_SCRIPT_DIRECTORY}/vs-code/keybindings.json": f"{USER_HOME_DIRECTORY}/.config/Code/User/keybindings.json",
        f"{INSTALL_SCRIPT_DIRECTORY}/alacritty.yml": f"{USER_HOME_DIRECTORY}/.config/alacritty/alacritty.yml",
        f"{INSTALL_SCRIPT_DIRECTORY}/nixos/shell.nix": f"{USER_HOME_DIRECTORY}/shell.nix",
        f"{INSTALL_SCRIPT_DIRECTORY}/nixos/flake.nix": f"{USER_HOME_DIRECTORY}/flake.nix",
        f"{INSTALL_SCRIPT_DIRECTORY}/micro/settings.json": f"{USER_HOME_DIRECTORY}/.config/micro/settings.json",
        f"{INSTALL_SCRIPT_DIRECTORY}/micro/bindings.json": f"{USER_HOME_DIRECTORY}/.config/micro/bindings.json",
    }

    for source, destination in SOURCE_TO_DESTINATION_SYMLINK_MAPPING.items():
        if not os.path.exists(source):
            print(f"Source path {source} does not exist")
            continue

        if os.path.exists(destination):
            print(f"Path {destination} already exists")
            continue

        if not os.path.exists(os.path.dirname(destination)):
            print(f"Creating directory {os.path.dirname(destination)}")
            os.makedirs(os.path.dirname(destination))

        print(f"Creating symlink {destination} -> {source}")
        os.symlink(source, destination)
