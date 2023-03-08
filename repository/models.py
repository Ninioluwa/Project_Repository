import os
import re
from uuid import uuid4
from datetime import datetime
from random import randint
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

from account.models import Institution

User = get_user_model()


def set_folder_name(model):
    title = model.id
    folder = os.path.join("repo", model.project_id)

    return folder


def set_cover_upload(model, filename):
    folder = set_folder_name(model)
    extension = filename.split(".")
    if len(extension) > 1:
        extension = extension[-1]
    else:
        extension = ""

    return os.path.join(folder, f"coverpage.{extension}")


def set_document_upload(model, filename):
    folder = set_folder_name(model)
    extension = filename.split(".")
    if len(extension) > 1:
        extension = extension[-1]
    else:
        extension = ""

    return os.path.join(folder, f"project.{extension}")


def year_validator(value):
    minimum_year = datetime.now().year - 20
    maximum_year = datetime.now().year

    if not re.match(r"\d{4}", value):
        raise ValidationError("Not a valid Year")

    if int(value) < minimum_year and int(value) > maximum_year:
        raise ValidationError("Resource too old")

    return value


class Department(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Project(models.Model):

    def set_id():
        return randint(int("1"*15), int("9"*15))

    id = models.IntegerField(primary_key=True, default=set_id)
    project_id = models.CharField(
        max_length=115, null=False, blank=False, unique=True)
    title = models.CharField(
        max_length=100, null=False, blank=False)
    institution = models.ForeignKey(
        to=Institution, on_delete=models.CASCADE, related_name="projects", null=False, blank=False)
    department = models.ForeignKey(
        to=Department, on_delete=models.CASCADE, null=False, blank=False, related_name="projects")
    scholar = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, null=True, related_name="projects")
    description = models.TextField(null=False, blank=False)
    cover_page = models.ImageField(
        upload_to=set_cover_upload, null=False, blank=False,
        validators=[FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    document = models.FileField(upload_to=set_document_upload, validators=[
                                FileExtensionValidator(['pdf'])])
    url = models.URLField(null=True)
    supervisor = models.CharField(max_length=50, null=False, blank=False)
    date_uploaded = models.DateTimeField(
        auto_now_add=True, null=False, blank=False)
    year_published = models.CharField(max_length=4, validators=[
                                      year_validator], null=False, blank=False)
    views = models.PositiveIntegerField(default=0, null=False, blank=False)
    plagiarism_score = models.FloatField(null=False, blank=False)
    tags = models.ManyToManyField(to=Tag, related_name="projects")

    def set_project_id(self):
        title = self.title.replace(" ", "-").lower()
        return f"{title}-{self.id}"

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        if not self.project_id:
            self.project_id = self.set_project_id()

        return super().save(**kwargs)
