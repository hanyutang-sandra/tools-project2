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

	def __unicode__(self):
		return self.user

class ExpertPost(models.Model):
	user = models.ForeignKey(User, related_name='expertposts',on_delete=models.CASCADE)
	text = models.TextField(max_length=20000)
	deleted = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.text

	@staticmethod
	def get_posts_user(user, time="1970-01-01T00:00+00:00"):
		return ExpertPost.objects.filter(user=user, deleted=False, 
			   date_created__gt=time).distinct().order_by('-date_created').reverse()

	@staticmethod
	def get_posts_expert_stream(user, time="1970-01-01T00:00+00:00"):
		user_role = UserProfile.objects.get(role = user.profile.role)
		return ExpertPost.objects.all().filter(deleted=False, user = User.objects.get(username = user_role.user.username), 
			   date_created__gt=time).distinct().order_by('-date_created').reverse()

	@staticmethod
	def get_max_time_user(user):
		return ExpertPost.objects.filter(user=user).aggregate(Max('date_created'))['date_created__max'] or "1970-01-01T00:00+00:00"

	@staticmethod
	def get_max_time_expert_stream(user):
		return ExpertPost.objects.all().aggregate(Max('date_created'))['date_created__max'] or "1970-01-01T00:00+00:00"


	@staticmethod
	def get_changes_user(user, time="1970-01-01T00:00+00:00"):
		return ExpertPost.objects.filter(user=user, date_created__gt=time).distinct().order_by('-date_created').reverse()

	@staticmethod
	def get_changes_expert_stream(user, time="1970-01-01T00:00+00:00"):
		user_role = UserProfile.objects.get(role = user.profile.role)
		return ExpertPost.objects.filter(user = User.objects.get(username = user_role.user.username)).filter(date_created__gt=time).distinct().order_by('-date_created').reverse()

	@property
	def html(self):
		time = str(self.date_created).split('.')
		if self.user.profile.picture:
			return "<li class='post_item' id='post_%d'> \
					<div class='form card'> \
					<div class='card-content'> \
					<div class='post-main'>\
					<span class='card-title grey-text text-darken-4 post-content'> %s </span>  \
					<p class='date_created'> %s </p> \
					</div>\
					<div class='card-profile'> \
					<span>\
	      			<img class='responsive-img' src='/profile-picture/%s' alt='No picture'> \
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
	        		<button id='comment-btn'>Comment</button><ul style='list-style-type: none' id='comment-list'></ul> \
	   				</div> \
	        		</div> \
	        		</li>" % (self.id, escape(self.text), time[0], escape(self.user.id), escape(self.user.username))
		else:
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
	        		<button id='comment-btn'>Comment</button><ul style='list-style-type: none' id='comment-list'></ul> \
	   				</div> \
	        		</div> \
	        		</li>" % (self.id, escape(self.text), time[0], escape(self.user.username))
	    
