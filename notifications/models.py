from django.db import models
from friends.models import Friend

class Notification(models.Model):
    content = models.CharField(max_length=255, default="")
    status = models.CharField(max_length=100, default="Unread")
    friend_request = models.ForeignKey(Friend, null=True, on_delete=models.CASCADE, related_name='notifications')

    def __str__(self):
        return self.content

