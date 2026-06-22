import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .state import get_scoreboard_state

class ScoreboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "scoreboard_group"
        
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        
        async_get_scoreboard_state = database_sync_to_async(get_scoreboard_state)
        scoreboard_state = await async_get_scoreboard_state()
        await self.send(text_data=json.dumps(scoreboard_state))
        
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        
    async def scoreboard_update(self, event):
        await self.send(text_data=json.dumps(event['data']))