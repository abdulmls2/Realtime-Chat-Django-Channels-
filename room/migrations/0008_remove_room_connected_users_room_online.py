# Generated by Django 4.2.4 on 2023-08-29 17:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('room', '0007_remove_room_online_users_room_connected_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='connected_users',
        ),
        migrations.AddField(
            model_name='room',
            name='online',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]