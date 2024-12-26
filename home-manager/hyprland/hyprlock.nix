{ pkgs-pinned-hypr, ... }:

{
  programs.hyprlock = {
    enable = true;
    settings = {
      background = [
        {
          color = "rgba(0, 0, 0, 1.0)";
          path = "screenshot";
          blur_passes = 3;
          blur_size = 3;
          brightness = 0.4;
          contrast = 1;
          noise = 0;
        }
      ];

      input-field = [
        {
          size = "200, 50";
          position = "0, 0";
          monitor = "";
          halign = "center";
          valign = "center";
          fade_on_empty = true;
          fade_timeout = 500;
          fail_transition = 500;
          font_color = "rgba(216, 194, 191, 1.0)";
          inner_color = "rgba(19, 15, 15, 0.067)";
          outer_color = "rgba(160, 140, 137, 0.333)";
          outline_thickness = 10;
          dots_size = 0.4;
          dots_spacing = 0.3;
          dots_fade_time = 400;
        }
      ];

      label = [
        {
          monitor = "";
          text = "cmd[update:10000] date \"+%A %d. %m.\"";
          color = "rgba(237, 224, 222, 1.0)";
          font_size = 20;
          font_family = "FiraCode Nerd Font Mono Med";
          position = "0, 100";
          halign = "center";
          valign = "center";
        }
        {
          monitor = "";
          text = "$TIME";
          color = "rgba(237, 224, 222, 1.0)";
          font_size = 65;
          font_family = "FiraCode Nerd Font Mono Med";
          position = "0, 180";
          halign = "center";
          valign = "center";
        }
        {
          monitor = "";
          text = "cmd[update:5000] $HOME/Config-Files/hyprland/scripts/get-battery-status.sh";
          color = "rgba(237, 224, 222, 1.0)";
          font_size = 14;
          font_family = "FiraCode Nerd Font Mono Med";
          position = "30, -30";
          halign = "left";
          valign = "top";
        }
      ];

    };

  };
}
