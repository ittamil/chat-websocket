import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
# from accounts.models import User
from django.contrib.auth.models import User

from .models import ChatMessage,Thread
import timeago, datetime
from django.template.loader import render_to_string

from channels.db import database_sync_to_async

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        # user = self.scope['user']
        # if user.is_authenticated:  
        #     self.update_user_status(user, True)
            

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

        # user = self.scope['user']
        # if user.is_authenticated:
        #     self.update_user_status(user, False)
            
        
    # Receive message from WebSocket
    def receive(self, text_data):
        if self.scope['user'] != "AnonymousUser":
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            username_text = text_data_json['username']
            room_name = self.scope['url_route']['kwargs']['room_name']
            thread = Thread.objects.get(threadname = room_name)        
            username = User.objects.get(username = username_text)
            chatmessage = ChatMessage.objects.create(thread = thread , user = username , message = message)
            convert_str = str(chatmessage.timestamp)
            
            datetime_split = convert_str.split('.')
    
            datetime_convert_properformat = datetime.datetime.strptime(datetime_split[0], "%Y-%m-%d %H:%M:%S")

            date = datetime.datetime.now()
            timestamp = timeago.format(date, datetime_convert_properformat)

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username':username_text,
                    'timestamp': str(timestamp)
                }
            )
        else:
            pass

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        username = event['username']
        timestamp = event['timestamp']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username':username,
            'timestamp':timestamp
        }))
        
        

    # def update_user_status(self, user, status):
    #     return User.objects.filter(id = user.pk).update(status = status)