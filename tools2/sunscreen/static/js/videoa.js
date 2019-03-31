var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";

var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
function onYouTubeIframeAPIReady() {
  player = new YT.Player('playera', {
      height: '640',
      width: '960',
      videoId: 'bLdm82MA0bg',
      events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
          }
        });
   }

function onPlayerReady(event) {
  event.target.playVideo();
}



//let interval = setInterval(function(){
//    console.log(getTime())
//}, 700)
singleSelection()

const quiz1 = {
  id: '#a1',
  answerkey: 'a1a',
  begin: 29.5,
  incorrect: 57.5,
  next: 103
}

function displayQuiz1(){
  pauseVideo()
  $('#playerb').css('display', 'none')
  $('.cover.b').css('display', 'block').css('visibility', 'visible')
  $('#b1').css('display', 'inline-block').css('visibility', 'visible')
}

function handleQuiz1(){
  $('#b1').children().find('input').click(function(){
    $('#b1').children('.quiz_btn').css('display', 'block').click(function(){
      $('.cover.b').css('display', 'none').css('visibility', 'hidden')
    $('#b1').css('display', 'none').css('visibility', 'hidden')
    $('#playerb').css('display', 'block')
    if ($('#b1').children().find('input:checked')[0].attributes[0].value === 'a1a') {        
      playVideo()
    }else{
      seekVideo(58)
      playVideo()
    }
    })
  })
}

function handleChange1(){
  seekVideo(103)
  playVideo()
}

handleQuiz1()



const quiz2 = {
  id: '#a2',
  answerkey: 'a2b',
  begin: 167,
  incorrect: 186,
  next: 226,
}

function displayQuiz2(){
  pauseVideo()
  $('#playerb').css('display', 'none')
  $('.cover.b').css('display', 'block').css('visibility', 'visible')
  $('#b2').css('display', 'inline-block').css('visibility', 'visible')
}

function handleQuiz2(){
  $('#b2').children().find('input').click(function(){
    $('#b2').children('.quiz_btn').css('display', 'block').click(function(){
      $('.cover.b').css('display', 'none').css('visibility', 'hidden')
    $('#b2').css('display', 'none').css('visibility', 'hidden')
    $('#playerb').css('display', 'block')
    if ($('#b2').children().find('input:checked')[0].attributes[0].value === 'a2b') {        
      playVideo()
    }else{
      seekVideo(186)
      playVideo()
    }
    })
  })
}

function handleChange2(){
  seekVideo(226)
  playVideo()
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



