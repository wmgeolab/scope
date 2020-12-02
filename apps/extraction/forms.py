
from django.forms import ModelForm, modelformset_factory, HiddenInput

from .models import Extract

ExtractFormSet = modelformset_factory(Extract,
                                      exclude=[], #fields=('text',),
                                      widgets={'source':HiddenInput()},
                                      can_delete=True,
                                      extra=1,)



