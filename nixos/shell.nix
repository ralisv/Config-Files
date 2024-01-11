# On NixOS, you can't install python packages globally, this nix expression must be executed in nix-shell
# where my configuration of xonsh runs properly

{ pkgs ? import <nixpkgs> { } }:

let
  my-python-packages = p: with p; [
    (buildPythonPackage rec {
      pname = "xonsh";
      version = "0.14.3";

      src = fetchPypi {
        inherit pname version;
        sha256 = "sha256-pG1mE/jef1vrpsWyIuw3Z0BLZ4tLcH9Sq2ajJ+qbOWQ=";
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
