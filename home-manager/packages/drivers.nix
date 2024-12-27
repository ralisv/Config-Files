{ pkgs, ... }:

{
  home.packages = with pkgs; [
    ntfs3g # For NTFS support
  ];
}
