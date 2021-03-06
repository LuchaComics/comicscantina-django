from datetime import date
from django.db import models
from django import forms
from django.forms.widgets import EmailInput
from django.conf import settings
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Enter Email',
            'autocomplete':'off',
            'data-parsley-id':'7556',
            'required':'',
        }),
    )
    password = forms.CharField(
        label='Password',
        max_length=100,
        widget=forms.TextInput(attrs={
            'type':'password',
            'class':'form-control',
            'placeholder':'Enter Password',
            'autocomplete':'off',
            'data-parsley-id':'0276',
            'required':'',
        }),
    )
