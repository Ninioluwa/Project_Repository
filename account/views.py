from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404, render
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import AccountCreationForm, AccountLoginForm, AccountUpdateForm


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


class ProfileView(LoginRequiredMixin, generic.DetailView):
    template_name = 'viewprofile.html'
    context_object_name = 'account'

    def get_object(self):

        Account = get_user_model()
        id = self.kwargs["id"]

        return get_object_or_404(Account, id=id)


class UpdateProfileView(LoginRequiredMixin, generic.FormView):
    template_name = "updateprofile.html"
    form_class = AccountUpdateForm
    success_url = reverse_lazy("account-profile")

    def get_initial(self):
        user = self.request.user
        initial = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "institution": user.institution
        }
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request

        return kwargs

    def get(self, request):

        form = self.get_form()

        return render(request, self.template_name, context={"form": form})


class LogoutView(LoginRequiredMixin, generic.TemplateView):

    template_name = 'logout.html'

    def post(self, request):
        logout(self.request)
        return redirect(settings.LOGOUT_REDIRECT_URL)
