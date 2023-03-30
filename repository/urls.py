from django.urls import path

from .views import CreateProjectView, DisplayProjectView, ProjectDetailView, UpdateProjectView, deleteview

urlpatterns = [
    path("create/", CreateProjectView.as_view(), name="project-create"),
    path("display-projects/", DisplayProjectView.as_view(), name="display-projects"),
    path("edit/<int:pk>/", UpdateProjectView.as_view(), name="update-project"),
    path("delete/<int:id>/", deleteview, name="delete-project"),
    path("<int:id>/", ProjectDetailView.as_view(), name="project-detail")
]
