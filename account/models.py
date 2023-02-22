import os
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.db import models



def set_name(model, *args, **kwargs):
    username = model.username
    id = model.id
    return os.path.join("media", "profile-picture", f"{username}-{id}")

class Account(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid4)
    profile_picture = models.ImageField(upload_to=set_name, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    is_active = models.BooleanField(default=True)


    REQUIRED_FIELDS = ["email", "last_name", "first_name"]
    USERNAME_FIELD = "username"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)