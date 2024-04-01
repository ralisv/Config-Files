# On NixOS, you can't install python packages globally, this nix expression must be executed in nix-shell
# where my configuration of xonsh runs properly

{ pkgs ? import <nixpkgs> { } }:

let
  my-python-packages = p: with p; [
    (buildPythonPackage rec {
      pname = "xonsh";
      version = "0.15.1";

      src = fetchPypi {
        inherit pname version;
        sha256 = "sha256-NKYzK3qG9v6Gp0JzWFxZqx88iSkv2lqer+VMkmusRxA=";
      };

      doCheck = false;
    })
  ];
in
pkgs.mkShell {
  nativeBuildInputs = [
    (pkgs.python312.withPackages my-python-packages)
  ];
  buildInputs = with pkgs; [
    python312Packages.tabulate
    python312Packages.types-tabulate
    python312Packages.wheel
    python312Packages.prompt-toolkit
    python312Packages.pygments
  ];
  shellHook = ''
    python3.12 -m xonsh
    exit
  '';
}
