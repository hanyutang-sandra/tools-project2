from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
	progress = models.TextField(max_length=100, default='0', blank=False)
	role = models.TextField(max_length=100, default='a', blank=False)
	picture = models.ImageField(upload_to='profile-pictures', default='', blank=True)
	group = models.ManyToManyField(User, related_name='group', symmetrical=False)