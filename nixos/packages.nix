{ pkgs, ... }:

{
  environment.systemPackages = with pkgs; [
    # Useful applications
    brave
    firefox
    xonsh
    vlc
    mpv # Video players
    alacritty # Terminal emulator
    pinta # Image editor
    flameshot # Screenshot tool
    discord
    webcord-vencord # Discord frontend for Wayland
    bat # Better cat
    tree
    micro
    joplin-desktop
    libreoffice
    franz
    coreutils
    teams-for-linux
    unzip
    zip
    timer # CLI timer
    gnome.cheese # Webcam
    translate-shell # CLI translator
    qbittorrent # Torrent client
    gparted # For imaging USB drives
    dolphin # File manager
    eza # Better ls
    okular # PDF viewer
    caprine-bin # Facebook Messenger
    zoxide # cd improved

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
    btop
    stacer # System monitoring
    home-manager # For managing some dotfiles

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
    hyprpaper
    swww # Wallpaper manager
    mako
    libnotify # Notifications
    wluma # Brightness auto-adjust
    grimblast # Screenshot tool
    gimp # Image editing
    eww # Widgets
    wlogout # Logout menu
    tokyo-night-gtk
    webcord-vencord # Discord
    libsForQt5.polkit-kde-agent


    # SDDM themes
    sddm-chili-theme
    where-is-my-sddm-theme
    catppuccin-sddm-corners
  ];
}
