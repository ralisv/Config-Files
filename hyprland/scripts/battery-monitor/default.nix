{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python3Packages.watchdog
  ];

  shellHook = ''
    ./main.py
  '';
}
