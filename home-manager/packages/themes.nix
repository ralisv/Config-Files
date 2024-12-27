{ pkgs, ... }:

{
  home.packages = with pkgs; [
    libsForQt5.qt5ct # Qt theme manager
    catppuccin-qt5ct # Qt theme
    nwg-look # GTK theme manager
  ];
}
