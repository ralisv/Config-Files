{ pkgs, ... }:

{
  environment.systemPackages = with pkgs;
    [
      # Web browsers
      brave
      mullvad-browser

      # Mediaplayers
      vlc

      # PDF readers
      okular
      evince

      # Essential tools, utilities and applications
      libreoffice
      coreutils
      unzip
      zip
      gparted # For imaging USB drives
      brightnessctl
      pavucontrol # Audio control
      pulseaudio # CLI tools for audio
      wayland-utils
      xdg-utils
      ntfs3g # For NTFS support
      networkmanagerapplet
      acpi
      lenovo-legion

      timer # CLI timer
      translate-shell # CLI translator
      btop
      man-pages

      # Useful applications
      discord
      webcord-vencord # Discord frontend for Wayland
      teams-for-linux
      signal-desktop
      thunderbird # Email client

      cheese # Webcam

      # Shell utilities


      # File managers
      dolphin
      (nnn.override {
        withNerdIcons = true;
      })
      nemo

      # Development
      python312Full
      nixpkgs-fmt
      ghc
      docker
      docker-compose

      # Useful python packages
      python311Packages.jupyter
      python311Packages.jupyter-core
      python311Packages.scipy
      python311Packages.numpy

      # Useful things for Hyprland


      # Theming
      libsForQt5.qt5ct # Qt theme manager
      catppuccin-qt5ct # Qt theme
      nwg-look # GTK theme manager
    ];
}
