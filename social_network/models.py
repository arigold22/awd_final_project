from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_pictures', default='default.png')
    profile_bio = models.TextField(max_length=500, blank=True)

class Post(models.Model):
    post_id = models.AutoField(primary_key=True, blank=False, null=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    images = models.ImageField(upload_to='post_pictures', blank=True)
    anonymous = models.BooleanField(default=False, blank=False, null=False)

