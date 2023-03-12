from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_pictures', default='default.png')
    profile_cover_photo = models.ImageField(upload_to='profile_cover_pictures', blank=True)
    profile_bio = models.TextField(max_length=500, blank=True)
    def __str__(self):
        return self.user.username + ' Profile'

class Post(models.Model):
    post_id = models.AutoField(primary_key=True, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username + ' Post ' + str(self.post_id)

class PostImages(models.Model):
    post_image_id = models.AutoField(primary_key=True, blank=False, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_pictures')

class Friendship(models.Model):
    friendship_id = models.AutoField(primary_key=True, blank=False, null=False)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False, blank=False, null=False)
    def __str__(self):
        return self.from_user.username + ' is friends with ' + self.to_user.username
    
class Messages(models.Model):
    message_id = models.AutoField(primary_key=True, blank=False, null=False)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user_message')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user_message')
    message = models.TextField(max_length=1000, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.from_user.username + ' sent a message to ' + self.to_user.username