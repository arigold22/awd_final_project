# Generated by Django 4.1.7 on 2023-02-22 08:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social_network', '0003_posts'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Posts',
            new_name='Post',
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_cover_photo',
            field=models.ImageField(default='default_cover.png', upload_to='profile_cover_pictures'),
        ),
    ]
