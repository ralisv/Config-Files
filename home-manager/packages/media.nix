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
    librewolf

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
