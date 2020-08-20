from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/',views.room,name='room'), 
    path('<str:room_name>/werewolf/',views.werewolf_turn,name="werewolf_turn"),
    path('<str:room_name>/check_turn/',views.check_turn,name="check_turn"), 
    path('<str:room_name>/waiting_turn/',views.waiting_turn,name="waiting_turn"),
    path('<str:room_name>/werewolf_win/',views.werewolf_win,name="werewolf_win"),
    path('<str:room_name>/villager_win/',views.villager_win,name="villager_win"),
    path('<str:room_name>/villager_turn/',views.villager_turn,name="villager_turn"),
    path('<str:room_name>/wait_vote/',views.wait_vote,name="wait_vote"),
    path('<str:room_name>/check_votes/',views.check_votes,name="check_votes"),
]