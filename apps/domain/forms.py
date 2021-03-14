
from django.forms import ModelForm

from .models import Domain, ActivityCode, ActivitySubcode, ActorCode, StatusCode, FinancialCode, SourceCode, TriggerWord


class DomainForm(ModelForm):
    class Meta:
        model = Domain
        exclude = []

class ActivityCodeForm(ModelForm):
    class Meta:
        model = ActivityCode
        exclude = []

class ActivitySubcodeForm(ModelForm):
    class Meta:
        model = ActivitySubcode
        exclude = []

class ActorCodeForm(ModelForm):
    class Meta:
        model = ActorCode
        exclude = []

class StatusCodeForm(ModelForm):
    class Meta:
        model = StatusCode
        exclude = []

class FinancialCodeForm(ModelForm):
    class Meta:
        model = FinancialCode
        exclude = []

class SourceCodeForm(ModelForm):
    class Meta:
        model = SourceCode
        exclude = []

class TriggerWordForm(ModelForm):
    class Meta:
        model = TriggerWord
        exclude = []

