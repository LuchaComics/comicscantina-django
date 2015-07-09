from datetime import date
from django.db import models
from django import forms
from django.forms import ModelForm, Textarea, TextInput, NumberInput
from django.forms.extras.widgets import Select, SelectDateWidget
from django.forms.widgets import EmailInput
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from inventory.models.ec.imageupload import ImageUpload
from inventory.models.ec.customer import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'joined', 'street_name', 'street_number', 'unit_number', 'city' , 'province' , 'country' , 'postal' , 'email' , 'phone' ,
        ]
        labels = {
        
        }
        widgets = {
            'first_name': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter First Name'
            }),
            'last_name': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Last Name'
            }),
            'joined': TextInput(attrs={
                'class': u'form-control mb-lg',
                'readonly': u'',
            }),
            'street_number': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Street #'
            }),
            'street_name': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Street Name'
            }),
            'unit_number': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Unit #'
            }),
            'city': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter City'
            }),
            'province': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Province / State'
            }),
            'country': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Country'
            }),
            'postal': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Postal Code / Zip'
            }),
            'website': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Website URL'
            }),
            'email': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Email Address'
            }),
            'phone': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Phone Number'
            }),
        }