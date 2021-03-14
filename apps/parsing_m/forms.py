from django import forms

from django.forms import ModelForm
from domain.models import ActivityCode, ActorCode, StatusCode
from .models import Activity

class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        exclude = ['fuzzy_date']
        widgets = {'pk':forms.HiddenInput(), 'extract':forms.HiddenInput()}