class GroupPost(models.Model):
	user = models.ForeignKey(User, related_name='groupposts',on_delete=models.CASCADE)
	text = models.TextField(max_length=20000)
	deleted = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.text

	@staticmethod
	def get_posts_user(user, time="1970-01-01T00:00+00:00"):
		return GroupPost.objects.filter(user=user, deleted=False, 
			   date_created__gt=time).distinct().order_by('-date_created').reverse()


	@staticmethod
	def get_posts_group_stream(user, time="1970-01-01T00:00+00:00"):
		group = user.profile.group.all()
		return GroupPost.objects.filter(user__in=group, deleted=False, 
			   date_created__gt=time).distinct().order_by('-date_created').reverse()

	@staticmethod
	def get_max_time_user(user):
		return GroupPost.objects.filter(user=user).aggregate(Max('date_created'))['date_created__max'] or "1970-01-01T00:00+00:00"


	@staticmethod
	def get_max_time_group_stream(user):
		group = user.profile.group.all()
		print(group)
		return GroupPost.objects.filter(user__in=group).aggregate(Max('date_created'))['date_created__max'] or "1970-01-01T00:00+00:00"

	@staticmethod
	def get_changes_user(user, time="1970-01-01T00:00+00:00"):
		return GroupPost.objects.filter(user=user, date_created__gt=time).distinct().order_by('-date_created').reverse()

	@staticmethod
	def get_changes_group_stream(user, time="1970-01-01T00:00+00:00"):
		group = user.profile.group.all()
		return GroupPost.objects.filter(user__in=group, 
			   date_created__gt=time).distinct().order_by('-date_created').reverse()

	@property
	def html(self):
		time = str(self.date_created).split('.')
		if self.user.profile.picture:
			return "<li class='post_item' id='post_%d'> \
					<div class='form card'> \
					<div class='card-content'> \
					<div class='post-main'>\
					<span class='card-title grey-text text-darken-4 post-content'> %s </span>  \
					<p class='date_created'> %s </p> \
					</div>\
					<div class='card-profile'> \
					<span>\
	      			<img class='responsive-img' src='/profile-picture/%s' alt='No picture'> \
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
	        		<button id='comment-btn'>Comment</button><ul style='list-style-type: none' id='comment-list'></ul> \
	   				</div> \
	        		</div> \
	        		</li>" % (self.id, escape(self.text), time[0], escape(self.user.id), escape(self.user.username))
		else:
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
	        		<button id='comment-btn'>Comment</button><ul style='list-style-type: none' id='comment-list'></ul> \
	   				</div> \
	        		</div> \
	        		</li>" % (self.id, escape(self.text), time[0], escape(self.user.username))
	

class ExpertComment(models.Model):
	user = models.ForeignKey(User, related_name='expertcomments', on_delete=models.CASCADE) 
	post = models.ForeignKey(ExpertPost, related_name='expertcomments', on_delete=models.CASCADE) 
	deleted = models.BooleanField(default=False)
	text = models.TextField(max_length=20000)
	date_created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.text

	@staticmethod
	def get_comments(post, time="1970-01-01T00:00+00:00"):
		return ExpertComment.objects.filter(post=post, deleted=False, 
			           date_created__gt=time).distinct().order_by('-date_created').reverse()

	@staticmethod
	def get_changes(post, time="1970-01-01T00:00+00:00"):
		return ExpertComment.objects.filter(post=post, date_created__gt=time).distinct().order_by('-date_created').reverse()

	@property
	def html(self):
		time = str(self.date_created).split('.')
		if self.user.profile.picture:
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
	      			<img class='responsive-img' src='/profile-picture/%s' alt='No picture right now'> \
	      			</span>\
					<p> %s </p>\
					</div>\
					</div>\
					</div>\
	         		</li>" % (self.id, escape(self.text), time[0], escape(self.user.id), escape(self.user.username))
		else:
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
		return ExpertComment.objects.filter(post=post).aggregate(Max('date_created'))['date_created__max'] or "1970-01-01T00:00+00:00"


class GroupComment(models.Model):
	user = models.ForeignKey(User, related_name='groupcomments', on_delete=models.CASCADE) 
	post = models.ForeignKey(GroupPost, related_name='groupcomments', on_delete=models.CASCADE) 
	deleted = models.BooleanField(default=False)
	text = models.TextField(max_length=20000)
	date_created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.text

	@staticmethod
	def get_comments(post, time="1970-01-01T00:00+00:00"):
		return GroupComment.objects.filter(post=post, deleted=False, 
			           date_created__gt=time).distinct().order_by('-date_created').reverse()

	@staticmethod
	def get_changes(post, time="1970-01-01T00:00+00:00"):
		return GroupComment.objects.filter(post=post, date_created__gt=time).distinct().order_by('-date_created').reverse()

	@property
	def html(self):
		time = str(self.date_created).split('.')
		if self.user.profile.picture:
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
	      			<img class='responsive-img' src='/profile-picture/%s' alt='No picture right now'> \
	      			</span>\
					<p> %s </p>\
					</div>\
					</div>\
					</div>\
	         		</li>" % (self.id, escape(self.text), time[0], escape(self.user.id), escape(self.user.username))
		else:
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
		return GroupComment.objects.filter(post=post).aggregate(Max('date_created'))['date_created__max'] or "1970-01-01T00:00+00:00"