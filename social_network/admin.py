from django.contrib import admin
from .models import Profile, Post, PostImages, Friendship

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(PostImages)
admin.site.register(Friendship)