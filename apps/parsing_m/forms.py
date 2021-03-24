from django import forms

from django.forms import ModelForm, HiddenInput, Textarea
from domain.models import ActivityCode, ActivitySubcode, ActorCode, ActorRole, DateCode, StatusCode, FinancialCode
from .models import Activity, Actor

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

    def init_actor_formset(self, data=None):
        # gets nested actor formset
        if not hasattr(self, 'actor_formset'):
            # caches the formset to avoid multiple lookups and store validation and errors
            actorform_prefix = self.prefix + '-actorform' # the default 'form-x' prefix would collide with the main form prefix
            if self.instance.pk:
                # editing existing activity, get formset for related actors
                related_actors = self.instance.actors.all()
                actor_formset = ActivityActorFormSet(data,
                                                     queryset=related_actors,
                                                     prefix=actorform_prefix)
            else:
                # new activity, get empty actor formset
                actor_formset = ActivityActorFormSet(data,
                                                     queryset=Actor.objects.none(),
                                                     prefix=actorform_prefix)
                
            self.actor_formset = actor_formset

        return self.actor_formset

class ActorForm(ModelForm):
    class Meta:
        model = Actor
        exclude = ['pk', 'id', 'activity']

ActivityFormSet = forms.modelformset_factory(Activity,
                                          form=ActivityForm,
                                          can_delete=True,
                                          extra=1,)

ActivityActorFormSet = forms.modelformset_factory(Actor,
                                                  form=ActorForm,
                                                  can_delete=True,
                                                  extra=3,)



