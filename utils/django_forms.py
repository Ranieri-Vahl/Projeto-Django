import re

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


msgrequired = {'required': 'This field is required'}