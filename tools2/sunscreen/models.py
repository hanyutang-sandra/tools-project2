from django.db import models

from django.utils import timezone
from datetime import datetime
from django.db.models import Max
from django.utils.html import escape

from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
	progress = models.TextField(max_length=100, default='0', blank=False)
	role = models.TextField(max_length=100, default='a', blank=False)
	picture = models.ImageField(upload_to='profile-pictures', default='', blank=True)
	group = models.ManyToManyField(User, related_name='group', symmetrical=False)
	groupped = models.BooleanField(default=False)

	def __unicode__(self):
		return self.user

class Post(models.Model):
	user = models.ForeignKey(User, related_name='expertposts',on_delete=models.CASCADE)
	text = models.TextField(max_length=20000)
	deleted = models.BooleanField(default=False)
	expert = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.text

	@staticmethod
	def get_posts_user(user, time="1970-01-01T00:00+00:00"):
		return Post.objects.filter(user=user, deleted=False, 
			   date_created__gt=time).distinct().order_by('-date_created').reverse()

	@staticmethod
	def get_posts_expert_stream(user, time="1970-01-01T00:00+00:00"):
		user_role = UserProfile.objects.filter(role = user.profile.role)
		user_role_group = []
		for u in user_role:
			user_role_group.append(u.user)
		return Post.objects.all().filter(expert = False, deleted=False, user__in=user_role_group, 
			   date_created__gt=time).distinct().order_by('-date_created').reverse()

	@staticmethod
	def get_posts_group_stream(user, time="1970-01-01T00:00+00:00"):
		group = user.profile.group.all()
		return Post.objects.all().filter(expert = True, user__in=group, deleted=False, 
			   date_created__gt=time).distinct().order_by('-date_created').reverse()

	@staticmethod
	def get_max_time_user(user):
		return Post.objects.filter(user=user).aggregate(Max('date_created'))['date_created__max'] or "1970-01-01T00:00+00:00"

	@staticmethod
	def get_max_time_expert_stream(user):
		user_role = UserProfile.objects.filter(role = user.profile.role)
		user_role_group = []
		for u in user_role:
			user_role_group.append(u.user)
		return Post.objects.filter(expert = False, deleted=False, user__in=user_role_group).aggregate(Max('date_created'))['date_created__max'] or "1970-01-01T00:00+00:00"

	@staticmethod
	def get_max_time_group_stream(user):
		group = user.profile.group.all()
		return Post.objects.filter(expert = True, user__in=group, deleted=False).aggregate(Max('date_created'))['date_created__max'] or "1970-01-01T00:00+00:00"

	@staticmethod
	def get_changes_user(user, time="1970-01-01T00:00+00:00"):
		return Post.objects.filter(user=user, date_created__gt=time).distinct().order_by('-date_created').reverse()

	@staticmethod
	def get_changes_expert_stream(user, time="1970-01-01T00:00+00:00"):
		user_role = UserProfile.objects.filter(role = user.profile.role)
		user_role_group = []
		for u in user_role:
			user_role_group.append(u.user)
		return Post.objects.filter(expert = False, deleted=False, user__in=user_role_group).filter(date_created__gt=time).distinct().order_by('-date_created').reverse()

	@staticmethod
	def get_changes_group_stream(user, time="1970-01-01T00:00+00:00"):
		group = user.profile.group.all()
		return Post.objects.filter(expert = True, user__in=group, deleted=False).filter(date_created__gt=time).distinct()
	
	@property
	def html(self):
		time = str(self.date_created).split('.')
		return "<li class='post_item' id='post_%d'> \
				<div class='form card'> \
				<div class='card-content'> \
				<div class='post-main'>\
				<span class='card-title grey-text text-darken-4 post-content'> %s </span>  \
				<p class='date_created'> %s </p> \
				</div>\
				<div class='card-profile'> \
				<span>\
	      		<img class='responsive-img' src='/static/site-resources/default.png' alt='No picture'> \
	      		</span>\
				<p> %s </p>\
				</div>\
				<span class='comment-btn'>\
				<i class='material-icons activator'>comment</i>\
				</span>\
	        	</div> \
	        	<div class= 'card-reveal'> \
	      		<span class= 'card-title grey-text text-darken-4'>Comment<i class='material-icons right'>close</i></span> \
	      		<textarea class='form-control comment-area' type='text' placeholder='Write something...' name='comment' id='new-comment'> </textarea>\
	        	<button id='comment-btn' class='btn'>Comment</button><ul style='list-style-type: none' id='comment-list'></ul> \
	   			</div> \
	        	</div> \
	        	</li>" % (self.id, escape(self.text), time[0], escape(self.user.username))
	

class Comment(models.Model):
	user = models.ForeignKey(User, related_name='expertcomments', on_delete=models.CASCADE) 
	post = models.ForeignKey(Post, related_name='expertcomments', on_delete=models.CASCADE) 
	deleted = models.BooleanField(default=False)
	text = models.TextField(max_length=20000)
	date_created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.text

	@staticmethod
	def get_comments(post, time="1970-01-01T00:00+00:00"):
		return Comment.objects.filter(post=post, deleted=False, 
			           date_created__gt=time).distinct().order_by('-date_created').reverse()

	@staticmethod
	def get_changes(post, time="1970-01-01T00:00+00:00"):
		return Comment.objects.filter(post=post, date_created__gt=time).distinct().order_by('-date_created').reverse()

	@property
	def html(self):
		time = str(self.date_created).split('.')
		return "<hr>\
				<li id='comment_%d'>\
				<div class='form card'> \
				<div class='card-content'> \
				<div class='post-main'>\
				<span class='card-title grey-text text-darken-4 post-content'> %s </span>  \
				<p class='date_created'> %s </p> \
				</div>\
				<div class='card-profile'> \
				<span>\
	      		<img class='responsive-img' src='/static/site-resources/default.png' alt='Nope'> \
	      		</span>\
				<p> %s </p>\
				</div>\
				</div>\
				</div>\
	         	</li>" % (self.id, escape(self.text), time[0], escape(self.user.username))
	

	@staticmethod
	def get_max_time(post):
		return Comment.objects.filter(post=post).aggregate(Max('date_created'))['date_created__max'] or "1970-01-01T00:00+00:00"

