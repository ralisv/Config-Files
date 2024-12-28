{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    (pkgs.python312.withPackages (ps: [ ps.pydantic ]))
  ];

  shellHook = ''
    python3.12 ~/.config/hypr/daemons/monitor/sysmonitor.py > ~/.local/share/sysmonitor.log.txt
    exit 0
  '';
}
