from django.urls import path

from .views import CreateProjectView, DisplayProjectView

urlpatterns = [
    path("create/", CreateProjectView.as_view(), name="project-create"),
    path("display-projects/", DisplayProjectView.as_view(), name="display-projects")
]
