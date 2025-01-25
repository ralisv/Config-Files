{ pkgs, ... }:

{
  home.packages = with pkgs; [
    (catppuccin-kvantum.override {
      accent = "lavender";
      variant = "mocha";
    })
    libsForQt5.qtstyleplugin-kvantum
    libsForQt5.qt5ct
    qt6Packages.qt6ct
  ];

  qt = {
    enable = true;
    platformTheme = "qtct";
    style = {
      name = "kvantum";
    };
  };

  xdg.configFile = {
    "Kvantum/kvantum.kvconfig".text = ''
      [General]
      theme=Catppuccin-Mocha-Lavender
    '';

    "qt5ct/qt5ct.conf".text = ''
      [Appearance]
      style=kvantum
    '';

    "qt6ct/qt6ct.conf".text = ''
      [Appearance]
      style=kvantum
    '';
  };
}
