from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={"class": "form-control my-3", "placeholder": "Enter email"}))
    # country = forms.ChoiceField(required=True)
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={"class": "form-control my-3", "placeholder": "Enter password"}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={"class": "form-control my-3", "placeholder": "Repeat password"}))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter username"}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Enter username"}))
    password = forms.CharField(required=True,
                               widget=forms.PasswordInput(
                                   attrs={"class": "form-control my-3", "placeholder": "Enter password"}))

    class Meta:
        model = User
        fields = ["username", "password"]

    def get_user(self):
        return self.user_cache
