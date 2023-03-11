from django import forms
from django.contrib.auth import get_user_model, authenticate, login
from django.core.exceptions import ValidationError
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

        self.cleaned_data.pop("c_password")
        return self.cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(**self.cleaned_data)
        return user


class AccountUpdateForm(forms.ModelForm):

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
            "email",
            "old_password",
            "password",
            "c_password",
            "first_name",
            "last_name",
            "institution"
        ]

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
        old_password = self.cleaned_data.pop("old_password")
        if not self.request.user.check_password(old_password):
            raise ValidationError("Invalid password")

        if self.cleaned_data["password"] != self.cleaned_data["c_password"]:
            raise ValidationError("Passwords Must Match")

        self.cleaned_data.pop("c_password")
        return self.cleaned_data


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
        print(user.backend)

        return super().clean()
