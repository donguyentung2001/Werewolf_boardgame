from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import GroupChat
# Create your views here.

@login_required
def index(request):
    return render(request, 'chat/index.html')

@login_required
def room(request, room_name):
    if GroupChat.objects.filter(name=room_name).count()!=0:
        participants=GroupChat.objects.filter(name=room_name).first().users_list[1:]
        participants=participants.split(sep="%")
        participants.append(request.user.username)
        real_participants=[] 
        for participant in participants: 
            if participant not in real_participants: 
                real_participants.append(participant)
    else: 
        real_participants=[]
        real_participants.append(request.user.username)

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        "username": request.user.username,
        "participants": real_participants 
    })
