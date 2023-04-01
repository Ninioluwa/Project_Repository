import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'private'
    file_overwrite = True


class OverWriteStorage(FileSystemStorage):

    def get_available_name(self, name, *args, **kwargs):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name
