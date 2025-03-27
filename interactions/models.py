from django.db import models
from accounts.models import Account
from posts.models import Post, Audience

class Comment(models.Model):
    content = models.CharField(max_length=255, default="")
    dateTime = models.DateTimeField(auto_now_add=True, null=True)
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

class Glow(models.Model):
    account = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.account.firstname} reacted to {self.post.caption}"

class Share(models.Model):
    account = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
    audience = models.ForeignKey(Audience, null=True, on_delete=models.CASCADE)
    caption = models.CharField(max_length=800, blank=True, default="")
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.account.firstname} shared {self.post.caption}"

