# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from .models import GroupChat
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        current_username=self.user.username
        added_user="%"+current_username
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        if GroupChat.objects.filter(name=self.room_name).count()!=0: 
            current_group=GroupChat.objects.filter(name=self.room_name).first()
            current_group.users_list+=added_user
            current_group.save()
        else: 
            current_group=GroupChat.objects.create(name=self.room_name,users_list=added_user)
            current_group.save()
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        #remove user from model, delete model if no user is in it
        self.user = self.scope["user"]
        current_username=self.user.username
        removed_user="%"+current_username
        current_group=GroupChat.objects.filter(name=self.room_name).first() 
        start=current_group.users_list.find(removed_user) 
        current_group.users_list=current_group.users_list[0:start] + current_group.users_list[(start+len(removed_user)):len(current_group.users_list)]
        current_group.save()
        if len(current_group.users_list)==0: 
            current_group.delete() 
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))