import os
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.db import models


class Institution(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


def set_name(model, filename):
    username = model.username
    id = model.id
    extension = filename.split(".")[-1]
    return os.path.join("profile-picture", f"{username}-{id}.{extension}")


class Account(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid4)
    profile_picture = models.ImageField(
        upload_to=set_name, null=False, blank=False, default=os.path.join("profile-picture", "avatar.png"))
    last_name = models.CharField(max_length=50, null=False, blank=False)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    institution = models.ForeignKey(
        to=Institution, null=False, blank=False, on_delete=models.CASCADE)

    @ property
    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'

    def __str__(self):
        return self.get_full_name

    REQUIRED_FIELDS = ["email", "last_name", "first_name"]
    USERNAME_FIELD = "username"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
