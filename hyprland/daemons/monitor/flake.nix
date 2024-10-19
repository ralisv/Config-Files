{
  description = "A flake for running sysmonitor.py with Python 3.12 and Pydantic";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, ... }:
    let
      pkgs = import nixpkgs { system = "x86_64-linux"; };
    in
    {
      devShells.default = pkgs.mkShell {
        buildInputs = [
          pkgs.python312
          (pkgs.python312.withPackages (ps: [ ps.pydantic ]))
        ];

        shellHook = ''
          echo "Executing sysmonitor.py..."
          python3.12 ${./sysmonitor.py}
          exit 0
        '';
      };
    };
}
