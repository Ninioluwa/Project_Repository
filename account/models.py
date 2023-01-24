import os
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.db import models



def set_name(model, *args, **kwargs):
    username = model.username
    id = model.id
    return os.path.join("media", "profile-picture", f"{username}-{id}")

class Account(AbstractUser):

    def set_uuid(self):
        uuid = uuid4()

        while(self.objects.filter(id=uuid).exists()):
            uuid = uuid4()
        
        return uuid

    id = models.UUIDField(primary_key=True, unique=True, null=False)
    profile_picture = models.ImageField(upload_to=set_name)

    def save(self, *args, **kwargs):

        self.id = self.set_uuid()

        return super().save(*args, **kwargs)