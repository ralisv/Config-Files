{ pkgs, ... }:

{
  home.packages = with pkgs; [
    newsboat
  ];

  home.file.".newsboat/config".text = ''
    keep-articles-days 365
    article-sort-order date-asc
    prepopulate-query-feeds yes
    refresh-on-startup yes

    color background default default
    color listnormal color249 default
    color listfocus default default standout
    color listnormal_unread yellow default
    color listfocus_unread default default standout
    color info default default bold
    color article default default
  '';
}
