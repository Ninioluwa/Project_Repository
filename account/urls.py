from django.urls import path
from .views import AccountLoginView, AccountCreationView, LogoutView

urlpatterns = [
    path("login/", AccountLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", AccountCreationView.as_view(), name="register")
]
