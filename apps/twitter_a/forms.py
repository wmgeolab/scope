import datetime

from django import forms
from .models import TwitterSearch
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class TwitterSearchForm(forms.ModelForm):
    primary_keywords = forms.CharField(help_text="\nEnter primary keywords\n\n")
    secondary_keywords = forms.CharField(help_text="\nEnter secondary keywords\n\n")
    tertiary_keywords = forms.CharField(required=False, help_text="\nEnter tertiary keywords\n\n")
    start_date = forms.DateTimeField(help_text="\nPlease enter a date (later than March 2006)\n\n")
    end_date = forms.DateTimeField(help_text="\nPlease enter a date (up to or earlier than the current date)\n\n")
    class Meta:
        model = TwitterSearch
        fields = '__all__'

    def clean_primary_kw(self):
        data = self.cleaned_data['primary_kw']
        return data
    
    def clean_secondary_kw(self):
        data = self.cleaned_data['secondary_kw']
        return data
    
    def clean_tertiary_kw(self):
        data = self.cleaned_data['tertiary_kw']
        if not data:  return ""
        return data
    
    def clean_start_date(self):
        data = self.cleaned_data['start_date']
        return data
    
    def clean_end_date(self):
        data = self.cleaned_data['end_date']
        return data
