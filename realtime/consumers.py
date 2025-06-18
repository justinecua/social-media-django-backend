from urllib.parse import parse_qs
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from friends.queries import (
    addFriend,
    cancelFriendRequest,
    acceptFriend,
    unfriend,
)

from notifications.queries import (
    showNotificationsByUser,
    countNotifications
)

ACTIONS = {
    "add_friend_result": addFriend,
    "cancel_friend_request": cancelFriendRequest,
    "accept_friend_result": acceptFriend,
    "unfriend": unfriend,
}

class GlobalConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope["query_string"].decode()
        query_params = parse_qs(query_string)
        self.user_id = query_params.get("user_id", [None])[0]

        self.room_group_name = f"user_{self.user_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        print(f"[WebSocket] User connected: user_id={self.user_id}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Checks what type of event was sent, calls the correct function
    async def receive(self, text_data):
        data = json.loads(text_data)
        event_type = data.get("type")
        friend_id = data.get("friend_id")
        user_id = data.get("user_id")

        handler = ACTIONS.get(event_type)
        if handler:
            result = await sync_to_async(handler, thread_sensitive=True)(friend_id, user_id)
            await self.notify_both(event_type, result, user_id, friend_id)

    # Sends message to both users
    async def notify_both(self, event_type, result, user_id, friend_id):
        for uid, fid in [(user_id, friend_id), (friend_id, user_id)]:
            await self.channel_layer.group_send(
                f"user_{uid}",
                {
                    "type": event_type,
                    "status": result["status"],
                    "message": result["message"],
                    "friend_id": fid,
                }
            )

            await self.channel_layer.group_send(
                f"user_{uid}",
                {
                    "type": "refresh_friend_status",
                    "user_id": user_id,
                    "friend_id": friend_id,
                }
            )

            # Notify receiver
            notification_count = await sync_to_async(countNotifications)(friend_id)
            notifications = await sync_to_async(showNotificationsByUser)(friend_id)

            await self.channel_layer.group_send(
                f"user_{friend_id}",
                {
                    "type": "new_notification",
                    "from_user_id": user_id,
                    "count": notification_count,
                    "notifications": notifications
                }
            )

    #Functions to handle what happens when the group message is received
    async def add_friend_result(self, event):
        await self.send(text_data=json.dumps(event))

    async def cancel_friend_request(self, event):
        await self.send(text_data=json.dumps(event))

    async def accept_friend_result(self, event):
        await self.send(text_data=json.dumps(event))

    async def unfriend(self, event):
        await self.send(text_data=json.dumps(event))
    
    async def refresh_friend_status(self, event):
        await self.send(text_data=json.dumps(event))

    async def new_notification(self, event):
        await self.send(text_data=json.dumps({
            "type": "notification",
            "status": event["status"],
            "message": event["message"],
            "from_user_id": event["from_user_id"],
            "count": event["count"],
            "notifications": event["notifications"]
        }))