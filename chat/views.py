from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import GroupChat, Choice, Game
from .serializers import UserSerializer, ChoiceSerializer
from django.contrib.auth.models import User
import random 
from django.http import HttpResponse
from django.shortcuts import redirect
@login_required
def index(request):
    for game in Game.objects.all().iterator(): 
        if request.user.username in game.participants: 
            game.delete()
    request.user.character.death="alive"
    request.user.character.role=""
    request.user.character.save()
    return render(request, 'chat/index.html')

@login_required
def room(request, room_name):
   if Game.objects.filter(name=room_name).count()==0: 
       current_game = Game.objects.create(name=room_name)
   current_game = Game.objects.filter(name=room_name).first()
   if request.user.username not in current_game.participants: 
       current_game.participants+="%"
       current_game.participants+=request.user.username 
   current_game.save()
   roles=['werewolf','villager',"villager","villager"]
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
   return render(request, 'chat/room.html', {
       'room_name': room_name,
       "user": UserSerializer(request.user).data,
       "participants": real_participants, 
   })

@login_required
def werewolf_turn(request,room_name):
    current_game=Game.objects.filter(name=room_name).first() 
    if request.method=="POST": 
        current_game.turn="villager"
        current_game.save()
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
            current_game.villager_num-=1 
            current_game.save()
        if highest_count==choices['option_two_count']: 
            dead_person=User.objects.filter(username=choices['option_two']).first()
            dead_person.character.death="Dead" 
            dead_person.character.save()
            current_game.villager_num-=1 
            current_game.save()
        if highest_count==choices['option_three_count']: 
            dead_person=User.objects.filter(username=choices['option_three']).first()
            dead_person.character.death="Dead" 
            dead_person.character.save()
            current_game.villager_num-=1 
            current_game.save()
        current_game.votes=""
        remained_players=current_game.werewolf_num + current_game.villager_num 
        for i in range(remained_players): 
            current_game.votes+="0"
            current_game.save()
        return redirect(url)

    current_game = Game.objects.filter(name=room_name).first() 
    choices=current_game.participants[1:].split("%")
    real_participants=[]
    for choice in choices:
        real_participants.append(UserSerializer(User.objects.filter(username=choice).first()).data) 
    humans=[]
    for real_participant in real_participants: 
        if real_participant['character']['role']!='werewolf' and real_participant['character']['death'] == "alive": 
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
    current_game=Game.objects.filter(name=room_name).first() 
    current_game.turn="werewolf"
    current_game.save()
    return render(request,'chat/werewolf_turn.html', { 
        "room_name": room_name,
        "choices": choices  
    })

@login_required
def check_turn(request,room_name): 
    current_game=Game.objects.filter(name=room_name).first()
    if current_game.villager_num == current_game.werewolf_num: 
        return HttpResponse("werewolf_win") 
    if current_game.werewolf_num == 0:
        return HttpResponse("villager_win")
    return HttpResponse(current_game.turn)

@login_required
def waiting_turn(request, room_name): 
    return render(request,'chat/waiting_turn.html', { 
        "room_name": room_name
    })

@login_required
def werewolf_win(request, room_name): 
    return render(request, 'chat/werewolf_win.html')


@login_required
def villager_win(request, room_name): 
    return render(request, 'chat/villager_win.html')

@login_required 
def villager_turn(request,room_name): 
    if request.method == 'POST': 
        url='/chat/' + str(room_name)+ '/wait_vote/'
        current_game = Game.objects.filter(name=room_name).first()  
        selected_option=request.POST['choices']
        if selected_option == "option0": 
            number = int(current_game.votes[0]) 
            number +=1 
            str_number=str(number)
            vote_list=list(current_game.votes)
            vote_list[0]=str_number 
            current_game.votes = "".join(vote_list)
            current_game.save()
        if selected_option == "option1": 
            number = int(current_game.votes[1]) 
            number +=1 
            str_number=str(number)
            vote_list=list(current_game.votes)
            vote_list[1]=str_number 
            current_game.votes = "".join(vote_list)
            current_game.save()
        if selected_option == "option2": 
            number = int(current_game.votes[2]) 
            number +=1 
            str_number=str(number)
            vote_list=list(current_game.votes)
            vote_list[2]=str_number 
            current_game.votes = "".join(vote_list)
            current_game.save()
        if selected_option == "option3": 
            number = int(current_game.votes[3]) 
            number +=1 
            str_number=str(number)
            vote_list=list(current_game.votes)
            vote_list[3]=str_number 
            current_game.votes = "".join(vote_list)
            current_game.save()
        return redirect(url)
    current_game = Game.objects.filter(name=room_name).first() 
    choices=current_game.participants[1:].split("%")
    for choice in choices: 
        if User.objects.filter(username=choice).first().character.death == "Dead": 
            choices.remove(choice)
    return render(request,'chat/villager_turn.html', { 
        "choices": choices,
    })

@login_required 
def check_votes(request, room_name): 
    current_game = Game.objects.filter(name=room_name).first() 
    vote_result=list(current_game.votes)
    count=0 
    for i in range(len(vote_result)): 
        vote_result[i] = int(vote_result[i])
        count+= vote_result[i]
    supposed_votes=current_game.villager_num + current_game.werewolf_num
    if current_game.turn == "": 
        return HttpResponse("True")
    if supposed_votes == count: 
        max_vote=-1
        for i in vote_result: 
            if i>max_vote: 
                max_vote=i 
        dead_index=vote_result.index(max_vote)
        choices=current_game.participants[1:].split("%")
        for choice in choices: 
            if User.objects.filter(username=choice).first().character.death == "Dead": 
                choices.remove(choice)
        dead_user=User.objects.filter(username=choices[dead_index]).first()
        dead_user.character.death = "Dead" 
        dead_user.character.save()
        for i in range(supposed_votes-1):
            current_game.save()
        if dead_user.character.role == "werewolf": 
            current_game.werewolf_num-=1 
            current_game.save()
        else: 
            current_game.villager_num-=1 
            current_game.save()
        current_game.turn = ""
        current_game.save()
        return HttpResponse("True")
    else: 
        return HttpResponse("False")

@login_required 
def wait_vote(request,room_name): 
    return render(request,'chat/wait_vote.html', {
        "room_name": room_name
    })

