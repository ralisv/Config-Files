{ pkgs, ... }:

{
  home.packages = with pkgs; [
    (xonsh.override {
      extraPackages = ps: [
        ps.tabulate
        ps.types-tabulate
        ps.wheel
        ps.prompt-toolkit
        ps.pygments
      ];
    })
    any-nix-shell
  ];

  home.file.".local/share/xonsh/xonsh_utils".source = ./xonsh_utils;
  home.file.".xonshrc".text = ''
    ${builtins.readFile ./xonsh_conf.py}
    source-bash ~/.nix-profile/etc/profile.d/hm-session-vars.sh
    execx ($(zoxide init xonsh), 'exec', __xonsh__.ctx, filename='zoxide')
    execx ($(any-nix-shell xonsh --info-right))
    def _y(args):
      tmp = $(mktemp -t "yazi-cwd.XXXXXX")
      args.append(f"--cwd-file={tmp}")
      $[yazi @(args)]
      with open(tmp) as f:
        cwd = f.read().strip()
      if cwd != $PWD:
        cd @(cwd)
      rmp -f -- @(tmp)

    aliases["y"] = _y
  '';
}
