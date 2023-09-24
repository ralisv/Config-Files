# NixOS configuration

This file contains all configuration files for NixOS operating system,
## configuration.nix
configuration.nix is the file which configures operating system, it must be copied into /etc/nixos directory.
## shell.nix
contains an expression which should be activated in each instance of terminal if you plan to use my xonsh
configuration on NixOS machine, this is because you can not install python packages globally.
## flake.nix
currently experimental, to optimize what shell.nix does
