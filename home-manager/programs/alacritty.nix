{
  programs.alacritty = {
    enable = true;
    settings = {
      colors.primary = {
        background = "0x000000";
      };
      cursor.style = {
        blinking = "Always";
        shape = "Beam";
      };
      font = {
        size = 9;
        normal.family = "FiraCode Nerd Font Ret";
        normal.style = "Retina";
        bold.family = "FiraCode Nerd Font";
        bold.style = "Bold";
        italic.family = "FiraCode Nerd Font";
        italic.style = "Italic";
      };
      scrolling = {
        history = 10000;
        multiplier = 1;
      };
      terminal.shell = {
        args = [ "-c" "xonsh" ];
        program = "bash";
      };
      window = {
        opacity = 0.7;

        title = "Alacritty";
        dynamic_title = true;

        padding = {
          x = 8;
          y = 8;
        };
        position = {
          x = 100;
          y = 100;
        };
      };
    };
  };
}
