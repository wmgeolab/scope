from django import forms

from django.forms import ModelForm, modelformset_factory, HiddenInput, Textarea
from domain.models import ActivityCode, ActivitySubcode, ActorCode, ActorRole, DateCode, StatusCode, FinancialCode
from .models import Activity

class NativeDateInput(forms.DateInput):
    input_type = 'date'

class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        exclude = ['extract', 'current_user', 'current_status']
        widgets = {#'pk':forms.HiddenInput(),
                   #'extract':forms.HiddenInput(),
                   #'current_user':HiddenInput(),
                   'activity_date':NativeDateInput(format='%Y-%m-%d'),
                   }

##ActivityFormSet = modelformset_factory(Activity,
##                                      exclude=['current_status'], #fields=('text',),
##                                      widgets={'extract':HiddenInput(), 'current_user':HiddenInput(),
##                                               'activity_date':NativeDateInput(format='%Y-%m-%d'),
##                                               },
##                                      can_delete=True,
##                                      extra=1,)

ActivityFormSet = modelformset_factory(Activity,
                                      form=ActivityForm,
                                      can_delete=True,
                                      extra=1,)
