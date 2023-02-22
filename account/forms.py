from django import forms
from django.contrib.auth import get_user_model, authenticate, login
User = get_user_model()

class AccountCreationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            ]

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
                "placeholder": "Password"
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

        user = authenticate(request=self.request, username=username, password=password)
        print(user)

        if not user:
            raise forms.ValidationError("Invalid Credentials")
        
        login(request=self.request, user=user)

        return super().clean()
