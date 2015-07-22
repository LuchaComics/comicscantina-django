from datetime import date
from django.db import models
from django import forms
from django.forms import ModelForm, Textarea, TextInput, NumberInput
from django.forms.extras.widgets import Select, SelectDateWidget
from django.forms.widgets import EmailInput
from django.conf import settings
from django.core.exceptions import ValidationError
from api.models.gcd.issue import Issue
from api.models.ec.comic import Comic


class ComicForm(forms.ModelForm):
    class Meta:
        model = Comic
        fields = ['cover','age','is_cgc_rated', 'cgc_rating', 'label_colour', 'condition_rating', 'is_canadian_priced_variant', 'is_variant_cover', 'is_retail_incentive_variant', 'is_newsstand_edition', 'price', 'section','price','cost', 'store',]
        labels = {
            'cover': 'Image',
            'is_cgc_rated': 'CGC Rated',
            'cgc_rating': 'CGC Rating',
            'label_colour': 'Label Colour',
            'condition_rating': 'Condition Rating',
            'is_canadian_priced_variant': 'Is Canadian Priced Variant',
            'is_variant_cover': 'Is Variant Cover',
            'is_retail_incentive_variant': 'Is Retail Incentive Variant',
        }
        widgets = {
            'age': Select(attrs={'class': u'form-control mb10 mt-lg'}),
            'cgc_rating': Select(attrs={'class': u'form-control'}),
            'label_colour': Select(attrs={'class': u'form-control m0 mb10'}),
            'condition_rating': Select(attrs={'class': u'form-control m0 mb10'}),
            'price': NumberInput(attrs={'class': u'form-control mb10','placeholder': u'Price Amount'}),
            'cost': NumberInput(attrs={'class': u'form-control mb10','placeholder': u'Cost Amount'}),
            'location': Select(attrs={'class': u'form-control m0 mb10'}),
            'section': Select(attrs={'class': u'form-control m0 mb10'}),
            'store': Select(attrs={'class': u'form-control m0 mb10'}),
        }
