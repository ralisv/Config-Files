{ config, pkgs, ... }:

{
  home.username = "ralis";
  home.homeDirectory = "/home/ralis";

  home.stateVersion = "23.11"; # Don't modify

  home.packages = [ ];

  gtk.enable = true;

  gtk.theme.name = "Sweet-Dark-v40";

  home.file = { };

  home.sessionVariables = {
    EDITOR = "micro";
  };

  # Let Home Manager install and manage itself.
  programs.home-manager.enable = true;
}
