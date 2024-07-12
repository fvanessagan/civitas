from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomGroupName = "groupchat"
        await self.channel_layer.group_add(self.roomGroupName, self.channel_name)
        await self.accept()

    async def disconnect(self , close_code):
        await self.channel_layer.group_discard(self.roomGroupName, self.channel_layer )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_cont = text_data_json["message_cont"]
        user = text_data_json["user"]
        await self.channel_layer.group_send(
            self.roomGroupName,{"type" : "sendMessage", "message_cont" : message_cont, "user" : user})
    
    async def sendMessage(self , event) : 
        message_cont = event["message_cont"]
        user = event["user"]
        await self.send(text_data = json.dumps({"message_cont":message_cont ,"user":user}))