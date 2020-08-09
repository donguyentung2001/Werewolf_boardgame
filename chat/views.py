from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import GroupChat, Choice
from .serializers import UserSerializer, ChoiceSerializer
from django.contrib.auth.models import User
import random 
from django.http import HttpResponse
from django.shortcuts import redirect
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
           if request.user.character.role=="":
                request.user.character.role=random.choice(roles)
                request.user.character.save()
           real_participants.append(UserSerializer(request.user).data)
   else:
       real_participants=[]
       if request.user.character.role=="":
           request.user.character.role=random.choice(roles)
           request.user.character.save()
       real_participants.append(UserSerializer(request.user).data)
   werewolf_win="False" 
   villager_win="False" 
   werewolf_lives=0 
   villager_lives=0
   if len(real_participants)==2:
        for real_participant in real_participants: 
            if real_participant['character']['role']=="werewolf" and real_participant['character']['death']=="alive": 
                    werewolf_lives+=1
            elif real_participant['character']['role']!="werewolf" and real_participant['character']['death']=="alive": 
                    villager_lives+=1 
        if villager_lives<werewolf_lives: 
            werewolf_win="True"
        elif werewolf_lives==0: 
            villager_win="True" 
   return render(request, 'chat/room.html', {
       'room_name': room_name,
       "user": UserSerializer(request.user).data,
       "participants": real_participants, 
       "werewolf_win": werewolf_win, 
       "villager_win": villager_win
   })

@login_required
def werewolf_turn(request,room_name):
    if request.method=="POST": 
        url='/chat/' + str(room_name)+ '/'
        choices=request.session['choices']
        selected_option=request.POST['choices'] 
        if selected_option=='option1': 
            choices['option_one_count']+=1 
        if selected_option=='option2': 
            choices['option_two_count']+=1 
        if selected_option=='option3': 
            choices['option_three_count']+=1 
        highest_count=max([choices['option_one_count'],choices['option_two_count'],choices['option_three_count']])
        if highest_count==choices['option_one_count']: 
            dead_person=User.objects.filter(username=choices['option_one']).first()
            dead_person.character.death="Dead" 
            dead_person.character.save()
        if highest_count==choices['option_two_count']: 
            dead_person=User.objects.filter(username=choices['option_two']).first()
            dead_person.character.death="Dead" 
            dead_person.character.save()
        if highest_count==choices['option_three_count']: 
            dead_person=User.objects.filter(username=choices['option_three']).first()
            dead_person.character.death="Dead" 
            dead_person.character.save()
        return redirect(url)

    participants=GroupChat.objects.filter(name=room_name).first().users_list[1:]
    participants=participants.split(sep="%")
    real_participants=[]
    for participant in participants:
        real_participants.append(UserSerializer(User.objects.filter(username=participant).first()).data) 
    humans=[]
    for real_participant in real_participants: 
        if real_participant['character']['role']!='werewolf': 
            humans.append(real_participant)
    choices=Choice.objects.create()
    count=0
    for human in humans: 
        if count==0: 
            choices.option_one=human['username'] 
        if count==1: 
            choices.option_two=human['username'] 
        if count==2: 
            choices.option_three=human['username'] 
        count+=1 
    choices = ChoiceSerializer(choices).data
    request.session['choices']=choices
    return render(request,'chat/werewolf_turn.html', { 
        "room_name": room_name,
        "choices": choices  
    })

