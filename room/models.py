from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    participants = models.ManyToManyField(User, related_name='joined_rooms')
    online_participants = models.ManyToManyField(User, related_name='online_rooms', blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_rooms', default=None, null=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[0:25]

    class Meta:
        ordering = ('date_added',)
