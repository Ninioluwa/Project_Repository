# Generated by Django 4.1.5 on 2023-04-15 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0006_project_file_id_project_job_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='job_id',
        ),
    ]
