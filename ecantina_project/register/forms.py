from datetime import date
from django.db import models
from django import forms
from django.forms import ModelForm, Textarea, TextInput, NumberInput
from django.forms.extras.widgets import Select, SelectDateWidget
from django.forms.widgets import EmailInput
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from api.models.ec.imageupload import ImageUpload
from api.models.ec.organization import Organization


class StoreRegistrationForm (forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Enter Email',
            'autocomplete':'on',
            'data-parsley-id':'7556',
            'required':'',
        }),
        required=True,
    )
    
    org_name = forms.CharField(
        label='Series',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Enter Organizations Name',
            'autocomplete':'on',
            'required':'',
        }),
        required=True,
    )
    
    first_name = forms.CharField(
        label='First Name',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Enter First Name',
            'autocomplete':'on',
            'required':'',
        }),
        required=True,
    )
                                 
    last_name = forms.CharField(
        label='Last Name',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Enter Last Name',
            'autocomplete':'on',
            'required':'',
        }),
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
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Enter Phone Number',
            'autocomplete':'on'
        }),
        required=False,
    )
    fax = forms.CharField(
        label='Fax',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control','placeholder':'Enter Fax Number', 'autocomplete':'on'
        }),
        required=False,
    )

    website = forms.CharField(
        label='Website',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control','placeholder':'Enter Website URL', 'autocomplete':'on',
        }),
        required=False,
    )

    twitter = forms.CharField(
        label='Website',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control','placeholder':'@twitter', 'autocomplete':'on',
        }),
        required=False,
    )

    facebook = forms.CharField(
        label='Website',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class':'form-control','placeholder':'Enter Facebook URL', 'autocomplete':'on',
        }),
        required=False,
    )

    # Location
    #----------
    street_number = forms.CharField(
        label='Street Address',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control','placeholder':'Enter Street Number', 'autocomplete':'on'
        }),
        required=True,
    )
    
    street_name = forms.CharField(
        label='Street Address',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control','placeholder':'Enter Street Name', 'autocomplete':'on'
        }),
        required=True,
    )

    unit_number = forms.CharField(
        label='Street Address',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control','placeholder':'Enter Unit Number', 'autocomplete':'on'
        }),
        required=False,
    )

    city = forms.CharField(
        label='City',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control','placeholder':'Enter City', 'autocomplete':'on'
        }),
        required=True,
    )

    province = forms.CharField(
        label='Province',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control','placeholder':'Enter Province', 'autocomplete':'on'
        }),
        required=True,
    )

    country = forms.CharField(
        label='Country',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control','placeholder':'Enter Country', 'autocomplete':'on'
        }),
        required=True,
    )
    
    postal = forms.CharField(
        label='Zip/Postal',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'form-control','placeholder':'Enter ZIP/Postal', 'autocomplete':'on'
        }),
        required=True,
    )

    # Terms
    is_terms_acceptable = forms.BooleanField(
        required=False
    )

    # Hidden
    hidden_upload_id = forms.CharField(
        widget=forms.HiddenInput(),
        required=True,
    )

    # Functions
    def clean_email(self):
        email = self.cleaned_data['email']
        if email is not None and email is not '':
            try:
                User.objects.get(email=email)
                raise forms.ValidationError("Email already exists.")
            except User.DoesNotExist:
                return email
        else:
            raise forms.ValidationError("Cannot be blank")

    def clean_org_name(self):
        org_name = self.cleaned_data['org_name']
        if org_name is not None and org_name is not '':
            try:
                Organization.objects.get(name=org_name)
                raise forms.ValidationError("Organization name already exists.")
            except Organization.DoesNotExist:
                return org_name
        else:
            raise forms.ValidationError("Cannot be blank")