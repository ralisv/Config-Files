{
  description = "Home Manager configuration of ralis";

  # Hyprland version 0.46.2 crashes, so nixpkgs with version 0.46.1 is pinned and used

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    nixpkgs-pinned-hyprland = {
      url = "github:NixOS/nixpkgs/d70bd19e0a38ad4790d3913bf08fcbfc9eeca507";
    };
    home-manager = {
      url = "github:nix-community/home-manager/master";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { nixpkgs, nixpkgs-pinned-hyprland, home-manager, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      pkgs-pinned-hypr = import nixpkgs-pinned-hyprland {
        inherit system;
      };
    in
    {
      homeConfigurations."ralis" = home-manager.lib.homeManagerConfiguration {
        inherit pkgs;

        extraSpecialArgs = {
          inherit pkgs-pinned-hypr;
        };

        modules = [ ./home.nix ];
      };
    };
}
