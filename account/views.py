from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

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


class LogoutView(LoginRequiredMixin, generic.TemplateView):

    template_name = 'logout.html'

    def post(self, request):
        logout(self.request)
        return redirect(settings.LOGOUT_REDIRECT_URL)
