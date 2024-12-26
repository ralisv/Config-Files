{ pkgs, ... }:

{
  environment.systemPackages = with pkgs; [
    # Web browsers
    brave
    mullvad-browser

    # Mediaplayers
    vlc
    freetube

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
    bash-completion
    xdg-utils
    nethogs # For application network activity monitoring
    ntfs3g # For NTFS support
    networkmanagerapplet
    acpi
    btop
    htop
    stacer # System monitoring
    lenovo-legion

    # Useful applications
    discord
    webcord-vencord # Discord frontend for Wayland
    teams-for-linux
    signal-desktop
    thunderbird # Email client

    cheese # Webcam

    # Shell utilities
    zoxide # cd improved
    timer # CLI timer
    tree
    micro
    translate-shell # CLI translator

    # File managers
    dolphin
    (nnn.override { withNerdIcons = true; })
    nemo

    # Development
    python312Full
    vscode-fhs
    nixpkgs-fmt
    man-pages
    ghc
    docker
    docker-compose

    # Python packages
    python312Packages.tabulate
    python312Packages.types-tabulate
    python312Packages.wheel
    python312Packages.prompt-toolkit
    python312Packages.pygments
    python312Packages.xonsh

    python311Packages.jupyter
    python311Packages.jupyter-core
    python311Packages.scipy
    python311Packages.numpy

    # Useful things for Hyprland
    swww # Wallpaper manager
    hyprshot # Screenshot tool
    hyprnotify # Bridge between hyprland notifications and libnotify
    libnotify # Notifications interface
    gimp # Image editing
    wlogout # Logout menu
    hyprlock # Lock screen
    hypridle # Idle manager
    hyprpicker # Color picker
    wl-clipboard # Clipboard manager
    hyprshade # Screen shader
    hyprlandPlugins.hyprgrass # Touch gestures
    wvkbd # Virtual keyboard

    # Theming
    libsForQt5.qt5ct # Qt theme manager
    catppuccin-qt5ct # Qt theme
    nwg-look # GTK theme manager
  ];
}
