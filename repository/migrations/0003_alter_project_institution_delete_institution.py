# Generated by Django 4.1.5 on 2023-02-24 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_institution_account_institution'),
        ('repository', '0002_department_rename_user_project_scholar_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='account.institution'),
        ),
        migrations.DeleteModel(
            name='Institution',
        ),
    ]