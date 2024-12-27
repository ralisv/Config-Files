{ pkgs, ... }:

{
  home.packages = with pkgs; [
    # File explorers
    dolphin
    (nnn.override {
      withNerdIcons = true;
    })
    nemo

    # Browsers
    brave
    mullvad-browser

    # PDF readers
    okular
    evince

    # Mediaplayers
    vlc

    # File editors
    libreoffice
    gimp # Image editing
    cheese # Webcam

  ];
}
