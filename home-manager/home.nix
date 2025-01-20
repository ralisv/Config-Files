{ config, pkgs, ... }:

{
  imports = [
    ./hyprland/hyprland.nix
    ./programs/ghostty.nix
    ./programs/lsd.nix
    ./programs/alacritty.nix
    ./programs/bat.nix
    ./programs/freetube.nix
    ./programs/git.nix
    ./programs/micro.nix
    ./programs/vscode.nix
    ./shell/shell.nix
    ./packages/development.nix
    ./packages/drivers.nix
    ./packages/media.nix
    ./packages/tools.nix
    ./packages/social.nix
    ./packages/themes.nix
    ./packages/others.nix
  ];

  nixpkgs.config.allowUnfree = true;

  home.username = "ralis";
  home.homeDirectory = "/home/ralis";

  home.stateVersion = "24.05"; # Don't modify

  gtk = {
    enable = true;
    theme = {
      name = "Sweet-Dark-v40";
    };
    cursorTheme = {
      name = "Saturn";
      size = 25;
    };
  };

  home.file = { };

  home.sessionVariables = {
    EDITOR = "micro";
  };

  # Let Home Manager install and manage itself.
  programs.home-manager.enable = true;
}
