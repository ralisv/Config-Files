{ pkgs-pinned-hypr, ... }:

{
  programs.hyprlock = {
    enable = true;
    settings = { }; # Generated settings file crashes hyprlock, use manual config for now
  };
}
