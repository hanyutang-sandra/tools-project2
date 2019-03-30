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
	status =  UserProfile.objects.get(user=request.user.id).progress
	print(status)
	notjoin = UserProfile.objects.filter(progress = '0')
	done = UserProfile.objects.filter(progress = '4')
	inprogress = len(UserProfile.objects.all()) - len(notjoin) - len(done)

	if inprogress >= 12:
		context['progress'] = 'full'
		return render(request, 'sunscree/join.html', context)

	if status == '0':
		context['progress'] = 'notjoin'
	elif status == '5':
		context['progress'] = 'done'
	else:
		context['progress'] = 'inprogress'
		if status == '1':
			context['section_id'] = "1"
		elif status == '2':
			context['section_id'] = "2"
		elif status == '3':
			context['section_id'] = "3"
		elif status == '4':
			context['section_id'] = "4"
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
			context['title'] = 'Section 1: Introduction'
			context['id'] = '9Meh079xYso'
			context['next'] = 'section/2'
			user.progress = '1'
			user.role = find_role()
			user.save()
		elif section_id == '2':
			user.progress = '2'
			user.save()
			if user.role == 'a':
				context['title'] = 'Section 2a : UVA and UVB'
				context['id'] = '7mc0Axd6Zf0'
			elif user.role == 'b':
				context['title'] = 'Section 2b: Physical Sunscreen'
				context['id'] = 'bBfr-o5gKR0'
			elif user.role == 'c':
				context['title'] = 'Section 2c: Chemical Sunscreen'
				context['id'] = 'wxI-jK7XgD4'
			context['next'] = 'section/3'
		print(user.role)
		return render(request, 'sunscreen/video.html', context)

def find_role():
	num_a = len(UserProfile.objects.filter(role = 'a')) - 1
	num_b = len(UserProfile.objects.filter(role = 'b'))
	num_c = len(UserProfile.objects.filter(role = 'c'))
	roles = {'a': num_a, 'b': num_b, 'c': num_c}
	for x, y in roles.items():
		new_role = list(min(roles.items(), key=lambda x: x[1]))[0]
	return new_role
	
def find_group(request):
	a_people = UserProfile.objects.filter(role = 'a', progress = '3')
	b_people = UserProfile.objects.filter(role = 'b', progress = '3')
	c_people = UserProfile.objects.filter(role = 'c', progress = '3')
	user = UserProfile.objects.get(user=request.user.id)
	user_role = user.role
	new_group = []
	if user_role == 'a':
		if len(b_people) > 0:
			user_b = b_people[0]
			user.group.add(user_b)
			new_group.append(user_b.user.username)
		else: 
			print('nobody available')
	print(new_group)
	return new_group

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

	return render(request, 'sunscreen/discuss.html')

def group(request):
	context = {}
	user = UserProfile.objects.get(user=request.user.id)
	user.group.add(request.user)
	user.progress = '4'
	user.save()

	context['posts'] = GroupPost.get_posts_group_stream(request.user)
	context['user'] = request.user

	context['userlist'] = UserProfile.objects.get(user=request.user.id).group.all()

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
	user = UserProfile.objects.get(user=request.user.id)
	max_time = ExpertPost.get_max_time_expert_stream(user=request.user)
	posts = ExpertPost.get_posts_expert_stream(user=request.user, time=time)
	context = {"max_time": max_time, "posts": posts}
	return render(request, 'posts.json', context, content_type='application/json')

def get_expert_stream_changes(request, time="1970-01-01T00:00+00:00"):
	user = UserProfile.objects.get(user=request.user.id)
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
