{ ... }:

{
  programs.lsd = {
    enable = true;
    settings = {
      color = {
        theme = "default";
        when = "auto";
      };
      icons = {
        when = "auto";
        theme = "fancy";
        separator = " ";
      };
      sorting = {
        dir-grouping = "first";
      };
      date = "date";
      blocks = [
        "permission"
        "user"
        "group"
        "size"
        "date"
        "name"
      ];
      permission = "rwx";
      size = "short";
      total-size = true;
      symlink-arrow = "-->";
    };
  };
}
