function singleSelection(){
	$('input').click(function(){
		$(this).closest('.single').children().find('input').not($(this)).prop('checked', false)
	})
}

function checkComplete(){
	let checklist = []
	$('.quiz_content').each(function(){
		if ($(this).children().find('input:checked').length > 0){
			return
		}else{
			checklist.push($(this)[0].attributes[1].value)
		}
	})
	if (checklist.length > 0){
		$('.error').text('Please finish the quiz')
		return false
	}else{
		$('.error').text('')
		return true
	}
}

function submitQuiz(){
	$('#submit').click(function(){
		if (!checkComplete()){
			return false
		}
		let answerMap = new Map()	

		let multi1 = []
		$('.multi1').children().find('input:checked').each(function(){
			multi1.push($(this)[0].attributes[0].value)
		})
		answerMap.set('f1', multi1)

		let multi2 = []
		$('.multi2').children().find('input:checked').each(function(){
			multi2.push($(this)[0].attributes[0].value)
		})
		answerMap.set('f2', multi2)

		$('.single').each(function(){
			answerMap.set($(this)[0].attributes[1].value, $(this).children().find('input:checked')[0].attributes[0].value)
		})
		
		answerData = JSON.stringify([...answerMap])
		$.post('/checkfinal/', {data: answerData})
			.done(function(data){
				provideFeedback(data)
			})  
	})
	
}

function provideFeedback(data){
	$('.feedback').css('display', 'block')
	let correct = 0
	for (var i in data){
		if (data[i] === 'correct'){
			$('.quiz_content')[i].children[0].style.color = 'green'
			correct += 1
		}else{
			$('.quiz_content')[i].children[0].style.color = 'pink'
		}
	}
	$('#submit').css('display', 'none')
	$('#end').css('display', 'inline-block')

}


$(document).ready(function(){
	singleSelection()
	submitQuiz()

	function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
})