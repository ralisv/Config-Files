{ config, lib, pkgs, ... }:

{
  security.sudo.wheelNeedsPassword = false;
  
  imports =
    [ # Include the results of the hardware scan.
      ./hardware-configuration.nix
      (let rev = "main"; in import (builtins.fetchTarball {
        url = "https://gitlab.com/VandalByte/darkmatter-grub-theme/-/archive/${rev}/darkmatter-grub-theme-${rev}.tar.gz";
        sha256 = "1i6dwmddjh0cbrp6zgafdrji202alkz52rjisx0hs1bgjbrbwxdj";
        }))
    ];

  programs = {
    light.enable = true;
    git.enable = true;
    hyprland = {
      enable = true;
      enableNvidiaPatches = true;
      xwayland.enable = true;
    };
    xwayland.enable = true;
  };

  hardware.bluetooth.enable = true;

  hardware.opengl.enable =  true;
  hardware.nvidia.modesetting.enable = true;

  environment.systemPackages = with pkgs; [
    # Useful applications
    brave
    xonsh
    vlc
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

    # Development
    dotnet-sdk_6
    python3
    libgccjit
    cmake
    godot_4
    vscode-fhs

    # Utility for file type convertions
    texlive.combined.scheme-full
    pandoc

    # System utilities
    brightnessctl
    bluetooth_battery
    bluez
    pipewire
    pavucontrol
    wayland-utils
    bash-completion
    man-pages
  ];

  xdg.portal.enable = true;
  xdg.portal.extraPortals = [ pkgs.xdg-desktop-portal-gtk ];
  
  nix.settings.experimental-features = [ "nix-command" "flakes" ];

  services.udev.extraRules = ''
  # Regular legions
  SUBSYSTEM=="usb", ATTR{idVendor}=="048d", ATTR{idProduct}=="c965", MODE="0666"
  '';

  documentation = {
    enable = true;
    dev.enable = true;
    man.enable = true;
    nixos.enable = true;
  };

  boot = {
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
  # networking.wireless.enable = true;  # Enables wireless support via wpa_supplicant.

  # Configure network proxy if necessary
  # networking.proxy.default = "http://user:password@proxy:port/";
  # networking.proxy.noProxy = "127.0.0.1,localhost,internal.domain";

  # Enable networking
  networking.networkmanager.enable = true;

  environment.sessionVariables = {
    WLR_NO_HARDWARE_CURSORS = "1";
    # As of now, it's causing problems, not worth the optimization
    NIXOS_OZONE_WL = "0";
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

  # Enable CUPS to print documents.
  services.printing.enable = true;

  nixpkgs.config.pulseaudio = true;

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
    jack.enable = true;
    wireplumber.enable = true;
  };

  hardware.i2c.enable = true;
  services.illum.enable = true;
  hardware.acpilight.enable = true;

  # Enable touchpad support (enabled default in most desktopManager).
  # services.xserver.libinput.enable = true;

  users.users.ralis = {
    isNormalUser = true;
    description = "Vojtech Ralis";
    extraGroups = [ "networkmanager" "wheel" "video" "audio" "jackaudio" ];
    packages = with pkgs; [
      python3Packages.gitpython
      python3Packages.colorama
      python3Packages.tabulate
      python3Packages.jupyter
      python3Packages.jupyter-core
    ];
  };

  nix.gc.automatic = true;
  nix.gc.dates = "weekly";
  nix.gc.options = "--delete-older-than 7d";

  nix.optimise.automatic = true;
  
  # Allow unfree packages
  nixpkgs.config.allowUnfree = true;

  system.stateVersion = "23.05";
}
