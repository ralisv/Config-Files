{
  config,
  lib,
  pkgs,
  ...
}:

{

  imports = [
    ./hardware-configuration.nix
    <nixos-hardware/lenovo/legion/16ach6h>
    (
      let
        rev = "main";
      in
      import (
        builtins.fetchTarball {
          url = "https://gitlab.com/VandalByte/darkmatter-grub-theme/-/archive/${rev}/darkmatter-grub-theme-${rev}.tar.gz";
          sha256 = "1i6dwmddjh0cbrp6zgafdrji202alkz52rjisx0hs1bgjbrbwxdj";
        }
      )
    )
  ];

  programs = {
    cfs-zen-tweaks.enable = true;
  };

  services = {
    illum.enable = true; # Map brightness keys

    mullvad-vpn.enable = true;

    pipewire = {
      enable = true;
      alsa.enable = true;
      alsa.support32Bit = true;
      audio.enable = true;
      pulse.enable = true;
      wireplumber.enable = true;
    };

    tlp = {
      enable = true;
      settings = {
        CPU_SCALING_GOVERNOR_ON_AC = "performance";
        CPU_SCALING_GOVERNOR_ON_BAT = "powersave";

        CPU_ENERGY_PERF_POLICY_ON_BAT = "power";
        CPU_ENERGY_PERF_POLICY_ON_AC = "performance";

        CPU_MIN_PERF_ON_AC = 0;
        CPU_MAX_PERF_ON_AC = 100;
        CPU_MIN_PERF_ON_BAT = 0;
        CPU_MAX_PERF_ON_BAT = 40;
      };
    };
  };

  hardware = {
    bluetooth = {
      enable = true;
      powerOnBoot = true;
    };

    graphics = {
      enable = true;
      enable32Bit = true;
    };

    i2c.enable = true;
    acpilight.enable = true;
  };

  documentation = {
    enable = true;
    dev.enable = true;
    man.enable = true;
    nixos.enable = true;
    doc.enable = true;
  };

  fonts = {
    enableDefaultPackages = true;
    packages = with pkgs; [
      ubuntu_font_family
      nerd-fonts.fira-code
    ];
    fontconfig = {
      defaultFonts = {
        serif = [ "FiraCode Nerd Font" ];
        sansSerif = [ "FiraCode Nerd Font" ];
        monospace = [ "FiraCode Nerd Font Mono Ret" ];
      };
    };
    fontDir.enable = true;
  };

  networking.hostName = "nixos"; # Define your hostname.

  networking.networkmanager.enable = true;

  environment.sessionVariables = {
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

  users.users.ralis = {
    isNormalUser = true;
    description = "Vojtech Ralis";
    extraGroups = [
      "networkmanager"
      "wheel"
      "video"
      "audio"
      "jackaudio"
      "dialout"
      "bluetooth"
      "lp"
      "docker"
    ];
  };

  nix = {
    gc = {
      automatic = true;
      dates = "quarterly";
      options = "--delete-older-than 30d";
    };
    optimise.automatic = true;

    settings = {
      auto-optimise-store = true;
      experimental-features = [
        "nix-command"
        "flakes"
      ];

      substituters = [
        "https://cache.nixos.org"
        "https://cuda-maintainers.cachix.org"
      ];
      trusted-public-keys = [
        "cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY="
        "cuda-maintainers.cachix.org-1:0dq3bujKpuEPMCX6U4WylrUDZ9JyUG0VpVZa7CNfq5E="
      ];
    };
  };
  nixpkgs.config.allowUnfree = true;

  boot = {
    supportedFilesystems = [ "ntfs" ];
    extraModulePackages = with config.boot.kernelPackages; [ lenovo-legion-module ];
    tmp.useTmpfs = true;

    loader = {
      # systemd-boot.enable = true;
      efi.canTouchEfiVariables = true;
      grub = {
        enable = true;
        device = "nodev";
        darkmatter-theme = {
          enable = true;
          style = "nixos";
          icon = "color";
          resolution = "1440p";
        };
        efiSupport = true;
        useOSProber = true;
      };
    };
  };

  virtualisation.docker = {
    enable = true;
    rootless = {
      enable = true;
      setSocketVariable = true;
    };
  };

  system.stateVersion = "24.05";

  security = {
    sudo.wheelNeedsPassword = false;
    polkit.enable = true;
    rtkit.enable = true;

    # Enable lock screen authentication
    pam.services.hyprlock = { };
  };
}
