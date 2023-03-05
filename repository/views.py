from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.core.paginator import Paginator

from .forms import ProjectForm
from .models import Project, Tag


class CreateProjectView(LoginRequiredMixin, generic.CreateView):

    form_class = ProjectForm
    template_name = 'createproject.html'
    success_url = reverse_lazy("home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request

        return kwargs


class DisplayProjectView(LoginRequiredMixin, generic.ListView):

    context_object_name = "projects"
    template_name = "displayprojects.html"
    paginate_by = 10

    def get_queryset(self):
        filter = self.request.GET.get("filter", None)
        if not filter:
            return Project.objects.all()

        search = self.request.GET.get("search", None)
        allowed_filters = [
            "year",
            "title",
            "supervisor",
            "department"
        ]

        if filter not in allowed_filters:

            return Project.objects.all()

        if filter == "year":
            query = Project.objects.filter(year=search)

        elif filter == "title":
            query = Project.objects.filter(title__icontains=search)

        elif filter == "department":
            query = Project.objects.filter(department__name__icontains=search)

        elif filter == "supervisor":
            query = Project.objects.filter(
                supervisor__icontains=search)

        return query

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
