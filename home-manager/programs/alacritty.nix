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
        dynamic_title = true;
        opacity = 0.7;
        title = "Alacritty";
        class = {
          general = "Alacritty";
          instance = "Alacritty";
        };
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
