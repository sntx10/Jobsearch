import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
import unittest
import asyncio
import pytest
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from apps.chat.consumers import ChatConsumer


class TestChat(unittest.TestCase):

    @pytest.mark.django_db(databases=['default'])
    @pytest.mark.asyncio
    async def test_chat(self):
        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/ws/work/")
        connected, _ = await communicator.connect()
        message = {'msg': 'Hello, world!', 'phone_number': '123-456-7890', 'city': 'New York', 'gender': 'Male',
                   'citizenship': 'USA'}
        await communicator.send_json_to(message)
        try:
            response = await asyncio.wait_for(communicator.receive_json_from(), timeout=60)
            print(response)
        except asyncio.TimeoutError:
            print("Timed out waiting for response")
        await communicator.disconnect()

    @pytest.mark.django_db(databases=['default'])
    @pytest.mark.asyncio
    async def test_channel_layer(self):
        channel_layer = get_channel_layer()
        channel_name = await channel_layer.new_channel()
        await channel_layer.send(
            'channel-1',
            {
                "type": "channel.ping",
                "channel": channel_name,
                "text": "This is a test"
            }
        )
        try:
            response = await asyncio.wait_for(channel_layer.receive(channel_name), 1)

        except asyncio.exceptions.TimeoutError:
            response = None

    @pytest.mark.asyncio
    async def test_my_consumer(self):
        from channels.testing import ApplicationCommunicator
        communicator = ApplicationCommunicator(ChatConsumer.as_asgi(), {
            "type": "websocket",
            "path": "/my-path/",
        })
        connected, _ = await communicator.connect()
        await communicator.send_json_to({
            "type": "my-message-type",
            "data": "my-message-data",
        })
        response = await communicator.receive_json_from()
        assert response == {
            "type": "my-response-type",
            "data": "my-response-data",
        }
        await communicator.disconnect()
