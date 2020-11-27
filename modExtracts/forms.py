
from django.forms import ModelForm, modelformset_factory

from .models import Extract

ExtractFormSet = modelformset_factory(Extract,
                                      fields=('text'),
                                      extra=1)



