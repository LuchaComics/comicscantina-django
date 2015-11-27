import datetime
from django.db import models
from django import forms
from django.forms import ModelForm, Textarea, TextInput, NumberInput
from django.forms.extras.widgets import Select, SelectDateWidget
from django.forms.widgets import EmailInput
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.subdomain import SubDomain

class SubDomainForm(forms.ModelForm):
    class Meta:
        model = SubDomain
        fields = ['name', 'organization','store',]
        labels = {
        }
        widgets = {
            'name': TextInput(attrs={
                'class': u'form-control mb-lg',
                'placeholder': u'Enter Sub-Domain Name'
            }),
        }