# Generated by Django 4.1.5 on 2023-03-12 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0016_messages'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='friendship',
            constraint=models.UniqueConstraint(fields=('from_user', 'to_user'), name='unique_friendship'),
        ),
    ]
