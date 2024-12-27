{ pkgs, ... }:

{
  home.packages = with pkgs; [
    webcord
    discord
    teams-for-linux
    signal-desktop
    thunderbird
  ];
}
