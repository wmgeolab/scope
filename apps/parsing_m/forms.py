from django import forms

from django.forms import ModelForm

from .models import Activity

class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        exclude = ['fuzzy_date','current_status']
        widgets = {'pk':forms.HiddenInput(), 'extract':forms.HiddenInput()}