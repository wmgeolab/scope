
from django.forms import ModelForm

from .models import Source, SourceCode

class SourceCodeForm(ModelForm):
    class Meta:
        model = SourceCode
        exclude = []

class SourceForm(ModelForm):
    class Meta:
        model = Source
        exclude = []
        
