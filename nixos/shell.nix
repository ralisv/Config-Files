# On NixOS, you can't install python packages globally, this nix expression must be executed in nix-shell
# where my configuration of xonsh runs properly

{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs.python3Packages; [
		gitpython
		colorama
		tabulate
  ];
	shellHook = ''
		xonsh
		exit
	'';
}
