from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    moderator = models.BooleanField(default=False)
    display_name = models.CharField(max_length=128, null=False)
    google_id = models.TextField(max_length=64, default="", blank=True, null=True)
