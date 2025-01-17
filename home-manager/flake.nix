{
  description = "Home Manager configuration of ralis";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    home-manager = {
      url = "github:nix-community/home-manager/master";
      inputs.nixpkgs.follows = "nixpkgs"; # Use the same nixpkgs as the main input
    };
  };

  outputs = { nixpkgs, home-manager, ... }:
    let
      system = "x86_64-linux";
    in
    {
      homeConfigurations."ralis" = home-manager.lib.homeManagerConfiguration {
        extraSpecialArgs = { inherit system; };
        pkgs = import nixpkgs {
          inherit system;
        };

        modules = [ ./home.nix ];
      };
    };
}
