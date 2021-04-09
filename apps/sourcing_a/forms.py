
from django import forms

from domain.models import SourceCode
from .models import Source


class AutoImportForm(forms.Form):

    primary_keywords = forms.CharField()

    secondary_keywords = forms.CharField()

    tertiary_keywords = forms.CharField()

    start_date = forms.DateField()

    end_date = forms.DateField()
