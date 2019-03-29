from django import forms

from django.contrib.auth.models import User
from sunscreen.models import *

class RegistrationForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'password')
		widgets = {
			'password': forms.PasswordInput()
		}

	repassword = forms.CharField(max_length=100, label='Comfirm Password', 
								error_messages={'required': 'Please conform your password.'},
								widget=forms.PasswordInput())
	def clean(self):
		cleaned_data = super(RegistrationForm, self).clean()
		password = cleaned_data.get('password')
		repassword = cleaned_data.get('repassword')
		if password and repassword and password != repassword:
			raise forms.ValidationError('Password did not match')
		return cleaned_data

	def cleaned_username(self):
		username = self.cleaned_data.get('username')
		if User.objects.filter(username__exact=username):
			raise forms.ValidationError('Username is already taken.')
		return username

	#def cleaned_email(self):
	#	email.self.cleaned_data.get('email')
	#	if User.objects.filter(email__exact=email):
	#		raise forms.ValidationError('Email is already taken.')
	#	return email

	def save(self):
		new_user = User.objects.create_user(username=self.cleaned_data.get('username'),
											#email=self.cleaned_data.get('email'),
											password=self.cleaned_data.get('password'))
		new_user.save()
		return new_user


class LoginForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'password')
		widgets = {
			'password': forms.PasswordInput()
		}


	def clean(self):
		cleaned_data = super(LoginForm, self).clean()
		return cleaned_data


