# Generated by Django 4.2.4 on 2023-08-29 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0010_delete_connected'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='is_online',
            field=models.BooleanField(default=False),
        ),
    ]
