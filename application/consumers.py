import time
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ApplicationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.accept()
        for i in range(100):
            data=json.dumps({"message": "message "+str(i)})
            self.send(data)
            time.sleep(2)