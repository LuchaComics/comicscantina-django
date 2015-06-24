from datetime import date
from django.db import models
from django import forms
from django.forms import ModelForm, Textarea, TextInput, NumberInput
from django.forms.extras.widgets import Select, SelectDateWidget
from django.forms.widgets import EmailInput
from django.conf import settings
from django.core.exceptions import ValidationError
from inventory.models.gcd.issue import Issue
from inventory.models.ec.comic import Comic


class StoreRegistrationForm (forms.Form):
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
    
    store_name = forms.CharField(
        label='Series',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Enter Store Name',
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
                             
    repeat_password = forms.CharField(
        label='Repeat Password',
            max_length=100,
            widget=forms.TextInput(attrs={
                'type':'password',
                'class':'form-control',
                'placeholder':'Enter Password Again',
                'autocomplete':'off',
                'data-parsley-equalto':'#id_password',
                'required':'',
            }),
    )