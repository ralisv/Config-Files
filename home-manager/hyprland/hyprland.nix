{ pkgs, pkgs-pinned-hypr, ... }:

{
  imports = [
    ./hypridle.nix
    ./hyprlock.nix
  ];

  wayland.windowManager.hyprland = {
    enable = true;
    package = pkgs-pinned-hypr.hyprland;
    plugins = [
      pkgs-pinned-hypr.hyprlandPlugins.hyprgrass
    ];

    settings = {
      monitor = [
        "DP-1,2560x1440,0x0,auto"
        "DP-2,2560x1440,4160x800,auto"
        "eDP-1,2560x1600,2560x400,auto"
      ];

      env = [
        "XCURSOR_SIZE,35"
        "WLR_NO_HARDWARE_CURSORS,1"
        "GTK_THEME,Sweet-Dark-v40"
        "XCURSOR_THEME,LyraS-cursors"
        "XCURSOR_SIZE,26"
        "HYPRCURSOR_THEME,LyraS-cursors"
        "HYPRCURSOR_SIZE,25"
      ];

      exec-once = [
        "dbus-update-activation-environment --systemd HYPRLAND_INSTANCE_SIGNATURE"
        "hypridle"
        "~/Config-Files/hyprland/daemons/wallpaper-manager.sh"
        "~/Config-Files/hyprland/scripts/launch-eww.sh"
        "nix-shell ~/Config-Files/hyprland/daemons/monitor/shell.nix &"
        "while true; do hyprnotify --no-sound; done"
        "hyprctl setcursor LyraS-cursors 25"
        "systemctl --user start hyprpolkitagent"
        "wvkbd-mobintl --hidden"
      ];

      exec = "hyprshade auto";

      windowrulev2 = [
        "idleinhibit focus, class:(FreeTube)|(vlc)"
        "nodim, class:(vlc)|(FreeTube)"
        "noborder, fullscreen:1"
        "bordercolor rgb(aa00aa) rgb(550022), floating:1"
        "rounding 20, floating:1"
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
          enabled = false;
          size = 8;
          passes = 1;
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
        "$launchMod, N, exec, nm-applet"
        "$launchMod, T, exec, alacritty"
        "$launchMod, F, exec, freetube"
        "$launchMod, D, exec, webcord"
        "$launchMod, B, exec, brave --password-store=basic --enable-features=UseOzonePlatform --ozone-platform=wayland"
        "$launchMod, R, exec, eww reload"
        "$launchMod, M, exec, mullvad-vpn"
        "$launchMod, S, exec, signal-desktop"
        "$launchMod, C, exec, caprine"
        "$mainMod, S, exec, hyprshot --mode=region --freeze --clipboard-only"
        "$mainMod+SHIFT, S, exec, hyprshot --mode=region --freeze"
        "$mainMod, L, exec, hyprlock"
        "$mainMod, C, exec, hyprpicker -a"
        "$mainMod, Q, killactive,"
        "$mainMod+SHIFT, Q, exit,"
        "$mainMod, V, togglefloating,"
        "$mainMod, P, pin"
        "$mainMod, A, layoutmsg, addmaster"
        "$mainMod, W, layoutmsg, removemaster"
        "$mainMod, R, exec, hyprctl reload"
        "$mainMod, F, fullscreen, 1"
        "$mainMod+SHIFT, left, movefocus, l"
        "$mainMod+SHIFT, right, movefocus, r"
        "$mainMod+SHIFT, up, movefocus, u"
        "$mainMod+SHIFT, down, movefocus, d"
        "ALT, TAB, cyclenext"
        "$mainMod, left, movewindow, l"
        "$mainMod, right, movewindow, r"
        "$mainMod, up, movewindow, u"
        "$mainMod, down, movewindow, d"
        "$mainMod+ALT, right, movetoworkspace, +1"
        "$mainMod+ALT, left, movetoworkspace, -1"
        "$mainMod+ALT, up, togglefloating"
      ];

      bindm = [
        "$mainMod, mouse:272, resizewindow"
        "$mainMod, mouse:273, movewindow"
      ];

      binde = [
        ", XF86AudioRaiseVolume, exec, ~/Config-Files/hyprland/scripts/volume.sh up"
        ", XF86AudioLowerVolume, exec, ~/Config-Files/hyprland/scripts/volume.sh down"
      ];

      bindr = [
        ", XF86AudioMute, exec, ~/Config-Files/hyprland/scripts/volume.sh mute"
        ", XF86AudioMicMute, exec, ~/Config-Files/hyprland/scripts/mic.sh toggle"
      ];

      plugin.touch_gestures = {
        sensitivity = 10;
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
