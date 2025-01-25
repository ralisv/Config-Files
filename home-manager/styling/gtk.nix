{ pkgs, ... }:

{
  gtk = {
    enable = true;
    theme = {
      name = "catppuccin-mocha-lavender-standard+black";
      package = pkgs.catppuccin-gtk.override {
        accents = [ "lavender" ];
        tweaks = [ "black" ];
        size = "standard";
        variant = "mocha";
      };
    };

    cursorTheme = {
      name = "Saturn";
      size = 24;
    };
  };
}
