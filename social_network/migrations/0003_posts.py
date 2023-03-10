# Generated by Django 4.1.7 on 2023-02-21 15:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social_network', '0002_profile_profile_bio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField(max_length=1000)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('images', models.ImageField(blank=True, upload_to='post_pictures')),
                ('anonymous', models.BooleanField(default=False)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
