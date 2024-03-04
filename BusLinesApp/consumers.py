import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ArrivalTimeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Implement logic to calculate and send real-time estimated arrival times
        await self.send(text_data=json.dumps({'arrival_times': arrival_times}))