from django import forms

from django.forms import ModelForm

from extraction.models import Extract

class ExtractQAForm(ModelForm):
    class Meta:
        model = Extract
        exclude = ['source','text']
        widgets = {'pk':forms.HiddenInput(), 'extract':forms.HiddenInput()}