var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";

var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
function onYouTubeIframeAPIReady() {
  player = new YT.Player('playera', {
      height: '640',
      width: '960',
      playerVars: {
          rel: 0,
          showinfo: 0,
          fs: 0
      },
      videoId: '7mc0Axd6Zf0',
      events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
          }
        });
   }

function onPlayerReady(event) {
  event.target.playVideo();
}


singleSelection()

const quiz1 = {
  id: '#a1',
  answerkey: 'a1a',
  begin: 75,
  incorrect: 86,
  next: 160
}

function displayQuiz1(){
  console.log('1')
  pauseVideo()
  $('#playera').css('display', 'none')
  $('.cover.a').css('display', 'block').css('visibility', 'visible')
  $('#a1').css('display', 'inline-block').css('visibility', 'visible')
}

function handleQuiz1(){
  $('#a1').children().find('input').click(function(){
    $('#a1').children('.quiz_btn').css('display', 'inline-block').click(function(){
      $('.cover.a').css('display', 'none').css('visibility', 'hidden')
    $('#a1').css('display', 'none').css('visibility', 'hidden')
    $('#playera').css('display', 'block')
    if ($('#a1').children().find('input:checked')[0].attributes[0].value === 'a1a') {        
      seekVideo(76)
      playVideo()
    }else{
      seekVideo(86)
      playVideo()
    }
    })
  })
}

function handleChange1(){
  seekVideo(160)
  playVideo()
}

handleQuiz1()



const quiz2 = {
  id: '#a2',
  answerkey: 'a2b',
  begin: 170,
  incorrect: 181,
  next: 300,
}

function displayQuiz2(){
  pauseVideo()
  $('#playera').css('display', 'none')
  $('.cover.a').css('display', 'block').css('visibility', 'visible')
  $('#a2').css('display', 'inline-block').css('visibility', 'visible')
}

function handleQuiz2(){
  $('#a2').children().find('input').click(function(){
    $('#a2').children('.quiz_btn').css('display', 'inline-block').click(function(){
      $('.cover.a').css('display', 'none').css('visibility', 'hidden')
    $('#a2').css('display', 'none').css('visibility', 'hidden')
    $('#playera').css('display', 'block')
    if ($('#a2').children().find('input:checked')[0].attributes[0].value === 'a2b') {        
      playVideo()
    }else{
      seekVideo(181)
      playVideo()
    }
    })
  })
}

function handleChange2(){
  stopVideo()
}

handleQuiz2()

let stopPlayTimer
      

function onPlayerStateChange(event) {
  var time, rate, remainingTime
  clearTimeout(stopPlayTimer);

  if (event.data == YT.PlayerState.PLAYING) {
      time = player.getCurrentTime();
      if (time + .1 < quiz1.begin) {
          rate = player.getPlaybackRate();
          remainingTime = (quiz1.begin - time) / rate;
          stopPlayTimer = setTimeout(displayQuiz1, remainingTime * 1000);
      }
      if(time + .1 >=quiz1.begin && time + .1 < quiz1.incorrect){
          rate = player.getPlaybackRate();
          remainingTime = (quiz1.incorrect - time) / rate;
          stopPlayTimer = setTimeout(handleChange1, remainingTime * 1000);
        }
      if(time + .1 >=quiz1.incorrect && time + .1 < quiz2.begin){
          rate = player.getPlaybackRate();
          remainingTime = (quiz2.begin - time) / rate;
          stopPlayTimer = setTimeout(displayQuiz2, remainingTime * 1000);
        }
      if(time + .1 >=quiz2.begin && time + .1 < quiz2.incorrect){
          rate = player.getPlaybackRate();
          remainingTime = (quiz2.incorrect - time) / rate;
          stopPlayTimer = setTimeout(handleChange2, remainingTime * 1000);
      }
        
}
    
      }
function stopVideo() {
  player.stopVideo();
}

function getTime(){
    return Math.round(player.getCurrentTime());
}

function playVideo(){
    player.playVideo()
}

function pauseVideo() {
    player.pauseVideo();
}

function seekVideo(t){
  player.seekTo(t)
}

function singleSelection(){
  $('input').click(function(){
    $(this).closest('.quiz').children().find('input').not($(this)).prop('checked', false)
  })
}



