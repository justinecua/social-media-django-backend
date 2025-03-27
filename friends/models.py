from django.db import models
from accounts.models import Account

class Friend(models.Model):
    user = models.ForeignKey(Account, related_name='user_friendships', null=True, on_delete=models.CASCADE)
    friend = models.ForeignKey(Account, related_name='friend_friendships', null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default="Pending")  # Pending, Accepted, Rejected
    date_friend_request = models.DateTimeField(auto_now_add=True, null=True)
    date_became_friends = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.firstname} sent a friend request to {self.friend.firstname}"

