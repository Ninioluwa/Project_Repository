# Generated by Django 4.1.5 on 2023-04-14 19:27

from django.db import migrations, models
import repository.models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0005_alter_project_similarity_check_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='file_id',
            field=models.SlugField(default=None, max_length=33, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='job_id',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='cover_page',
            field=models.ImageField(default=None, null=True, upload_to=repository.models.set_cover_upload),
        ),
    ]
