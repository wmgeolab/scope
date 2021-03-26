from django import forms

from django.forms import ModelForm

from parsing_m.models import Activity

class ActivityQAForm(ModelForm):
    class Meta:
        model = Activity
        exclude = ['fuzzy_date','current_status']
        widgets = {'pk':forms.HiddenInput(), 'activity':forms.HiddenInput()}