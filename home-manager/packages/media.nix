{ pkgs, ... }:

{
  home.packages = with pkgs; [
    # File explorers
    (nnn.override {
      withNerdIcons = true;
    })
    nemo

    # Browsers
    brave
    mullvad-browser
    librewolf

    # PDF readers
    okular

    # Mediaplayers
    vlc

    # File editors
    libreoffice
    gimp # Image editing
    cheese # Webcam
  ];

  xdg.mimeApps = {
    defaultApplications = {
      # Documents
      "application/pdf" = [ "org.kde.okular.desktop" ];
      "application/postscript" = [ "org.kde.okular.desktop" ];
      "application/x-dvi" = [ "org.kde.okular.desktop" ];
      "application/epub+zip" = [ "org.kde.okular.desktop" ];
      "application/x-mobipocket-ebook" = [ "org.kde.okular.desktop" ];
      "application/x-fictionbook+xml" = [ "org.kde.okular.desktop" ];
      "application/vnd.comicbook+zip" = [ "org.kde.okular.desktop" ];
      "application/vnd.comicbook-rar" = [ "org.kde.okular.desktop" ];
      "application/x-cbz" = [ "org.kde.okular.desktop" ];
      "application/x-cbr" = [ "org.kde.okular.desktop" ];
      "application/oxps" = [ "org.kde.okular.desktop" ];
      "application/vnd.ms-xpsdocument" = [ "org.kde.okular.desktop" ];
      "application/x-chm" = [ "org.kde.okular.desktop" ];
      "application/vnd.oasis.opendocument.text" = [ "org.kde.okular.desktop" ];

      # Images
      "image/jpeg" = [ "org.kde.okular.desktop" ];
      "image/png" = [ "org.kde.okular.desktop" ];
      "image/tiff" = [ "org.kde.okular.desktop" ];
      "image/x-djvu" = [ "org.kde.okular.desktop" ];
      "image/gif" = [ "org.kde.okular.desktop" ];
      "image/webp" = [ "org.kde.okular.desktop" ];
      "image/x-tiff" = [ "org.kde.okular.desktop" ];
      "image/x-portable-bitmap" = [ "org.kde.okular.desktop" ];
      "image/bmp" = [ "org.kde.okular.desktop" ];
      "image/x-portable-anymap" = [ "org.kde.okular.desktop" ];

      # Web content
      "text/html" = [ "brave-browser.desktop" ];
      "application/x-extension-htm" = [ "brave-browser.desktop" ];
      "application/x-extension-html" = [ "brave-browser.desktop" ];
      "application/x-extension-shtml" = [ "brave-browser.desktop" ];
      "application/xhtml+xml" = [ "brave-browser.desktop" ];
      "application/x-extension-xhtml" = [ "brave-browser.desktop" ];
      "application/x-extension-xht" = [ "brave-browser.desktop" ];

      # Web feeds
      "application/rss+xml" = [ "brave-browser.desktop" ];
      "application/xml" = [ "brave-browser.desktop" ];

      # Video formats
      "video/x-msvideo" = [ "vlc.desktop" ];
      "video/mp4" = [ "vlc.desktop" ];
      "video/mpeg" = [ "vlc.desktop" ];
      "video/ogg" = [ "vlc.desktop" ];
      "video/quicktime" = [ "vlc.desktop" ];
      "video/webm" = [ "vlc.desktop" ];
      "video/x-matroska" = [ "vlc.desktop" ];
      "video/x-flv" = [ "vlc.desktop" ];
      "video/3gpp" = [ "vlc.desktop" ];
      "video/3gpp2" = [ "vlc.desktop" ];
      "video/x-ms-wmv" = [ "vlc.desktop" ];
      "video/x-theora" = [ "vlc.desktop" ];
      "video/dv" = [ "vlc.desktop" ];

      # Audio formats
      "audio/mpeg" = [ "vlc.desktop" ];
      "audio/mp4" = [ "vlc.desktop" ];
      "audio/ogg" = [ "vlc.desktop" ];
      "audio/flac" = [ "vlc.desktop" ];
      "audio/x-wav" = [ "vlc.desktop" ];
      "audio/x-ms-wma" = [ "vlc.desktop" ];
      "audio/x-matroska" = [ "vlc.desktop" ];
      "audio/aac" = [ "vlc.desktop" ];
      "audio/ac3" = [ "vlc.desktop" ];
      "audio/webm" = [ "vlc.desktop" ];
    };
  };
}
