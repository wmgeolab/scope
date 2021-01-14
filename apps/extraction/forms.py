
from django.forms import ModelForm, modelformset_factory, HiddenInput, Textarea

from .models import Extract

ExtractFormSet = modelformset_factory(Extract,
                                      exclude=[], #fields=('text',),
                                      widgets={'source':HiddenInput(),
                                               'text':Textarea(attrs={'rows':5,
                                                                      'style':'width:100%'})
                                               },
                                      can_delete=True,
                                      extra=1,)



