{ config, lib, pkgs, ... }:

{
  security.sudo.wheelNeedsPassword = false;

  imports =
    [
      # Include the results of the hardware scan.
      ./hardware-configuration.nix
      (
        let rev = "main"; in import (builtins.fetchTarball {
          url = "https://gitlab.com/VandalByte/darkmatter-grub-theme/-/archive/${rev}/darkmatter-grub-theme-${rev}.tar.gz";
          sha256 = "1i6dwmddjh0cbrp6zgafdrji202alkz52rjisx0hs1bgjbrbwxdj";
        })
      )
      <home-manager/nixos>
    ];

  programs = { #
    light.enable = true;
    git.enable = true;
    xwayland.enable = true;
    hyprland.enable = true;
  };

  hardware.bluetooth = {
    enable = true;
    powerOnBoot = true;
  };


  hardware.opengl.enable = true;
  hardware.nvidia.modesetting.enable = true;

  environment.systemPackages = with pkgs; [
    # Useful applications
    brave
    firefox
    xonsh
    vlc mpv  # Video players
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
    gparted  # For imaging USB drives
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
    hyprpaper     # Wallpaper manager
    avizo         # Notifications
    wluma         # Brightness auto-adjust
    grimblast     # Screenshot tool
    gimp          # Image editing
    eww-wayland   # Widgets
  ];

  home-manager.users.ralis = {
    home.stateVersion = "23.11";
  };

  xdg.portal.enable = true;
  xdg.portal.extraPortals = [ pkgs.xdg-desktop-portal-gtk ];

  nix.settings.experimental-features = [ "nix-command" "flakes" ];

  documentation = {
    enable = true;
    dev.enable = true;
    man.enable = true;
    nixos.enable = true;
    doc.enable = true;
  };

  boot = {
    supportedFilesystems = [ "ntfs" ];

    loader = {
      # systemd-boot.enable = true;
      efi.canTouchEfiVariables = true;
      grub = {
        enable = true;
        device = "nodev";
        useOSProber = true;
        darkmatter-theme = {
          enable = true;
          style = "nixos";
          icon = "color";
          resolution = "1440p";
        };
        efiSupport = true;
      };
    };
  };

  fonts = {
    enableDefaultPackages = true;
    packages = with pkgs; [
      ubuntu_font_family
      (nerdfonts.override { fonts = [ "FiraCode" "DroidSansMono" ]; })
    ];
    fontconfig = {
      defaultFonts = {
        serif = [ "Ubuntu" ];
        sansSerif = [ "Ubuntu" ];
        monospace = [ "Ubuntu" ];
      };
    };
    fontDir.enable = true;
  };

  networking.hostName = "nixos"; # Define your hostname.

  # Enable networking
  networking.networkmanager.enable = true;

  environment.sessionVariables = {
    WLR_NO_HARDWARE_CURSORS = "1";
    NIXOS_OZONE_WL = "1";
  };

  # Set your time zone.
  time.timeZone = "Europe/Prague";

  # Select internationalisation properties.
  i18n.defaultLocale = "en_US.UTF-8";

  i18n.extraLocaleSettings = {
    LC_ADDRESS = "cs_CZ.UTF-8";
    LC_IDENTIFICATION = "cs_CZ.UTF-8";
    LC_MEASUREMENT = "cs_CZ.UTF-8";
    LC_MONETARY = "cs_CZ.UTF-8";
    LC_NAME = "cs_CZ.UTF-8";
    LC_NUMERIC = "cs_CZ.UTF-8";
    LC_PAPER = "cs_CZ.UTF-8";
    LC_TELEPHONE = "cs_CZ.UTF-8";
    LC_TIME = "cs_CZ.UTF-8";
  };

  # Enable the KDE Plasma Desktop Environment.
  services.xserver = {
    enable = true;
    displayManager.sddm = {
      enable = true;
      # theme = "Magna-SDDM";
    };
    desktopManager.plasma5.enable = true;
    layout = "cz";
    xkbVariant = "";
  };

  # For touchpad gestures
  # services.touchegg.enable = true;

  # Enable CUPS to print documents.
  services.printing.enable = true;

  # Enable sound with pipewire.
  sound.enable = true;
  hardware.pulseaudio.enable = false;
  security.rtkit.enable = true;
  services.pipewire = {
    enable = true;
    alsa.enable = true;
    alsa.support32Bit = true;
    audio.enable = true;
    pulse.enable = true;
    wireplumber.enable = true;
  };

  hardware.i2c.enable = true;
  services.illum.enable = true;
  hardware.acpilight.enable = true;

  users.users.ralis = {
    isNormalUser = true;
    description = "Vojtech Ralis";
    extraGroups = [ "networkmanager" "wheel" "video" "audio" "jackaudio" "dialout" "bluetooth" "lp" ];
  };

  nix.gc = {
    automatic = true;
    dates = "weekly";
    options = "--delete-older-than 30d";
  };

  nix.optimise.automatic = true;
  nix.settings.auto-optimise-store = true;

  # Allow unfree packages
  nixpkgs.config.allowUnfree = true;

  system.stateVersion = "23.05";
}
