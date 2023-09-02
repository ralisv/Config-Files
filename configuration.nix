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
  };
  
  environment.systemPackages = with pkgs; [
    brave
    python3
    python3Packages.gitpython
    python3Packages.colorama
    python3Packages.tabulate
  	xonsh
    vscode
    vlc
    alacritty
    cmake
    libgccjit
  ];
  
  boot.loader = {
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

  fonts = {
    enableDefaultFonts = true;
    fonts = with pkgs; [
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
    displayManager.sddm.enable = true;
    desktopManager.plasma5.enable = true;
    layout = "cz";
    xkbVariant = "";
  };
 
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
    pulse.enable = true;
    # If you want to use JACK applications, uncomment this
    #jack.enable = true;
  };

  # Enable touchpad support (enabled default in most desktopManager).
  # services.xserver.libinput.enable = true;

  # Define a user account. Don't forget to set a password with ‘passwd’.
  users.users.ralis = {
    isNormalUser = true;
    description = "Vojtech Ralis";
    extraGroups = [ "networkmanager" "wheel" ];
    packages = with pkgs; [];
  };

  # Allow unfree packages
  nixpkgs.config.allowUnfree = true;

  system.stateVersion = "23.05";
}
