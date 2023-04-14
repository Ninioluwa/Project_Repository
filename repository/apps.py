from django.apps import AppConfig


class RepositoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'repository'

    def ready(self):
        from .signals import delete_project, run_plagiarism_check
        delete_project
        run_plagiarism_check
