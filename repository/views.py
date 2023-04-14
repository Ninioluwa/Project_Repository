from django.shortcuts import get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy

from .forms import ProjectForm, UpdateProjectForm
from .models import Project, Tag


class CreateProjectView(LoginRequiredMixin, generic.CreateView):

    form_class = ProjectForm
    template_name = 'createproject.html'
    object = None

    def get_success_url(self) -> str:
        id = self.request.user.id
        return reverse_lazy("account-profile", kwargs={"id": id})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request

        return kwargs


class DisplayProjectView(generic.ListView):

    context_object_name = "projects"
    template_name = "displayprojects.html"
    paginate_by = 9

    def get_queryset(self):
        filter = self.request.GET.get("filter", None)
        queryset = Project.objects.filter(status="verified")
        if not filter:
            return queryset.order_by('date_uploaded')

        search = self.request.GET.get("search", None)
        allowed_filters = [
            "year",
            "title",
            "supervisor",
            "department"
        ]

        if filter not in allowed_filters:

            return queryset.order_by('date_uploaded')

        if filter == "year":
            query = queryset.filter(year_published=search)

        elif filter == "title":
            query = queryset.filter(title__icontains=search)

        elif filter == "department":
            query = queryset.filter(department__name__icontains=search)

        elif filter == "supervisor":
            query = queryset.filter(
                supervisor__icontains=search)

        return query.order_by('date_uploaded')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest"] = Project.objects.all().order_by(
            'date_uploaded').last()

        return context

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):

    template_name = 'projectdetail.html'
    context_object_name = 'project'

    def get_object(self):
        id = self.kwargs["id"]
        project = get_object_or_404(Project, id=id)
        if self.request.user != project.scholar:
            project.views += 1
            project.save()

        return project


@login_required
def deleteview(request, *args, **kwargs):
    if request.method != "GET":
        return HttpResponse("Invalid", status=405)

    id = kwargs["id"]
    project = get_object_or_404(Project, id=id)

    if project.scholar != request.user:
        return HttpResponse("Invalid", status=405)

    project.delete()

    return redirect(reverse_lazy("account-profile", kwargs={"id": request.user.id}))


class UpdateProjectView(LoginRequiredMixin, generic.UpdateView):

    template_name = 'editproject.html'
    form_class = UpdateProjectForm

    def get_queryset(self):
        return Project.objects.filter(scholar=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        kwargs["instance"] = self.get_queryset().get(id=self.kwargs["pk"])

        return kwargs

    def get_success_url(self) -> str:
        return reverse_lazy('project-detail', kwargs={"id": self.kwargs["pk"]})
