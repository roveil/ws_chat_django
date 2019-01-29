from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(JsonWebsocketConsumer):

    def connect(self):
        if self.scope["user"].is_anonymous:
            #TODO log this
            self.close()
        async_to_sync(self.channel_layer.group_add)("chat", self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("chat", self.channel_name)
        pass

    def chat_message(self, event):
        self.send_json(event["data"])

# for handle incoming packets use recieve_json(self, content)