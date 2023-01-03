import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')   
    if not regex.match(password):
        raise ValidationError('Must have 1 upper case letter, 1 lower case letter, 1 number and min 8 characters', code='invalid') # noqa E501


def username_validation(username):
    regex = re.compile(r'^(?=.{5,20}$)(.*[a-z0-9@.+-_])$')

    if not regex.match(username):
        raise ValidationError(
            'Min 5 and max 20 characters. Letters, numbers and @/./+/-/_ only', 
            code='invalid'
            ) 


def email_validation(email):
    regex = re.compile(r'^[^\s@<>\(\)[\]\.]+(?:\.[^\s@<>\(\)\[\]\.]+)*@\w+(?:[\.\-_]\w+)*$') # noqa E501

    if not regex.match(email):
        raise ValidationError(
            'Invalid E-mail!, type again', code='invalid'
            ) 


class RegisterForm(forms.ModelForm):
    msgrequired = {'required': 'This field is required'}

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