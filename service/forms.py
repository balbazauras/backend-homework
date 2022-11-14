from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import *


class CreateUrlForm(ModelForm):
    expiration_time = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={'type': 'datetime-local'}
        )
    )

    class Meta:
        model = Url
        fields = ['long_url', 'expiration_time', 'click_limit']


class UpdateExpirationUrlForm(ModelForm):
    expiration_time = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={'type': 'datetime-local'}
        )
    )

    class Meta:
        model = Url
        fields = ['expiration_time']


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
