# Generated by Django 4.1.5 on 2023-04-14 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0003_project_similarity_check_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='similarity_check_id',
            field=models.SlugField(default=None, null=True),
        ),
    ]
