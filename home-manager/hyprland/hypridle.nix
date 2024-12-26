{ ... }:

{
  services.hypridle = {
    enable = true;
    settings = {
      general = {
        lock_cmd = "pidof hyprlock || hyprlock";
        before_sleep_cmd = "pidof hyprlock || hyprlock";
      };

      listener = [
        {
          timeout = 900;
          on-timeout = "notify-send \"Screen will be locked in 30 seconds\"";
        }
        {
          timeout = 930;
          on-timeout = "pidof hyprlock || hyprlock";
        }
        {
          timeout = 1200;
          on-timeout = "hyprctl dispatch dpms off";
          on-resume = "hyprctl dispatch dpms on";
        }
        {
          timeout = 7200;
          on-timeout = "systemctl suspend";
        }
      ];
    };
  };
}

