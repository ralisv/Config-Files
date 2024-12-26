{ config, lib, pkgs, ... }:

{
  security.sudo.wheelNeedsPassword = false;
  security.polkit.enable = true;

  imports = [
    ./hardware-configuration.nix
    (
      let rev = "main"; in import (builtins.fetchTarball {
        url = "https://gitlab.com/VandalByte/darkmatter-grub-theme/-/archive/${rev}/darkmatter-grub-theme-${rev}.tar.gz";
        sha256 = "1i6dwmddjh0cbrp6zgafdrji202alkz52rjisx0hs1bgjbrbwxdj";
      })
    )
    ./packages.nix
  ];

  programs = {
    light.enable = true;
    git.enable = true;
    xwayland.enable = true;
    hyprland = {
      enable = true;
      xwayland.enable = true;
      portalPackage = pkgs.xdg-desktop-portal-hyprland;
    };
    npm.enable = true;
    steam.enable = true;
    cfs-zen-tweaks.enable = true;
  };

  xdg.portal = {
    enable = true;
    extraPortals = [ pkgs.xdg-desktop-portal-gtk ];
  };

  services = {
    illum.enable = true; # Map brightness keys

    mullvad-vpn = {
      enable = true;
      package = pkgs.mullvad-vpn.overrideAttrs (finalAttrs: prevAttrs: rec {
        version = "2024.5";
        platform = "amd64";
        src = pkgs.fetchurl {
          url = "https://github.com/mullvad/mullvadvpn-app/releases/download/${version}/MullvadVPN-${version}_${platform}.deb";
          hash = "sha256-2d4l5BIjXQaaKOUkK+pZYsECVnyK6zOx0NkuCy9jx5I=";
        };
      });
    };

    pipewire = {
      enable = true;
      alsa.enable = true;
      alsa.support32Bit = true;
      audio.enable = true;
      pulse.enable = true;
      wireplumber = {
        enable = true;
        extraConfig = {
          "10-bluez" = {
            "monitor.bluez.properties" = {
              "bluez5.default-profile" = "a2dp-sink";
              "bluez5.a2dp.default.audio-info" = "format=S16LE rate=48000 channels=2";
              "bluez5.a2dp.default.buffer-size" = 1024;

              "bluez5.codecs" = [ "sbc_xq" "aac" "ldac" "aptx" "aptx_hd" ];
              "bluez5.roles" = [ "hsp_hs" "hsp_ag" "hfp_hf" "hfp_ag" ];

              "bluez5.enable-hw-volume" = true;
            };
            "11-bluetooth-policy" = {
              "wireplumber.settings" = {
                "bluetooth.autoswitch-to-headset-profile" = true;
              };
            };
          };
        };
      };
    };
    power-profiles-daemon.enable = false;
    upower.enable = true;

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

        START_CHARGE_THRESH_BAT0 = 70; # 70 and bellow it starts to charge
        STOP_CHARGE_THRESH_BAT0 = 85; # 80 and above it stops charging
      };
    };



    xserver = {
      videoDrivers = [ "nvidia" ];
      enable = false;
      desktopManager.plasma5.enable = true;
    };
  };

  hardware.bluetooth = {
    enable = true;
    powerOnBoot = true;
  };

  hardware.graphics = {
    enable = true;
    enable32Bit = true;
  };

  hardware.nvidia = {
    open = false;
    package = config.boot.kernelPackages.nvidiaPackages.stable;
    modesetting.enable = true;
    nvidiaSettings = true;
    prime = {
      amdgpuBusId = "PCI:5:0:0";
      nvidiaBusId = "PCI:1:0:0";
      offload = {
        enable = true;
        enableOffloadCmd = true;
      };
    };
  };

  nix.settings.experimental-features = [ "nix-command" "flakes" ];

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
    WLR_NO_HARDWARE_CURSORS = "1";
    NIXOS_OZONE_WL = "1";
    QT_QPA_PLATFORMTHEME = "qt5ct";
    QT_QPA_PLATFORM = "wayland";
    ELECTRON_OZONE_PLATFORM_HINT = "auto";
    ELECTRON_ENABLE_LOGGING = "true";
    GDK_BACKEND = "wayland";
  };

  nixpkgs.config.qt5 = {
    enable = true;
    platformTheme = "qt5ct";
    style = {
      package = pkgs.utterly-nord-plasma;
      name = "Utterly Nord Plasma";
    };
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

  # Enable sound with pipewire.
  hardware.pulseaudio.enable = false;
  security.rtkit.enable = true;

  hardware.i2c.enable = true;
  hardware.acpilight.enable = true;

  # Necessary to make swaylock work
  security.pam.services.swaylock = { };

  users.users.ralis = {
    isNormalUser = true;
    description = "Vojtech Ralis";
    extraGroups = [ "networkmanager" "wheel" "video" "audio" "jackaudio" "dialout" "bluetooth" "lp" "docker" ];
  };

  nix.gc = {
    automatic = true;
    dates = "quarterly";
    options = "--delete-older-than 30d";
  };

  nix.optimise.automatic = true;
  nix.settings = {
    auto-optimise-store = true;

    substituters = [
      "https://cache.nixos.org"
      "https://cuda-maintainers.cachix.org"
    ];
    trusted-public-keys = [
      "cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY="
      "cuda-maintainers.cachix.org-1:0dq3bujKpuEPMCX6U4WylrUDZ9JyUG0VpVZa7CNfq5E="
    ];
  };

  # Allow unfree packages
  nixpkgs.config.allowUnfree = true;

  boot = {
    supportedFilesystems = [ "ntfs" ];

    tmp.useTmpfs = true;

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

  virtualisation.docker.enable = true;
  virtualisation.docker.rootless = {
    enable = true;
    setSocketVariable = true;
  };

  boot.extraModulePackages = with config.boot.kernelPackages; [ lenovo-legion-module ];

  system.stateVersion = "24.05";

  xdg.mime.defaultApplications = {
    "text/plain" = "micro.desktop";
    "application/pdf" = "org.kde.okular.desktop";
    "text/html" = "brave-browser.desktop";
    "application/x-shellscript" = "code.desktop";
    "image/png" = "org.kde.okular.desktop";
    "audio/mpeg" = "org.kde.okular.desktop";
    "application/octet-stream" = "micro";
  };
}
