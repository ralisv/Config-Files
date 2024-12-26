{ pkgs, ... }:

{
  programs.bat = {
    enable = true;
    config = {
      pager = "never";
      style = "header,changes";
      theme = "darkneon";
    };

    themes = {
      darkneon = {
        src = pkgs.fetchFromGitHub {
          owner = "RainyDayMedia";
          repo = "DarkNeon";
          rev = "master";
          sha256 = "sha256-J3jddEM8qLDtzlG4an7pEDyXcCpeeJvM3uqEnbUVGhc=";
        };
        file = "DarkNeon.tmTheme";
      };
    };

    extraPackages = with pkgs.bat-extras; [ batman ];
  };
}
