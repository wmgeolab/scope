from django.db import models

from extracting_m.models import Extract

from users.models import User
from domain.models import ActivityCode, ActivitySubcode, ActorCode, StatusCode, FinancialCode

# Create your models here.

class Activity(models.Model):
    #activity_id = models.AutoField(primary_key=True)
    #actor_code may need to be reassessed in the future
    actor_code = models.ForeignKey(ActorCode, related_name='activities', on_delete=models.PROTECT)
    actor_desc = models.CharField(max_length=255)
    activity_code = models.ForeignKey(ActivityCode, related_name='activities', on_delete=models.PROTECT)
    activity_subcode = models.ForeignKey(ActivitySubcode, related_name='activities', on_delete=models.PROTECT)
    activity_date = models.DateField()
    fuzzy_date = models.CharField(max_length=30, blank=True, null=True)
    status_code = models.ForeignKey(StatusCode, related_name='activities', on_delete=models.PROTECT)
    financial_code = models.ForeignKey(FinancialCode, related_name='activities', on_delete=models.PROTECT, null=True, blank=True)
    dollar_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    locations = models.CharField(max_length=50, blank=True, null=True)
    #for now, this is extract. in the next version, we'll include modules between extracting and parsing
    extract = models.ForeignKey(Extract, related_name='activities', on_delete=models.PROTECT)
    current_user = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True)
    current_status = models.CharField(max_length=10, blank=True, choices=[('PARM','parsed_m'),('PARQ','parsed_q')])
