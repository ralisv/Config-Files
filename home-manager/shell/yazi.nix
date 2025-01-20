{ pkgs, ... }:

{
  programs.yazi = {
    enable = true;

    theme = {
      filetype = {
        rules = [
          {
            name = "*.avi";
            fg = "#ff0000";
          }
          {
            name = "*.bmp";
            fg = "#875faf";
          }
          {
            name = "*.c";
            fg = "#00ff00";
          }
          {
            name = "*.conf";
            fg = "#00ff00";
          }
          {
            name = "*.cpp";
            fg = "#0000ff";
          }
          {
            name = "*.crdownload";
            fg = "#ff0000";
          }
          {
            name = "*.cs";
            fg = "#875faf";
          }
          {
            name = "*.deb";
            fg = "#d7d7d7";
            bold = true;
          }
          {
            name = "*.gif";
            fg = "#875faf";
          }
          {
            name = "*.gz";
            fg = "#ffff00";
            bold = true;
          }
          {
            name = "*.ipynb";
            fg = "#0000ff";
          }
          {
            name = "*.jpeg";
            fg = "#875faf";
          }
          {
            name = "*.jpg";
            fg = "#875faf";
          }
          {
            name = "*.json";
            fg = "#ffff00";
          }
          {
            name = "*.m4v";
            fg = "#ff0000";
          }
          {
            name = "*.md";
            fg = "#ff0000";
          }
          {
            name = "*.mjpeg";
            fg = "#875faf";
          }
          {
            name = "*.mjpg";
            fg = "#875faf";
          }
          {
            name = "*.mkv";
            fg = "#ff0000";
          }
          {
            name = "*.mp4";
            fg = "#ff0000";
          }
          {
            name = "*.mpeg";
            fg = "#875faf";
          }
          {
            name = "*.mpg";
            fg = "#875faf";
          }
          {
            name = "*.nix";
            fg = "#00d7ff";
            bold = true;
          }
          {
            name = "*.ogg";
            fg = "#00d7ff";
          }
          {
            name = "*.pdf";
            fg = "#875faf";
          }
          {
            name = "*.png";
            fg = "#875faf";
          }
          {
            name = "*.py";
            fg = "#00d7ff";
          }
          {
            name = "*.pyc";
            fg = "#ffff00";
          }
          {
            name = "*.rs";
            fg = "#ffff00";
          }
          {
            name = "*.tar";
            fg = "#ffff00";
            bold = true;
          }
          {
            name = "*.tif";
            fg = "#875faf";
          }
          {
            name = "*.tiff";
            fg = "#875faf";
          }
          {
            name = "*.toml";
            fg = "#00d7ff";
          }
          {
            name = "*.txt";
            fg = "#00ff00";
          }
          {
            name = "*.wav";
            fg = "#ff0000";
          }
          {
            name = "*.yml";
            fg = "#00d7ff";
          }
          {
            name = "*.zip";
            fg = "#ffff00";
            bold = true;
          }
          {
            name = "*";
            is = "block";
            fg = "#5f5f5f";
          }
          {
            name = "*";
            is = "char";
            fg = "#5f5f5f";
            bold = true;
          }
          {
            name = "*/";
            fg = "#00d7ff";
          }
          {
            name = "*";
            is = "exec";
            fg = "#00ff00";
            bold = true;
          }
          {
            name = "*";
            is = "link";
            fg = "#0000ff";
            bold = true;
          }
          {
            name = "*";
            is = "orphan";
            fg = "#ff0000";
          }
          {
            name = "*";
            is = "fifo";
            fg = "#ffff00";
          }
          {
            name = "*";
            is = "sock";
            fg = "#5f5f5f";
          }
        ];
      };
    };
  };
}
