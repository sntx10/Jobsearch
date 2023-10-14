import json
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from .models import Chat


User = get_user_model()

class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self): # подключение
        print("Websocket connect!")
        await database_sync_to_async(self.get_user)()
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def receive_json(self, content, **kwargs):
        if content['msg'] is not None:
            phone_number = content.get('phone_number', '')
            city = content.get('city', '')
            gender = content.get('gender', '')
            citizenship = content.get('citizenship', '')
            await database_sync_to_async(save_to_database)(self, content, phone_number, city, gender, citizenship)
            await self.channel_layer.group_send(self.room_name,
                                                {
                                                    'type': 'chat.message',
                                                    'msg': content['msg']
                                                })

    async def disconnect(self, close_code): # отключение
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        self.close()
        raise StopConsumer()

    async def chat_message(self, event):
        msg = json.dumps({'msg': event['msg']})
        await self.send(msg)

    @database_sync_to_async
    def get_user(self):
        if "sessionid" in self.scope["cookies"]:
            session_key = self.scope["cookies"]["sessionid"]
            session = Session.objects.get(session_key=session_key)
            uid = session.get_decoded().get("_auth_user_id")
            if uid is not None:
                return User.objects.get(pk=uid)
        return None

    async def connect(self):
        self.user = await self.get_user()

def save_to_database(self, content, phone_number, city, gender, citizenship):
    group = Chat.objects.get(name=self.room_name)
    profile = User.objects.get(user=self.user)
    chat = Chat.objects.create(
        content=content['msg'],
        phone_number=phone_number,
        city=city,
        gender=gender,
        citizenship=citizenship,
        sender=profile,
        recipient=group
    )
    chat.save()
