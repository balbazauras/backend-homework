from django.forms import ModelForm
from .models import *
from django import forms


class CreateUrlForm(ModelForm):
    expiration_time = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = Url
        fields = ['long', 'expiration_time']
