{
  programs.freetube = {
    enable = true;
    settings = {
      autoplayVideos = false;
      backendPreference = "local";
      barColor = false;
      baseTheme = "catppuccinMocha";
      bounds = {
        x = 2960;
        y = 600;
        width = 1200;
        height = 800;
        maximized = true;
        fullScreen = false;
      };
      checkForUpdates = false;
      defaultPlayback = 1.4;
      defaultTheatreMode = true;
      expandSideBar = false;
      hideActiveSubscriptions = false;
      hideComments = false;
      hideHeaderLogo = false;
      hideLabelsSideBar = false;
      hidePlaylists = true;
      hidePopularVideos = true;
      hideTrendingVideos = true;
      mainColor = "Pink";
      maxVideoPlaybackRate = 2;
      playNextVideo = false;
      quickBookmarkTargetPlaylistId = "favorites";
      secColor = "Red";
      sponsorBlockFiller = {
        color = "Cyan";
        skip = "showInSeekBar";
      };
      sponsorBlockIntro = {
        color = "Orange";
        skip = "autoSkip";
      };
      sponsorBlockMusicOffTopic = {
        color = "Amber";
        skip = "showInSeekBar";
      };
      sponsorBlockOutro = {
        color = "Orange";
        skip = "autoSkip";
      };
      sponsorBlockRecap = {
        color = "Pink";
        skip = "doNothing";
      };
      sponsorBlockSelfPromo = {
        color = "Yellow";
        skip = "showInSeekBar";
      };
      sponsorBlockSponsor = {
        color = "LightGreen";
        skip = "autoSkip";
      };
      uiScale = 80;
      useDeArrowThumbnails = true;
      useDeArrowTitles = false;
      useRssFeeds = false;
      useSponsorBlock = true;
      videoPlaybackRateInterval = "0.1";
      allowDashAv1Formats = true;
      defaultQuality = "1080";
    };
  };
}
