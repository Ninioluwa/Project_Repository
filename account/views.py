from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import AccountCreationForm, AccountLoginForm


class AccountCreationView(generic.CreateView):

    form_class = AccountCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

class AccountLoginView(generic.FormView):

    form_class = AccountLoginForm
    template_name = "registration/login.html"
    success_url = reverse_lazy("home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request

        return kwargs
