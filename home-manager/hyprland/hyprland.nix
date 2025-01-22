{ pkgs, ... }:

{
  imports = [
    ./hypridle.nix
    ./hyprlock.nix
    ./eww/eww.nix
  ];
  home.file.".config/hypr/daemons".source = ./daemons;
  home.file.".config/hypr/pyprland.toml".source = ./pyprland.toml;

  home.packages = with pkgs; [
    swww # Wallpaper manager
    hyprshot # Screenshot tool
    hyprnotify # Bridge between hyprland notifications and libnotify
    libnotify # Notifications interface
    hyprpicker # Color picker
    wl-clipboard # Clipboard manager
    hyprshade # Screen shader
    wvkbd # Virtual keyboard
    xdg-desktop-portal-hyprland # Desktop portal
    hyprpolkitagent # Privilege escalation agent
    hyprsunset # Blue light filter
    pyprland # Plugins
  ];

  home.sessionVariables = {
    QT_QPA_PLATFORM = "wayland";
    QT_QPA_PLATFORMTHEME = "qt5ct";

    GDK_BACKEND = "wayland";
    GTK_THEME = "Sweet-Dark-v40";

    ELECTRON_OZONE_PLATFORM_HINT = "auto";
    WLR_NO_HARDWARE_CURSORS = "1";

    HYPRCURSOR_SIZE = "25";
    HYPRCURSOR_THEME = "saturn";

  };

  wayland.windowManager.hyprland = {
    enable = true;
    package = pkgs.hyprland;
    plugins = [
      # pkgs.hyprlandPlugins.hyprgrass
    ];

    settings = {
      monitor = [
        "DP-1,2560x1440,0x0,auto"
        "DP-2,2560x1440,4160x800,auto"
        "HDMI-A-1, 1920x1080, 2560x0, auto"
        "eDP-1,2560x1600,2560x400,auto"
      ];

      exec-once = [
        "dbus-update-activation-environment --systemd HYPRLAND_INSTANCE_SIGNATURE"
        "~/.config/hypr/daemons/wallpaper-manager.sh"
        "~/.config/hypr/daemons/blue-light-filter.py"
        "sleep 1 && cd ~/.config/hypr/daemons/monitor/ && nix-shell"
        "sleep 2 && eww open info"
        "eww daemon"
        "while true; do hyprnotify --no-sound; done"
        "hyprctl setcursor saturn 25"
        "systemctl --user start hyprpolkitagent"
        "wvkbd-mobintl --hidden"
        "hypridle"
        "pypr"
      ];

      exec = "hyprshade auto";

      windowrulev2 = [
        "idleinhibit focus, class:(FreeTube)|(vlc)"
        "nodim, class:(vlc)|(FreeTube)"
        "noborder, fullscreen:1"
        "bordercolor rgb(aa00aa) rgb(550022), floating:1"
        "rounding 20, floating:1"
        "float, class:^(com.mitchellh.ghostty.scratchpad)$"
      ];

      input = {
        kb_layout = "cz";
        kb_variant = "";
        kb_model = "";
        kb_options = "";
        kb_rules = "";
        follow_mouse = 2;

        touchpad = {
          disable_while_typing = true;
          natural_scroll = true;
          "tap-to-click" = false;
        };

        sensitivity = 0;
        accel_profile = "adaptive";
        numlock_by_default = false;
      };

      general = {
        gaps_in = 0;
        gaps_out = 0;
        gaps_workspaces = 300;
        border_size = 1;
        "col.active_border" = "rgba(bb0099aa) rgba(aa0077aa) 45deg";
        "col.inactive_border" = "rgba(222222ff) rgba(000000ff) 45deg";
        layout = "master";
        allow_tearing = false;
      };

      decoration = {
        rounding = 0;
        blur = {
          enabled = true;
          size = 3;
          passes = 3;
        };
        dim_inactive = true;
        dim_strength = 0.15;
      };

      animations = {
        enabled = true;
        bezier = "moveBezier, 0.3, 0.85, 0.01, 1.O5";
        animation = [
          "windowsMove, 1, 7, moveBezier"
          "border, 1, 15, default"
          "fade, 1, 15, default"
          "workspaces, 1, 10, moveBezier, slide"
        ];
      };

      dwindle = {
        pseudotile = true;
        preserve_split = true;
      };

      master = {
        mfact = 0.5;
        allow_small_split = true;
        new_status = "slave";
        orientation = "right";
        inherit_fullscreen = false;
        drop_at_cursor = false;
      };

      gestures = {
        workspace_swipe = true;
        workspace_swipe_forever = true;
        workspace_swipe_direction_lock = false;
      };

      "$launchMod" = "SUPER+ALT";
      "$mainMod" = "SUPER";

      bind = [
        "$launchMod, T, exec, ghostty"
        "$launchMod, F, exec, freetube"
        "$launchMod, D, exec, mullvad-exclude webcord"
        "$launchMod, B, exec, brave --password-store=basic"
        "$launchMod, R, exec, eww reload"
        "$launchMod, M, exec, mullvad-vpn"
        "$launchMod, S, exec, signal-desktop"
        "$launchMod, C, exec, mullvad-exclude caprine"
        "$launchMod, P, exec, mullvad-exclude librewolf --new-window www.perplexity.ai"
        "$launchMod, K, exec, keepassxc"
        "$launchMod, E, exec, mullvad-exclude thunderbird"

        "$mainMod, S, exec, hyprshot --mode=region --freeze --clipboard-only"
        "$mainMod+SHIFT, S, exec, hyprshot --mode=region --freeze"
        "$mainMod, C, exec, hyprpicker -a"

        "$mainMod, L, exec, hyprlock"

        "$mainMod, Q, killactive,"
        "$mainMod+SHIFT, Q, exit,"

        "$mainMod, SPACE, exec, pypr toggle term"

        "$mainMod, P, pin"
        "$mainMod, A, layoutmsg, addmaster"
        "$mainMod, W, layoutmsg, removemaster"
        "$mainMod, F, fullscreen, 1"

        "$mainMod, R, exec, hyprctl reload"
        "$mainMod+ALT, up, togglefloating"
        "$mainMod+ALT, right, movetoworkspace, +1"
        "$mainMod+ALT, left, movetoworkspace, -1"
        "$mainMod, left, movewindow, l"
        "$mainMod, right, movewindow, r"
        "$mainMod, up, movewindow, u"
        "$mainMod, down, movewindow, d"
        "$mainMod+SHIFT, left, movefocus, l"
        "$mainMod+SHIFT, right, movefocus, r"
        "$mainMod+SHIFT, up, movefocus, u"
        "$mainMod+SHIFT, down, movefocus, d"
        "ALT, TAB, layoutmsg, rollnext"
      ];

      bindm = [
        "$mainMod, mouse:272, resizewindow"
        "$mainMod, mouse:273, movewindow"
      ];

      binde = [
        ", XF86AudioRaiseVolume, exec, wpctl set-volume -l 1.5 @DEFAULT_AUDIO_SINK@ 5%+ && wpctl set-mute @DEFAULT_AUDIO_SINK@ 0"
        ", XF86AudioLowerVolume, exec, wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-"
      ];

      bindr = [
        ", XF86AudioMute, exec, wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle"
        ", XF86AudioMicMute, exec, wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle"
      ];

      plugin.touch_gestures = {
        sensitivity = 20;
        hyprgrass-bind = [
          ", swipe:4:d, exec, kill -sUSR1 $(pidof wvkbd-mobintl)"
          ", swipe:4:u, exec, kill -sUSR2 $(pidof wvkbd-mobintl)"
          ", swipe:3:u, killactive"
        ];
      };

      misc.force_default_wallpaper = 0;

      xwayland.force_zero_scaling = true;
    };
  };
}
