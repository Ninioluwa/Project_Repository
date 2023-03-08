from django.urls import path
from .views import AccountLoginView, AccountCreationView, LogoutView, ProfileView

urlpatterns = [
    path("login/", AccountLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/<uuid:id>/", ProfileView.as_view(), name="account-profile"),
    path("register/", AccountCreationView.as_view(), name="register")
]
