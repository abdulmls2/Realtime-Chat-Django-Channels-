from django.contrib.auth.models import User
from django.db import models


# class Room(models.Model):
#     # creator = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
#     name = models.CharField(max_length=255)
#     slug = models.SlugField(unique=True)
#     # participants = models.ManyToManyField(User, related_name='joined_rooms')
#
#     def __str__(self):
#         return self.name
#
#
# class Message(models.Model):
#     room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
#     user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
#     content = models.TextField()
#     date_added = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ('date_added',)

class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    participants = models.ManyToManyField(User, related_name='joined_rooms')

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)
