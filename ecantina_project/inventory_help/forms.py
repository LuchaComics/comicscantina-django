from datetime import date
from django.db import models
from django import forms
from django.forms import ModelForm, Textarea, TextInput, NumberInput
from django.forms.extras.widgets import Select, SelectDateWidget
from django.forms.widgets import EmailInput
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from api.models.ec.helprequest import HelpRequest


class HelpRequestForm(forms.ModelForm):
    class Meta:
        model = HelpRequest
        fields = ['subject', 'subject_url', 'message']
        labels = {
        
        }
        widgets = {
            'subject': Select(attrs={'class': u'form-control'}),
            'subject_url': TextInput(attrs={
                'class': u'form-control',
                'placeholder': u'Enter URL of Issue'
            }),
            'message': Textarea(attrs={
                'class': u'form-control',
                'placeholder': u'Enter Message',
                'style':'height:200px;',
            }),
        }