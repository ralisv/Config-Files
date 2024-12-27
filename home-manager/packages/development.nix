{ pkgs, ... }:

{
  home.packages = with pkgs; [
    nixpkgs-fmt
    ghc
    python312Full
    python312Packages.jupyter
    python312Packages.jupyter-core
    python312Packages.scipy
    python312Packages.numpy
    docker
    docker-compose
  ];
}
