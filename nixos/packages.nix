{ pkgs, ... }:

{
  environment.systemPackages = with pkgs; [
    # Useful applications
    brave
    firefox
    xonsh
    vlc
    mpv # Video players
    alacritty
    pinta
    flameshot
    discord
    bat
    tree
    micro
    joplin-desktop
    libreoffice
    franz
    coreutils
    teams-for-linux
    unzip
    zip
    timer
    gnome.cheese
    translate-shell
    qbittorrent
    gparted # For imaging USB drives
    dolphin
    polkit-kde-agent

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

    # Utility for file type convertions
    texlive.combined.scheme-full
    pandoc

    # System utilities
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
    hyprpaper # Wallpaper manager
    mako
    libnotify # Notifications
    wluma # Brightness auto-adjust
    grimblast # Screenshot tool
    gimp # Image editing
    eww-wayland # Widgets
    wlogout # Logout menu
  ];
}
