{ pkgs, ... }:

{
  environment.systemPackages = with pkgs; [
    # Web browsers
    brave
    librewolf-wayland

    # Mediaplayers
    vlc
    gnome.totem

    # Essential tools, utilities and applications
    alacritty # Terminal emulator
    libreoffice
    coreutils
    unzip
    zip
    gparted # For imaging USB drives
    brightnessctl
    pavucontrol
    wayland-utils
    bash-completion
    xdg-utils
    nethogs # For application network activity monitoring
    ntfs3g # For NTFS support
    networkmanagerapplet
    acpi
    wlsunset # For screen temperature adjustment
    btop
    htop
    stacer # System monitoring
    home-manager # For managing some dotfiles

    # Useful applications
    pinta # Image editor
    flameshot # Screenshot tool
    discord
    webcord-vencord # Discord frontend for Wayland
    qbittorrent # Torrent client
    teams-for-linux
    okular # PDF viewer
    evince # Alternative PDF viewer
    caprine-bin # Facebook Messenger
    gnome.cheese # Webcam

    # Shell utilities
    xonsh
    zoxide # cd improved
    timer # CLI timer
    bat # Better cat
    tree
    micro
    eza # Better ls
    translate-shell # CLI translator

    # File managers
    dolphin
    (nnn.override { withNerdIcons = true; })
    cinnamon.nemo

    # Development
    dotnet-sdk_6
    python312Full
    libgccjit
    cmake
    godot_4
    vscode-fhs
    nixpkgs-fmt
    zulu8 # Java 8, for Digital executable
    arduino
    man-pages
    ghc
    cargo
    rustc
    docker
    docker-compose

    # Utility for file type convertions
    texlive.combined.scheme-full
    pandoc

    # Python packages
    python312Packages.tabulate
    python312Packages.types-tabulate
    python312Packages.wheel
    python312Packages.prompt-toolkit
    python312Packages.pygments

    python311Packages.jupyter
    python311Packages.jupyter-core
    python311Packages.scipy
    python311Packages.numpy

    # Useful things for Hyprland
    swww # Wallpaper manager
    mako # Notifications daemon
    libnotify # Notifications
    wluma # Brightness auto-adjust
    grimblast # Screenshot tool
    gimp # Image editing
    eww # Widgets
    wlogout # Logout menu
    libsForQt5.polkit-kde-agent
    hyprlock # Lock screen
    hypridle # Idle manager
    nwg-look # GTK theme
    hyprpicker # Color picker
    wl-clipboard # Clipboard manager
  ];
}
