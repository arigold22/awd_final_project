# Generated by Django 4.1.7 on 2023-02-18 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_bio',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]