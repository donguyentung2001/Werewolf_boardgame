from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import GroupChat
from .serializers import UserSerializer
from django.contrib.auth.models import User

@login_required
def index(request):
    return render(request, 'chat/index.html')

@login_required
def room(request, room_name):
    if GroupChat.objects.filter(name=room_name).count()!=0:
        participants=GroupChat.objects.filter(name=room_name).first().users_list[1:]
        participants=participants.split(sep="%")
        real_participants=[] 
        for participant in participants: 
            real_participants.append(UserSerializer(User.objects.filter(username=participant).first()).data)
        if UserSerializer(request.user).data not in real_participants: 
            real_participants.append(UserSerializer(request.user).data)
    else: 
        real_participants=[]
        real_participants.append(UserSerializer(request.user).data)

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        "username": request.user.username,
        "participants": real_participants 
    })
