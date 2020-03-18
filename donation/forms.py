from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Email', 'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Hasło', 'autocomplete': 'current-password'}))


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Imię', 'autofocus': True}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Nazwisko', 'autofocus': True}))
    username = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Email', 'autofocus': True}))
    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'placeholder': 'Hasło'}),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "password1", "password2")


