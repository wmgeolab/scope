from django import forms

from django.forms import ModelForm, HiddenInput, Textarea
from domain.models import ActivityCode, ActivitySubcode, ActorCode, ActorRole, DateCode, StatusCode, FinancialCode
from .models import Activity, Actor

from .widgets import SelectMultipleDropdowns

class NativeDateInput(forms.DateInput):
    input_type = 'date'


class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        exclude = ['extract', 'current_user', 'current_status']
        widgets = {#'pk':forms.HiddenInput(),
                   #'extract':forms.HiddenInput(),
                   #'current_user':HiddenInput(),
                   #'activity_subcodes':forms.CheckboxSelectMultiple(),
                   'activity_subcodes':SelectMultipleDropdowns(extraselects=3),
                   'activity_date':NativeDateInput(format='%Y-%m-%d'),
                   }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # set empty label for all choice fields to blank '' instead of default '--------'
        for fl in self.fields.values():
            if hasattr(fl, 'empty_label'):
                fl.empty_label = ''

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

    def is_empty(self):
        data = self.clean()
        if not data:
            return True

    def is_valid(self):
        # the usual form validation
        valid = super().is_valid()

        # additional cached checks
        if not hasattr(self, '_is_valid'):
            
            if self.is_empty():
                # empty form, no additional checks needed
                self._is_valid = valid
                
            else:
                # check that at least one actor in actorformset
                def is_empty(form):
                    data = form.clean()
                    if not data or data['DELETE']:
                        return True
                nonempty_actor_forms = [actorform for actorform in self.actor_formset
                                        if not is_empty(actorform)]

                # add error if not
                if not nonempty_actor_forms:
                    msg = 'At least one actor required.'
                    self.add_error(None, msg)

                # check that at least one activity subcode
                data = self.clean()
                related_subcodes = data.get('activity_subcodes') 
                
                # cache final validation
                self._is_valid = (valid and bool(nonempty_actor_forms) and bool(related_subcodes))

        return self._is_valid
        

class ActorForm(ModelForm):
    class Meta:
        model = Actor
        exclude = ['pk', 'id', 'activity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # set empty label for all choice fields to blank '' instead of default '--------'
        for fl in self.fields.values():
            if hasattr(fl, 'empty_label'):
                fl.empty_label = ''

# formsets

ActivityFormSet = forms.modelformset_factory(Activity,
                                          form=ActivityForm,
                                          can_delete=True,
                                          extra=1,)

ActivityActorFormSet = forms.modelformset_factory(Actor,
                                                  form=ActorForm,
                                                  can_delete=True,
                                                  extra=3,)



