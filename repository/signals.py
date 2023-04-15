import os
import shutil
from django.db.models.signals import post_delete, post_save
from django.conf import settings
from django.dispatch import receiver
from django.core.mail import send_mail

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
        instance.save()
        plagiarism.re_authenticate()
        plagiarism.start_plagiarism_check(instance)

        send_mail(subject="Debug Testing", message="sent the start plagrism",
                  from_email=settings.EMAIL_HOST_USER, recipient_list=["toluhunter19@gmail.com"])
        instance.save()
