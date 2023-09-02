from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404

from .models import Room, Message

import uuid


@login_required
def user_rooms(request):
    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'join':
            slug = request.POST.get('room_slug', '')
            try:
                room = Room.objects.get(slug=slug)
                room.participants.add(request.user)
            except Room.DoesNotExist:
                pass  # Handle this case as needed

        elif action == 'create':
            room_name = request.POST.get('room_name', '')
            slug = str(uuid.uuid4().int)[:5]
            if not Room.objects.filter(slug=slug).exists():
                new_room = Room.objects.create(name=room_name, slug=slug, owner=request.user)
                new_room.participants.add(request.user)
                return redirect('user_rooms')

    user_rooms = Room.objects.filter(participants=request.user)
    return render(request, 'room/rooms.html', {'user_rooms': user_rooms})


@login_required
def room(request, slug):
    room = get_object_or_404(Room, slug=slug)
    # room = Room.objects.get(slug=slug)
    if request.user in room.participants.all():
        messages = Message.objects.filter(room=room)
        participants_count = room.participants.count()
        participants = room.participants.all()
        return render(request, 'room/room.html',
                      {'room': room, 'messages': messages, 'participants_count': participants_count,
                       'participants': participants})
    else:
        return HttpResponse("You are not a participant of this room.")


@login_required()
def delete_room(request, slug):
    room = Room.objects.get(slug=slug)
    room.delete()
    return redirect('user_rooms')


