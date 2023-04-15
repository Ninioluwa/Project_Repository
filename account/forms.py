from django import forms
from django.contrib.auth import get_user_model, authenticate, login
from django.core.exceptions import ValidationError

from .models import Account
User = get_user_model()


class AccountCreationForm(forms.ModelForm):

    c_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-3 py-2 mb-3 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:border-indigo-500 focus:outline-none focus:shadow-outline",
                "placeholder": "*"*20
            }
        )
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "c_password",
            "first_name",
            "last_name",
            "institution"
        ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget = forms.TextInput(
            attrs={
                "class": "w-full px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:border-indigo-500 focus:outline-none focus:shadow-outline",
                "placeholder": "First Name"
            }
        )
        self.fields["last_name"].widget = forms.TextInput(
            attrs={
                "class": "w-full px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:border-indigo-500 focus:outline-none focus:shadow-outline",
                "placeholder": "Last Name"
            }
        )
        self.fields["username"].widget = forms.TextInput(
            attrs={
                "class": "w-full px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:border-indigo-500 focus:outline-none focus:shadow-outline",
                "placeholder": "Username"
            }
        )
        self.fields["email"].widget = forms.TextInput(
            attrs={
                "class": "w-full px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:border-indigo-500 focus:outline-none focus:shadow-outline",
                "placeholder": "user@gmail.com"
            }
        )
        self.fields["password"].widget = forms.PasswordInput(
            attrs={
                "class": "w-full px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:border-indigo-500 focus:outline-none focus:shadow-outline",
                "placeholder": "*"*20
            }
        )

        self.fields["institution"].widget.attrs = {
            "class": "w-full px-3 py-2 mb-3 text-sm leading-tight focus:border-indigo-500 focus:outline-none bg-white text-black border rounded shadow focus:shadow-outline"
        }

    def clean(self):
        if self.cleaned_data["password"] != self.cleaned_data["c_password"]:
            raise ValidationError("Passwords Must Match")
        
        if Account.objects.filter(username=self.cleaned_data["username"]).exists():
            raise ValidationError({"username": "Invalid Username Already exists"})

        if Account.objects.filter(email=self.cleaned_data["email"]).exists():
            raise ValidationError({"email": "Invalid Email Already exists"})

        self.cleaned_data.pop("c_password")
        return self.cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(**self.cleaned_data)
        return user


class ChangePasswordForm(forms.ModelForm):

    old_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-3 py-2 mb-3 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:border-indigo-500 focus:outline-none focus:shadow-outline",
                "placeholder": "*"*20
            }
        )
    )
    c_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-3 py-2 mb-3 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:border-indigo-500 focus:outline-none focus:shadow-outline",
                "placeholder": "*"*20
            }
        )
    )

    class Meta:
        model = User
        fields = [
            "old_password",
            "password",
            "c_password",
        ]

    def __init__(self, request=None, *args, **kwargs) -> None:
        self.request = request

        super().__init__(*args, **kwargs)

        self.fields["password"].widget = forms.PasswordInput(
            attrs={
                "class": "w-full px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:border-indigo-500 focus:outline-none focus:shadow-outline",
                "placeholder": "*"*20
            }
        )

    def clean(self):
        old_password = self.cleaned_data.pop("old_password")
        if not self.request.user.check_password(old_password):
            raise ValidationError("Invalid password")

        if self.cleaned_data["password"] != self.cleaned_data["c_password"]:
            raise ValidationError("Passwords Must Match")

        self.cleaned_data.pop("c_password")
        return self.cleaned_data

    def save(self, *args, **kwargs):
        self.instance.set_password(self.cleaned_data["password"])
        self.instance.save()

        return self.instance


class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "institution"
        ]

    def clean_email(self):
        user = self.request.user

        email = self.cleaned_data["email"]

        users = User.objects.filter(email__iexact=email).exclude(
            username__iexact=user.username)
        if users:
            raise forms.ValidationError(
                "User with this email already exists.")

        return email.lower()

    def __init__(self, request=None, *args, **kwargs) -> None:
        self.request = request

        super().__init__(*args, **kwargs)

        self.fields["first_name"].widget = forms.TextInput(
            attrs={
                "class": "w-full px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:border-indigo-500 focus:outline-none focus:shadow-outline",
                "placeholder": "First Name"
            }
        )
        self.fields["last_name"].widget = forms.TextInput(
            attrs={
                "class": "w-full px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:border-indigo-500 focus:outline-none focus:shadow-outline",
                "placeholder": "Last Name"
            }
        )
        self.fields["email"].widget = forms.TextInput(
            attrs={
                "class": "w-full px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:border-indigo-500 focus:outline-none focus:shadow-outline",
                "placeholder": "user@gmail.com"
            }
        )

        self.fields["institution"].widget.attrs = {
            "class": "w-full px-3 py-2 mb-3 text-sm leading-tight focus:border-indigo-500 focus:outline-none bg-white text-black border rounded shadow focus:shadow-outline"
        }


class ChangeProfilePictureForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "profile_picture"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["profile_picture"].widget = forms.FileInput(attrs={
            "class": "block w-full mb-3 text-sm text-gray-900 bg-indigo-100 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none",
            "accept": ".png, .jpg",
            "type": "file"
        })


class AccountLoginForm(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-2 py-4 mb-4 text-lg leading-tight text-gray-700 border rounded shadow appearance-none focus:border-indigo-500 focus:outline-none focus:shadow-outline",
                "placeholder": "Email/Username"
            }),
        max_length=150,
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-3 py-4 mb-3 text-lg leading-tight text-gray-700 border rounded shadow appearance-none focus:border-indigo-500 focus:outline-none focus:shadow-outline",
                "placeholder": "*"*20
            }),
        required=True,
        max_length=150
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.request = request

    def clean(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]

        user = authenticate(request=self.request,
                            username=username, password=password)

        if not user:
            raise forms.ValidationError("Invalid Credentials")

        login(request=self.request, user=user)

        return super().clean()
