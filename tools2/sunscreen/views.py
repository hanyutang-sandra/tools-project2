from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from mimetypes import guess_type

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from django.urls import reverse

from django.core.mail import send_mail

import json
from django.http import JsonResponse

from sunscreen.models import *
from sunscreen.forms import *

# Create your views here.

def front(request):
	return render(request, 'sunscreen/front.html')

def register(request):
	context={}
	errors = []
	context['errors'] = errors

	if request.method == 'GET':
		context['form'] = RegistrationForm()
		return render(request, 'sunscreen/register.html', context)

	form = RegistrationForm(request.POST)
	context['form'] = form

	if not form.is_valid():
		return render(request, 'sunscreen/register.html', context)

	new_user = form.save()
	new_user.save()

	user_profile = UserProfile(user=new_user)
	user_profile.save()
	login(request, new_user)

	#token = default_token_generator.make_token(new_user)

	#email_body = """
	#Welcome to 'How sunscreens work' course! 
	#In this course you will experience the classical Jigsaw puzzle in a new online learning mode. 
	#Please click the link below to verify your email address (which will be used in case you forget your password in the future) 
	#to complete the registeration process:

	#http://%s%s""" % (request.get_host(), reverse('confirm-registeration', args = (new_user.username, token)))

	#send_mail(subject="Complete your registration process",
	#		message = email_body,
	#		from_email = "hanyut.dev@gmail.com",
	#		recipient_list = [new_user.email])

	return redirect('join')

def userlogin(request):
	context={}
	errors=[]
	context['errors'] = errors

	if request.method=="GET":
		context['form'] = LoginForm()
		return render(request,'sunscreen/login.html',context)

	form = LoginForm()

	username = request.POST.get('username')
	password = request.POST.get('password')

	user = authenticate(request, username=username, password=password)

	if user is not None:
		login(request, user)
		return redirect('join')

	errors.append("Authentication failed")
	context['form'] = LoginForm()

	return render(request,'sunscreen/login.html',context)

def join(request):
	context = {}
	context['progress'] = ''
	context['section_id'] = ''
	user = UserProfile.objects.get(user=request.user.id)
	status =  UserProfile.objects.get(user=request.user.id).progress
	print(status)
	notjoin = UserProfile.objects.filter(progress = '0')
	done = UserProfile.objects.filter(progress = '4')
	inprogress = len(UserProfile.objects.all()) - len(notjoin) - len(done)

	if status == '0':
		context['progress'] = 'notjoin'
		user.role = find_role()
		user.save()
		context['role'] = user.role
		print(user.role)
		print(user.group.all())
		print(UserProfile.objects.all())
	elif status == '5':
		context['progress'] = 'done'
	else:
		context['progress'] = 'inprogress'
		if status == '1':
			context['section_id'] = "1"
			context['sec_word'] = "You are currently watching the common video"
		elif status == '2':
			context['section_id'] = "2"
			context['sec_word'] = "You are currently watching your individual video"
		elif status == '3':
			context['section_id'] = "3"
			context['sec_word'] = "You are currently in expert group dicussion"
		elif status == '4':
			context['section_id'] = "4"
			context['sec_word'] = "You are currently discussing with your group members"
	return render(request, 'sunscreen/join.html', context)

def section(request, section_id):
	context = {}
	user = UserProfile.objects.get(user=request.user.id)
	if section_id == '3':
		user.progress = '3'
		user.save()
		return redirect('discuss_expert')
	elif section_id == '4':
		user.progress = '4'
		user.save()
		return  redirect('discuss_group')
	else:
		context['title'] = ''
		context['id'] = ''
		context['next'] = ''
		if section_id == '1':
			context['title'] = 'Section 1: Common Video'
			context['intro'] = "Now you will watch the video, this part is accessible to all people in your group, you DON’T need to teach them this part."
			#context['id'] = '9Meh079xYso'
			context['next'] = 'section/2'
			context['sec'] = '1'
			user.progress = '1'
			user.save()
			if len(find_group(request)) < 3:
				context['error'] = 'Sorry, there are not enough people in your group yet. You can proceed and learn, but you may miss part of the content, and may not be able to do final quiz perfectly! You can refresh to see if other people have joined the course.'
				context['role'] = user.role
			else:
				find_group(request)
				user.save()
				context['role'] = user.role
				context['group'] = user.group.all()
		elif section_id == '2':
			user.progress = '2'
			user.save()
			context['intro'] = "Now you will watch a video, you are the ONLY one watching this part in your group, so you ARE RESPONSIBLE TO TEACH your peer about this part afterwards."
			if user.role == 'a':
				context['title'] = 'Section 2a : UVA and UVB'
				#context['id'] = '7mc0Axd6Zf0'
				context['cover'] = 'a'
			elif user.role == 'b':
				context['title'] = 'Section 2b: Physical and Chemical Sunscreen'
				#context['id'] = 'bLdm82MA0bg'
				context['cover'] = 'b'
			context['next'] = 'section/3'
		return render(request, 'sunscreen/video.html', context)

