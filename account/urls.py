from django.urls import path
from .views import AccountLoginView, AccountCreationView

urlpatterns = [
    path("login/", AccountLoginView.as_view(), name="login"),
    path("register/", AccountCreationView.as_view(), name="register")
]