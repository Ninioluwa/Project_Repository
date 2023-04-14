import os
import shutil
from django.db.models.signals import post_delete, post_save
from django.conf import settings
from django.dispatch import receiver

from .models import Project
from .plagrism import Plagiarism


@receiver(post_delete, sender=Project)
def delete_project(sender, instance, **kwargs):
    ...
    # if not settings.DEBUG:
    #     return
    # # get parent directory of document
    # dir = os.sep.join(instance.document.path.split(os.sep)[:-1])
    # # removes directory and contents inside

    # shutil.rmtree(dir)


@receiver(post_save, sender=Project)
def run_plagiarism_check(sender, instance, **kwargs):
    if kwargs["created"]:
        plagiarism = Plagiarism()
        plagiarism.upload_file(instance)
        plagiarism.start_plagiarism_check(instance)
        instance.save()
