var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";

var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
function onYouTubeIframeAPIReady() {
  player = new YT.Player('playercommon', {
      height: '640',
      width: '960',
      videoId: '9Meh079xYso',
      events: {
            'onReady': onPlayerReady
          }
        });
   }

function onPlayerReady(event) {
  event.target.playVideo();
}