from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class AppConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.room_group_name = "notifications"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def notify_event(self, event):
        data = event["data"]
        self.send_json(data)
