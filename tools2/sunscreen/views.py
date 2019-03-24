from django.shortcuts import render

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from django.urls import reverse

from django.core.mail import send_mail

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
		context['form'] = RegisterationForm()
		return render(request, 'sunscreen/register.html', context)

	if not form.is_valid():
		context['form'] = RegisterationForm()
		return render(request, 'sunscreen/register.html', context)

	new_user = form.save()
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

	return render(request, 'sunscreen/join.html', context)

def login(request):
	context={}
	errors=[]
	context['errors'] = errors

	if request.method=="GET":
		context['form'] = LoginForm()
		return render(request,'sunscreen/login.html',context)

	form = LoginForm()
	username = form.fields['username']
	password = form.fields['password']

	user = authenticate(request, username=username, password=password)

	if user is not None:
		login(request, user)
		return render(request,'sunscreen/join.html',context)

	errors.append("Authentication failed")
	context['form'] = LoginForm()

	return render(request,'sunscreen/login.html',context)

def join(request):
	return render(request, 'sunscreen/join.html')
