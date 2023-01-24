import os
import re
from uuid import uuid4
from datetime import datetime
from random import randint
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

def set_folder_name(model):
    title = model.id
    folder = os.path.join("repo", title)
        
    return folder

def set_cover_upload(model, *args, **kwargs):
    folder = set_folder_name(model)
    return os.path.join(folder, "coverpage")

def set_document_upload(model, filename):
    folder = set_folder_name(model)

    return os.path.join(folder, "project")

def year_validator(value):
    minimum_year = datetime.now().year - 20
    maximum_year = datetime.now().year

    if not re.match(r"\d{4}", value):
        raise ValidationError("Not a valid Year")
    
    if int(value) < minimum_year and int(value) > maximum_year:
        raise ValidationError("Resource too old")

    return value
        

class Project(models.Model):

    id = models.CharField(max_length=130, primary_key=True, unique=True)
    title = models.CharField(max_length=100)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=False, blank=False)
    cover_page = models.ImageField(upload_to=set_cover_upload, null=True)
    document = models.FileField(upload_to=set_document_upload)
    url = models.URLField(null=True)
    author = models.JSONField(null=False)
    citation = models.TextField(null=False, blank=False)
    supervisor = models.CharField(max_length=50, null=False, blank=False)
    date_uploaded = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    year_published = models.CharField(max_length=4,validators=[year_validator], null=False, blank=False)

    def set_id(self):
        title = self.title.replace(" ", "-").lower()
        rand_id = randint(11111111, 99999999)

        id = f"{title}-{rand_id}"

        while(Project.objects.filter(id=id).exists()):
            
            rand_id = randint(11111111, 99999999)
            id = f"{title}-{rand_id}"
        
        return id
            

    def save(self, **kwargs):
        if not self.id:
            self.id = self.set_id()

        return super().save(**kwargs)

class Tag(models.Model):
    name = models.CharField(max_length=30)
    projects = models.ManyToManyField(to=Project, related_name="tags")


    
class Institution(models.Model):

    def set_uuid():
        uuid = uuid4()

        while(Institution.objects.exists(id=uuid).exists()):
            uuid = uuid4()

        return uuid
    id = models.UUIDField(primary_key=True, default=set_uuid, unique=True, blank=False, null=False)
    name = models.CharField(max_length=100, null=False, blank=False)