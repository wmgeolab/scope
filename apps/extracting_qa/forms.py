from django import forms

from django.forms import ModelForm

from extracting_m.models import Extract

class ExtractQAForm(ModelForm):
    class Meta:
        model = Extract
        exclude = ['source','text']
        widgets = {'pk':forms.HiddenInput(), 'extract':forms.HiddenInput()}