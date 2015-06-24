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
        required=True,
    )
    
    store_name = forms.CharField(
        label='Series',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Enter Store Name',
        }),
        required=True,
    )
    
    first_name = forms.CharField(
        label='First Name',
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter First Name'}),
        required=True,
    )
                                 
    last_name = forms.CharField(
        label='Last Name',
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Last Name'}),
        required=True,
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
        required=True,
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
        required=True,
    )
    is_digital_store_only = forms.BooleanField(
        required=False
    )

    # Contact
    #---------
    phone = forms.CharField(
        label='Phone',
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Phone Number', 'autocomplete':'off'}),
        required=True,
    )

    website = forms.CharField(
        label='Website',
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Website URL', 'autocomplete':'off',}),
        required=False,
    )

    twitter = forms.CharField(
        label='Website',
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'@twitter', 'autocomplete':'off',}),
        required=False,
    )

    facebook = forms.CharField(
        label='Website',
        max_length=255,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Facebook URL', 'autocomplete':'off',}),
        required=False,
    )

    # Location
    #----------
    street = forms.CharField(
        label='Street Address',
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Street Address', 'autocomplete':'off'}),
        required=True,
    )

    city = forms.CharField(
        label='City',
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter City', 'autocomplete':'off'}),
        required=True,
    )

    province = forms.CharField(
        label='Province',
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Province', 'autocomplete':'off'}),
        required=True,
    )

    country = forms.CharField(
        label='Country',
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Country', 'autocomplete':'off'}),
        required=True,
    )

    # Terms
    is_terms_acceptable = forms.BooleanField(
        required=False
    )