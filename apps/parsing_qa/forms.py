from django import forms

from django.forms import ModelForm

from parsing_m.models import Activity, Actor

class ActivityQAForm(ModelForm):
    class Meta:
        model = Activity
        exclude = ['fuzzy_date','current_status']
        widgets = {'pk':forms.HiddenInput(), 'activity':forms.HiddenInput()}

class ActorQAForm(ModelForm):
    class Meta:
        model = Actor
        exclude = []
        widgets = {'pk':forms.HiddenInput(), 'activity':forms.HiddenInput()}