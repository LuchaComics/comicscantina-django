from datetime import date
from django.db import models
from django import forms
from django.forms import ModelForm, Textarea, TextInput, NumberInput
from django.forms.extras.widgets import Select, SelectDateWidget
from django.forms.widgets import EmailInput
from django.conf import settings
from django.core.exceptions import ValidationError
from api.models.gcd.issue import GCDIssue
from api.models.ec.comic import Comic
from api.models.ec.product import Product
from api.models.ec.category import Category


class ComicForm(forms.ModelForm):
    class Meta:
        model = Comic
        fields = ['age','is_cgc_rated', 'cgc_rating', 'label_colour', 'condition_rating', 'is_canadian_priced_variant', 'is_variant_cover', 'is_retail_incentive_variant', 'is_newsstand_edition', ]
        labels = {
            'is_cgc_rated': 'CGC Rated',
            'cgc_rating': 'CGC Rating',
            'label_colour': 'Label Colour',
            'condition_rating': 'Condition Rating',
            'is_canadian_priced_variant': 'Is Canadian Priced Variant',
            'is_variant_cover': 'Is Variant Cover',
            'is_retail_incentive_variant': 'Is Retail Incentive Variant',
        }
        widgets = {
            'age': Select(attrs={'class': u'form-control'}),
            'cgc_rating': Select(attrs={'class': u'form-control'}),
            'label_colour': Select(attrs={'class': u'form-control m0 mb10'}),
            'condition_rating': Select(attrs={'class': u'form-control m0 mb10'}),
        }


class IssueForm(forms.ModelForm):
    class Meta:
        model = GCDIssue
        fields = ['series','number', 'title', 'publisher_name', 'genre', ]
        labels = {
            'series': 'Series',
            'number': 'Issue #',
            'title': 'Comic Title',
            'publisher_name': 'Publisher',
            'genre': 'Genre',
        }
        widgets = {
            'series': TextInput(attrs={
                'class': u'form-control mb10 input-disabled mt0 p0',
                'style':'position:relative;top:-3px;',
                'placeholder':'Series',
                'readonly': u'true',
            }),
            'number': TextInput(attrs={
                'class':'form-control mb10 input-disabled p0',
                'placeholder':'Issue #','readonly': u'true',
            }),
            'title': TextInput(attrs={
                'class':'form-control mb10 input-disabled p0',
                'placeholder':'Comic Title','readonly': u'true',
            }),
            'publisher_name': TextInput(attrs={
                'class':'form-control mb10 input-disabled p0',
                'placeholder':'Publisher Name','readonly': u'true',
            }),
            'genre': TextInput(attrs={
                'class':'form-control mb10 input-disabled p0',
                'placeholder':'Genre','readonly': u'true',
            }),
        }


from datetime import date
from django.db import models
from django import forms
from django.forms import ModelForm, Textarea, TextInput, NumberInput
from django.forms.extras.widgets import Select, SelectDateWidget
from django.forms.widgets import EmailInput
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from api.models.ec.imageupload import ImageUpload


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']
        labels = {
        
        }
        widgets = {
    
    }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['image_url', 'price', 'section','price','cost', 'store','type','images', 'category',]
        labels = {
            
        }
        widgets = {
            'images': Select(attrs={'class': u'form-control mb10 mt-lg'}),
            'type': Select(attrs={'class': u'form-control'}),
            'price': NumberInput(attrs={'class': u'form-control','placeholder': u'Price Amount'}),
            'cost': NumberInput(attrs={'class': u'form-control','placeholder': u'Cost Amount'}),
            'location': Select(attrs={'class': u'form-control'}),
            'section': Select(attrs={'class': u'form-control'}),
            'store': Select(attrs={'class': u'form-control'}),
            'category': Select(attrs={'class': u'form-control'}),
    }