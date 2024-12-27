{ pkgs, ... }:

{
  home.packages = with pkgs; [
    (xonsh.override
      {
        extraPackages = ps: [
          ps.tabulate
          ps.types-tabulate
          ps.wheel
          ps.prompt-toolkit
          ps.pygments
        ];
      })
  ];

  home.file.".local/share/xonsh/xonsh_utils".source = ./xonsh_utils;
  home.file.".xonshrc".source = ./xonsh_conf.py;
}
