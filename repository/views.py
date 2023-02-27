from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import ProjectForm

class CreateProjectView(LoginRequiredMixin, generic.FormView):

    form_class = ProjectForm
    template_name = 'createproject.html'
    success_url = reverse_lazy("home")