def find_role():
	num_a = len(UserProfile.objects.filter(groupped = False, role = 'a')) - 1
	num_b = len(UserProfile.objects.filter(groupped = False, role = 'b'))
	if num_a > num_b:
		return 'b'
	else:
		return 'a'

def find_group(request):
	user_a_available =  UserProfile.objects.filter(groupped = False, role = 'a').all()
	user_b_available =  UserProfile.objects.filter(groupped = False, role = 'b').all()

	user = UserProfile.objects.get(user=request.user)
	user_role = user.role
	user.group.add(request.user)
	user.save()

	if len(user_b_available) == 0:
		return user.group.all()

	if len(user_a_available) == 0:
		return user.group.all()

	if user_role == 'a':
		user_b = User.objects.get(id = user_b_available[0].user.id)

		user.group.add(user_b)
		user.groupped = True
		user.save()

		user_b_available[0].group.add(request.user)
		user_b_available[0].groupped = True
		user_b_available[0].save()

	elif user_role == 'b':
		user_a = User.objects.get(id = user_a_available[0].user.id)

		user.group.add(user_a)
		user.groupped = True
		user.save()

		user_a_available[0].group.add(request.user)
		user_a_available[0].groupped = True
		user_a_available[0].save()
	
	print(user.groupped)
	print(user.group.all())

	return user.group.all()

def discuss(request):
	context = {}
	user = UserProfile.objects.get(user=request.user.id)
	user.progress = '3'
	user.save()
	user_role = user.role

	context['posts'] = ExpertPost.get_posts_expert_stream(request.user)
	context['user'] = request.user

	context['userlist'] = UserProfile.objects.filter(role = user_role)

	context['comment_redirect'] = 'stream'

	context['next'] = ''
	if user_role == 'a':
		context['next'] = '1'
	elif user_role == 'b':
		context['next'] = '2'
	else:
		context['next'] = '3'

	return render(request, 'sunscreen/discuss.html', context)

def group(request):
	context = {}
	user = UserProfile.objects.get(user=request.user.id)

	user.progress = '4'
	user.save()

	context['posts'] = GroupPost.get_posts_group_stream(request.user)
	context['user'] = request.user

	context['userlist'] = UserProfile.objects.get(user=request.user.id).group.all()

	userlist=UserProfile.objects.get(user=request.user.id).group.all()

	context['comment_redirect'] = 'stream'

	return render(request, 'sunscreen/teach.html', context)

def add_expertpost(request):
	if not 'post' in request.POST or not request.POST['post']:
		raise Http404
	else:
		new_post = ExpertPost(user=request.user, text=request.POST['post'])
		new_post.save()

	return HttpResponse("")  

def add_grouppost(request):
	if not 'post' in request.POST or not request.POST['post']:
		raise Http404
	else:
		new_post = GroupPost(user=request.user, text=request.POST['post'])
		new_post.save()

	return HttpResponse("")  

def expertcomment(request, redirect_name, user_id, post_id):
    context = {}
    errors = []
    if not 'comment' in request.POST or not request.POST['comment']:
        errors.append('You must post something...')
    else:
        post = ExpertPost.objects.get(id=post_id)
        new_comment = Comment(user=request.user, post=post, text=request.POST['comment'])
        new_comment.save()
        
    if (redirect_name == 'profile'):
        return redirect(reverse('profile', kwargs={'user_id':user_id}))
    else:
       return redirect(reverse(redirect_name))

def groupcomment(request, redirect_name, user_id, post_id):
    context = {}
    errors = []
    if not 'comment' in request.POST or not request.POST['comment']:
        errors.append('You must post something...')
    else:
        post = GroupPost.objects.get(id=post_id)
        new_comment = Comment(user=request.user, post=post, text=request.POST['comment'])
        new_comment.save()
        
    if (redirect_name == 'profile'):
        return redirect(reverse('profile', kwargs={'user_id':user_id}))
    else:
       return redirect(reverse(redirect_name))

def get_expert_stream_posts(request, time="1970-01-01T00:00+00:00"):
	#user = UserProfile.objects.get(user=request.user.id)
	max_time = ExpertPost.get_max_time_expert_stream(user=request.user)
	posts = ExpertPost.get_posts_expert_stream(user=request.user, time=time)
	context = {"max_time": max_time, "posts": posts}
	return render(request, 'posts.json', context, content_type='application/json')

def get_expert_stream_changes(request, time="1970-01-01T00:00+00:00"):
	#user = UserProfile.objects.get(user=request.user.id)
	max_time = ExpertPost.get_max_time_expert_stream(user=request.user)
	posts = ExpertPost.get_changes_expert_stream(user=request.user, time=time)
	context = {"max_time": max_time, "posts": posts}
	return render(request, 'posts.json', context, content_type='application/json')

