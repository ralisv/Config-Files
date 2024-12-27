{ pkgs-pinned-hypr, ... }:

{
  programs.hyprlock = {
    enable = true;
    settings = {
      background = [
        {
          color = "rgb(15, 15, 15)";
        }
      ];

      input-field = {
        monitor = "";
        size = "200, 50";
        outline_thickness = 10;
        dots_size = 0.4;
        dots_spacing = 0.3;

        dots_fade_time = 400;
        fade_timeout = 500;
        fade_on_empty = true;
        fail_transition = 500;

        outer_color = "rgb(160,140,137)";
        inner_color = "rgb(19,15,15)";
        font_color = "rgb(216,194,191)";

        position = "0, 0";
        halign = "center";
        valign = "center";
      };

      label = [
        {
          monitor = "";
          text = "cmd[update:10000] date \"+%A %d. %m.\"";
          color = "rgb(237,224,222)";
          font_size = 20;
          font_family = "FiraCode Nerd Font Mono Med";

          position = "0, 100";
          halign = "center";
          valign = "center";
        }
        {
          monitor = "";
          text = "$TIME";
          color = "rgb(237,224,222)";
          font_size = 65;
          font_family = "FiraCode Nerd Font Mono Med";

          position = "0, 180";
          halign = "center";
          valign = "center";
        }
        {
          monitor = "";
          text = "cmd[update:2000] ~/Config-Files/home-manager/hyprland/eww/configDir/scripts/get-battery-status.sh";
          color = "rgb(237,224,222)";
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
