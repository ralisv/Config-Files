{ pkgs, ... }:

{
  home.packages = with pkgs; [
    networkmanagerapplet
    pomodoro-gtk
  ];
}
