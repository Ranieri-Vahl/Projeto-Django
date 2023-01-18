from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.django_forms import (email_validation, msgrequired, strong_password,
                                username_validation)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        error_messages=msgrequired,
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Type your password'
        }),
        validators=[strong_password]
        )

    password2 = forms.CharField(
        error_messages=msgrequired,
        label='Confirm password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        })
        )

    username = forms.CharField(
        error_messages=msgrequired,
        label='Username',
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your username'
        }),
        validators={username_validation},
        )

    email = forms.EmailField(
        error_messages=msgrequired,
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Type your E-mail'
        }),
        validators={email_validation},
        )

    first_name = forms.CharField(
        error_messages=msgrequired,
        label='First name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your first name'
        }))

    last_name = forms.CharField(
        error_messages=msgrequired,
        label='Last name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your last name'
        }))

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'This email is already registered', code='invalid'
                ) 

        return email

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get('password')
        password2 = cleaned.get('password2')
        if password != password2:
            raise ValidationError({
                'password': 'The passwords must be equal!',
                'password2': 'The passwords must be equal!'
            })
        return cleaned
