from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import logout

from django.shortcuts import redirect, get_object_or_404, render
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AccountCreationForm, AccountLoginForm, AccountUpdateForm, ChangePasswordForm, ChangeProfilePictureForm


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
        kwargs["instance"] = self.request.user

        return kwargs

    def get_context_data(self, **kwargs):
        context = super(generic.FormView, self).get_context_data()
        context["form"] = self.form_class(
            self.request, instance=self.request.user)
        context["password"] = ChangePasswordForm(
            self.request, instance=self.request.user)
        context["profile"] = ChangeProfilePictureForm(
            self.request, instance=self.request.user
        )
        return context

    def get(self, request):

        return render(request, self.template_name, context=self.get_context_data())

    def post(self, request):
        form = None
        if "user_detail" in request.POST:
            form = self.get_form()

        elif "change_password" in request.POST:
            form = ChangePasswordForm(
                self.request, request.POST, instance=self.request.user)

        elif "profile_pic_btn" in request.POST:
            form = ChangeProfilePictureForm(
                files=request.FILES, data=request.POST, instance=self.request.user
            )

        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):

        form.save()
        if isinstance(form, ChangePasswordForm):
            logout(request=self.request)
            return redirect(reverse_lazy("home"))

        return redirect(reverse_lazy("account-profile", kwargs={"id": self.request.user.id}))

    def form_invalid(self, form):
        context = self.get_context_data()
        if isinstance(form, ChangePasswordForm):
            context["password"] = form
        elif isinstance(form, AccountUpdateForm):
            context["form"] = form
        elif isinstance(form, ChangeProfilePictureForm):
            context["profile"] = form

        return render(self.request, self.template_name, context=context)


class LogoutView(LoginRequiredMixin, generic.TemplateView):

    template_name = 'logout.html'

    def post(self, request):
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)