def get_expertcomments(request, post_id, time="1970-01-01T00:00+00:00"):
    post = ExpertPost.objects.get(id=post_id)
    max_time = ExpertComment.get_max_time(post=post)
    comments = ExpertComment.get_comments(post=post)
    context = {"max_time": max_time, "comments": comments}
    return render(request, 'comments.json', context, content_type='application/json')

def get_groupcomments(request, post_id, time="1970-01-01T00:00+00:00"):
    post = GroupPost.objects.get(id=post_id)
    max_time = GroupComment.get_max_time(post=post)
    comments = GroupComment.get_comments(post=post)
    context = {"max_time": max_time, "comments": comments}
    return render(request, 'comments.json', context, content_type='application/json')

def get_expertcomment_changes(request, post_id, time="1970-01-01T00:00+00:00"):
    post = ExpertPost.objects.get(id=post_id)
    max_time = ExpertComment.get_max_time(post=post)
    comments = ExpertComment.get_changes(post=post, time=time)
    context = {"max_time": max_time, "comments": comments}
    return render(request, 'comments.json', context, content_type='application/json')

def get_groupcomment_changes(request, post_id, time="1970-01-01T00:00+00:00"):
    post = GroupPost.objects.get(id=post_id)
    max_time = GroupComment.get_max_time(post=post)
    comments = GroupComment.get_changes(post=post, time=time)
    context = {"max_time": max_time, "comments": comments}
    return render(request, 'comments.json', context, content_type='application/json')

def get_group_stream_posts(request, time="1970-01-01T00:00+00:00"):
    max_time = GroupPost.get_max_time_group_stream(user=request.user)
    posts = GroupPost.get_posts_group_stream(user=request.user, time=time)
    context = {"max_time": max_time, "posts": posts}
    return render(request, 'posts.json', context, content_type='application/json')

def get_group_stream_changes(request, time="1970-01-01T00:00+00:00"):
    max_time = GroupPost.get_max_time_group_stream(user=request.user)
    posts = GroupPost.get_changes_group_stream(user=request.user, time=time)
    context = {"max_time": max_time, "posts": posts}
    return render(request, 'posts.json', context, content_type='application/json')

def add_expertcomment(request, post_id):
    if not 'comment' in request.POST or not request.POST['comment']:
        raise Http404
    else:
        post = ExpertPost.objects.get(id=post_id)
        new_comment = ExpertComment(user=request.user, post=post, text=request.POST['comment'])
        new_comment.save()
        max_time = new_comment.date_created
        comments = ExpertComment.get_comments(post)
        context = {"max_time":max_time, "comments": comments}
    
    return render(request, 'comments.json', context, content_type='application/json')

def add_groupcomment(request, post_id):
    if not 'comment' in request.POST or not request.POST['comment']:
        raise Http404
    else:
        post = GroupPost.objects.get(id=post_id)
        new_comment = GroupComment(user=request.user, post=post, text=request.POST['comment'])
        new_comment.save()
        max_time = new_comment.date_created
        comments = GroupComment.get_comments(post)
        context = {"max_time":max_time, "comments": comments}
    
    return render(request, 'comments.json', context, content_type='application/json')

def quiz(request, quiz_id):
	user = UserProfile.objects.get(user=request.user.id)
	context = {}
	context['role'] = ''
	if user.role == 'a':
		context['role'] = 'a'
	elif user.role == 'b':
		context['role'] = 'b'
	else:
		context['role'] = 'c'
	return render(request, 'sunscreen/quiz.html', context)

def checkquiz(request, quiz_id):
	result = json.loads(request.POST['data'])
	quiz_id = str(request).split('/')[2].split("'")[0]
	answerkey_1a = [['1a1', '1a1a'], ['1a2', '1a2a'], ['1a3', '1a3b']]
	answerkey_1b = [['1b1', '1b1b'], ['1b2', '1b2d']]
	answerkey_1c = [['1c1', '1c1a'], ['1c2', '1c2b']]
	if quiz_id == '1a':
		return JsonResponse(checkanswer(result, answerkey_1a), safe=False)
	elif quiz_id == '1b':
		return JsonResponse(checkanswer(result, answerkey_1b), safe=False)
	else:
		return JsonResponse(checkanswer(result, answerkey_1c), safe=False)
	
def checkanswer(result, answer):
	feedback = []
	for i in range(len(result)):
		if result[i][1] == answer[i][1]:
			feedback.append('correct')
		else:
			feedback.append('incorrect')
	return feedback

def final(request):
	return render(request, 'sunscreen/final.html')

def checkfinal(request):
	result = json.loads(request.POST['data'])
	answerkey = [['f1', ['f1a', 'f1d']], ['f2', ['f2b', 'f2c']], ['f3', 'f3b'], ['f4', 'f4a'], ['f5', 'f5a'], ['f6', 'f6b']]	
	return JsonResponse(checkanswer(result, answerkey), safe=False)

def end(request):
	user = UserProfile.objects.get(user=request.user.id)
	user.progress = '5'
	user.save()
	return render(request, 'sunscreen/end.html')
