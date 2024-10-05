{ pkgs }:

let
  python-with-packages = pkgs.python312.withPackages (ps: with ps; [
    tabulate
    types-tabulate
    wheel
    prompt-toolkit
    pygments
    xonsh
  ]);
in
pkgs.mkShell {
  buildInputs = [
    python-with-packages
  ];
  shellHook = ''
    exec ${python-with-packages}/bin/xonsh
  '';
}
