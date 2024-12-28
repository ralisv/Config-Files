{ pkgs, ... }:

{
  imports = [ ./xonsh/xonsh.nix ];

  home.file.".config/ls-colors/ls-colors.txt".source = ./ls-colors.txt;
  home.file.".inputrc".source = ./.inputrc;

  home.packages = with pkgs; [
    zoxide
    bash-completion
  ];
}
