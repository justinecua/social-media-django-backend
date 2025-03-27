from django.db import models
from django.conf import settings

class Account(models.Model):
    firstname = models.CharField(max_length=255, blank=True, default="")
    lastname = models.CharField(max_length=255, blank=True, default="")
    gender = models.CharField(max_length=75, blank=True, default="")
    age = models.IntegerField(null=True)
    birthday = models.DateField(null=True, blank=True)
    bio = models.CharField(max_length=255, blank=True, default="")
    ui_appearance = models.CharField(max_length=255, blank=True, default="")
    cover_photo = models.URLField(verbose_name="File URL", blank=True, default="")
    cover_photo_id_imagekit = models.CharField(max_length=355, null=True, blank=True, default="")
    profile_photo = models.URLField(verbose_name="File URL", default="")
    profile_photo_id_imagekit = models.CharField(max_length=355, null=True, blank=True, default="")
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    last_activity = models.DateTimeField(null=True, blank=True)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

