{ pkgs, ... }:

{
  home.packages = with pkgs; [
    # File explorers
    (nnn.override {
      withNerdIcons = true;
    })
    nemo

    # Browsers
    brave
    mullvad-browser

    # PDF readers
    okular

    # Mediaplayers
    vlc

    # File editors
    libreoffice
    gimp # Image editing
    cheese # Webcam
  ];
}
