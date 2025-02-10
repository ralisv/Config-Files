{ pkgs, ... }:

{
  programs.newsboat = {
    enable = true;
    reloadThreads = 12;
    reloadTime = 120;
    extraConfig = ''
      keep-articles-days 365
      article-sort-order date-asc
      prepopulate-query-feeds yes

      color background default default
      color listnormal color249 default
      color listfocus default default standout
      color listnormal_unread color148 default
      color listfocus_unread default default standout
      color info color208 default bold
      color article color253 default
    '';
  };
}
