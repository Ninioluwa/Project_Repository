from django.urls import path

from .views import CreateProjectView, DisplayProjectView, ProjectDetailView

urlpatterns = [
    path("create/", CreateProjectView.as_view(), name="project-create"),
    path("display-projects/", DisplayProjectView.as_view(), name="display-projects"),
    path("<int:id>/", ProjectDetailView.as_view(), name="project-detail")
]
