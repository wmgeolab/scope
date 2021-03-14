
from django.forms import ModelForm

from .models import Domain, ActivityCode, ActorCode, StatusCode, SourceCode, TriggerWord


class DomainForm(ModelForm):
    class Meta:
        model = Domain
        exclude = []

class ActivityCodeForm(ModelForm):
    class Meta:
        model = ActivityCode
        exclude = []

class ActorCodeForm(ModelForm):
    class Meta:
        model = ActorCode
        exclude = []

class StatusCodeForm(ModelForm):
    class Meta:
        model = StatusCode
        exclude = []

class SourceCodeForm(ModelForm):
    class Meta:
        model = SourceCode
        exclude = []

class TriggerWordForm(ModelForm):
    class Meta:
        model = TriggerWord
        exclude = []

