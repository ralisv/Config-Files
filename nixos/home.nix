{ pkgs, ... }:

{
  programs.git = {
    enable = true;
    userName = "Vojtěch Rališ";
    userEmail = "ralis.vojtech@email.cz";
  };
}
