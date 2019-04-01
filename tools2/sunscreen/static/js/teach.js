function addComment(e) {
    var contentField = $("#" + "post_" + e.data.id).find("#new-comment");
    var postDiv = $("#" + "post_" + e.data.id);
    var list = postDiv.find("#comment-list");
    $.post("/add-comment/" + e.data.id, {comment: contentField.val()})
      .done(function(data) {
        contentField.val("").focus();
        list.html('');
        for (var i = 0; i < data.comments.length; i++) {
            comment = data.comments[i];
            var new_comment = $(comment.html);
            new_comment.data("comment-id", comment.id);
            list.prepend(new_comment);
        }
        getUpdatedPost();
      });
}

function addCommentToPost(post) {
    var postDiv = $("#" + "post_" + post.id);
    var list = postDiv.find("#comment-list");
    $.get("/get-comments/" + post.id).done(function(data) {
        list.data('max-time', data['max-time']);
        list.html('');
        for (var i = 0; i < data.comments.length; i++) {
            comment = data.comments[i];
            var new_comment = $(comment.html);
            new_comment.data("comment-id", comment.id);
            list.prepend(new_comment);
        }
    });
}

function populateList() {
    $.get("/get-group-stream-posts").done(function(data) {
        var list = $("#post-list");
        list.data('max-time', data['max-time']);
        list.html('')
        for (var i = 0; i < data.posts.length; i++) {
            post = data.posts[i];
            var new_post = $(post.html);
            new_post.data("post-id", post.id);
            new_post.find("#comment-btn").click(post, addComment);
            list.prepend(new_post);
            addCommentToPost(post);
        }
    });
}

function addPost() {
    var contentField = $("#new_post");
    $.post("/add-grouppost", {post: contentField.val()}).done(function(data) {
            getUpdatedPost();
            contentField.val("").focus();
    });
}

function getUpdatedPost() {
    var list = $("#post-list")
    var max_time = list.data("max-time")
    $.get("/get-group-stream-changes/"+max_time)
      .done(function(data){
        list.data('max-time', data['max-time']);
        for (var i = 0; i < data.posts.length; i++) {
            var post = data.posts[i];
            if (post.deleted) {
                $("#post_" + post.id).remove();
            } else {
                var new_post = $(post.html);
                new_post.data("post-id", post.id);
                new_post.find("#comment-btn").click(post, addComment);
                list.prepend(new_post);
                addCommentToPost(post)
            }
        }
    });
}
function handleAlert(){
    $('.final_btn').click(function(){
        $('.alert').css('display', 'block').css('visibility', 'visible')
        $('.info').css('opacity', '0.5').css('filter', 'blur(0.3rem)')
        $('.blog-post').css('opacity', '0.5').css('filter', 'blur(0.3rem)')
    })
    $('.q1').css('display', 'block').siblings('p').css('display', 'none')
    $('.ac_q1').css('display', 'block').siblings('.card-action').css('display', 'none')

    $('.ac_q1').children('.btn').click(function(){
        if ($(this).index('.btn') === 0){
            $('.q2').css('display', 'block').siblings('p').css('display', 'none')
            $('.ac_q2').css('display', 'block').siblings('.card-action').css('display', 'none')
        }else if ($(this).index('.btn') === 1){
            $('.al1').css('display', 'block').siblings('p').css('display', 'none')
            $('.ac_al').css('display', 'block').siblings('.card-action').css('display', 'none')
        }
    })

    $('.ac_q2').children('.btn').click(function(){
        if ($(this).index('.btn') === 2){
            $('p').css('display', 'none')
            $('.alert-card').text('You are good to go!')
            $('.pass').css('display', 'block').siblings('.card-action').css('display', 'none')
        }else if ($(this).index('.btn') === 3){
            $('.al2').css('display', 'block').siblings('p').css('display', 'none')
            $('.ac_al').css('display', 'block').siblings('.card-action').css('display', 'none')
        }
    })

     $('.ac_al').click(function(){
        location.reload()
    })

}

$(document).ready(function () {
    populateList();
    $("#post-btn").click(addPost);

    handleAlert()

    window.setInterval(getUpdatedPost, 5000);

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
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
});

