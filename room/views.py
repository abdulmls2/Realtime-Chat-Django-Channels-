from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import Room, Message
import uuid


# list of rooms view
@login_required
def user_rooms(request):
    if request.method == 'POST':
        action = request.POST.get('action', '')

        # If the action is 'join', add the user to the specified room
        if action == 'join':
            slug = request.POST.get('room_slug', '')
            try:
                room = Room.objects.get(slug=slug)
                room.participants.add(request.user)
            except Room.DoesNotExist:
                pass  # Handle this case as needed

        # If the action is 'create', create a new room and add the user to it
        elif action == 'create':
            room_name = request.POST.get('room_name', '')

            # Generate a unique slug(id) for the new room
            slug = str(uuid.uuid4().int)[:5]

            # Check if a room with the same slug already exists
            if not Room.objects.filter(slug=slug).exists():
                new_room = Room.objects.create(name=room_name, slug=slug, owner=request.user)
                new_room.participants.add(request.user)
                return redirect('user_rooms')

    # Retrieve the rooms that the user is a participant of
    user_rooms = Room.objects.filter(participants=request.user)

    # Render the user's rooms view
    return render(request, 'room/rooms.html', {'user_rooms': user_rooms})


# Room detail view
@login_required
def room(request, slug):
    room = get_object_or_404(Room, slug=slug)

    if request.user in room.participants.all():
        # If the user is a participant of the room, retrieve messages and participants
        messages = Message.objects.filter(room=room)
        participants_count = room.participants.count()
        participants = room.participants.all()

        # Render the room view
        return render(request, 'room/room.html',
                      {'room': room, 'messages': messages, 'participants_count': participants_count,
                       'participants': participants})
    else:
        # If the user is not a participant of the room, display an error message
        return HttpResponse("You are not a participant of this room.")


# Room delete view
@login_required()
def delete_room(request, slug):
    room = Room.objects.get(slug=slug)
    room.delete()
    return redirect('user_rooms')
