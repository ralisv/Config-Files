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
}
