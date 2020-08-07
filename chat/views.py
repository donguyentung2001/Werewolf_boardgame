from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import GroupChat
from .serializers import UserSerializer
from django.contrib.auth.models import User
import random 
@login_required
def index(request):
    return render(request, 'chat/index.html')

@login_required
def room(request, room_name):
   roles=['werewolf','villager','villager','villager']
   if GroupChat.objects.filter(name=room_name).count()!=0:
       participants=GroupChat.objects.filter(name=room_name).first().users_list[1:]
       participants=participants.split(sep="%")
       real_participants=[]
       for participant in participants:
           real_participants.append(UserSerializer(User.objects.filter(username=participant).first()).data)
       #remove taken roles from original list "roles"
       for real_participant in real_participants:
           roles.remove(real_participant['character']['role'])
       if UserSerializer(request.user).data not in real_participants:
           request.user.character.role=random.choice(roles)
           request.user.character.save()
           real_participants.append(UserSerializer(request.user).data)
   else:
       real_participants=[]
       if request.user.character.role=="":
           request.user.character.role=random.choice(roles)
           request.user.character.save()
       real_participants.append(UserSerializer(request.user).data)
 
   return render(request, 'chat/room.html', {
       'room_name': room_name,
       "user": UserSerializer(request.user).data,
       "participants": real_participants
   })
