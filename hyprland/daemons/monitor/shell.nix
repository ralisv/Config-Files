{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    (pkgs.python312.withPackages (ps: [ ps.pydantic ]))
  ];

  shellHook = ''
    echo "Executing sysmonitor.py..."
    python3.12 sysmonitor.py
    exit 0
  '';
}
