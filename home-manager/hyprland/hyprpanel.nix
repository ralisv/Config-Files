{ hyprpanel, ... }:

{
  imports = [ hyprpanel.homeManagerModules.hyprpanel ];

  programs.hyprpanel = {
    enable = true;
  };
}
