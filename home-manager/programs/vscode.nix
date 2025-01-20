{ pkgs, ... }:

{
  programs.vscode = {
    enable = true;
    package = pkgs.vscode-fhs;

    extensions = with pkgs.vscode-extensions; [
      ms-python.python
      ms-python.isort
      ms-python.debugpy
      ms-python.pylint
      ms-python.black-formatter
      github.copilot
      github.copilot-chat
      jnoortheen.nix-ide
      mads-hartmann.bash-ide-vscode
    ];

    keybindings = [
      {
        key = "ctrl+y";
        command = "redo";
      }
      {
        key = "ctrl+z";
        command = "undo";
      }
      {
        key = "ctrl+t";
        command = "python.createTerminal";
      }
      {
        key = "ctrl+q";
        command = "workbench.action.closeWindow";
      }
      {
        key = "ctrl+shift+q";
        command = "workbench.action.closeSidebar";
      }
      {
        key = "ctrl+a";
        command = "editor.action.selectAll";
      }
    ];
  };

  xdg.mimeApps = {
    defaultApplications = {
      # Plain text and documents
      "text/plain" = [ "code.desktop" ];
      "text/markdown" = [ "code.desktop" ];
      "text/x-markdown" = [ "code.desktop" ];
      "text/x-log" = [ "code.desktop" ];

      # Markup languages
      "text/html" = [ "code.desktop" ];
      "text/xml" = [ "code.desktop" ];
      "application/xml" = [ "code.desktop" ];
      "application/json" = [ "code.desktop" ];
      "application/ld+json" = [ "code.desktop" ];
      "application/x-yaml" = [ "code.desktop" ];
      "text/yaml" = [ "code.desktop" ];
      "text/x-toml" = [ "code.desktop" ];

      # Common programming languages
      "text/x-python" = [ "code.desktop" ];
      "text/x-python3" = [ "code.desktop" ];
      "text/x-java" = [ "code.desktop" ];
      "text/x-c" = [ "code.desktop" ];
      "text/x-c++" = [ "code.desktop" ];
      "text/x-c++src" = [ "code.desktop" ];
      "text/x-csrc" = [ "code.desktop" ];
      "text/javascript" = [ "code.desktop" ];
      "application/javascript" = [ "code.desktop" ];
      "application/x-javascript" = [ "code.desktop" ];
      "text/x-typescript" = [ "code.desktop" ];
      "text/typescript" = [ "code.desktop" ];
      "text/x-php" = [ "code.desktop" ];
      "application/x-php" = [ "code.desktop" ];
      "text/x-ruby" = [ "code.desktop" ];
      "text/x-shellscript" = [ "code.desktop" ];
      "application/x-shellscript" = [ "code.desktop" ];
      "text/x-makefile" = [ "code.desktop" ];
      "text/x-rust" = [ "code.desktop" ];
      "text/x-go" = [ "code.desktop" ];

      # Configuration files
      "text/x-properties" = [ "code.desktop" ];
      "text/x-config" = [ "code.desktop" ];
      "application/x-desktop" = [ "code.desktop" ];
      "application/x-perl" = [ "code.desktop" ];
    };
  };

}
