from django import forms
from utils.django_forms import msgrequired


class LoginForm(forms.Form):
    username = forms.CharField(
        error_messages=msgrequired,
        label='Username',
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your username'
        }),
    )

    password = forms.CharField(
        error_messages=msgrequired,
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Type your password'
        }),
    )
