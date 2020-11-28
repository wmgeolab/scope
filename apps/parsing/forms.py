
from django.forms import ModelForm

from .models import Activity, ActivityCode, ActorCode, StatusCode

class ActivityForm(ModelForm):
    class Meta:
        model = Activity
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





