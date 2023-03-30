import os
import shutil
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Project


@receiver(post_delete, sender=Project)
def delete_project(sender, instance, **kwargs):
    # get parent directory of document
    dir = os.sep.join(instance.document.path.split(os.sep)[:-1])
    # removes directory and contents inside

    shutil.rmtree(dir)
