from django.db import models

from extracting_m.models import Extract

from users.models import User
from domain.models import ActivityCode, ActivitySubcode, ActorCode, ActorRole, DateCode, StatusCode, FinancialCode

# Create your models here.

class Activity(models.Model):
    # these will be deleted later on
    actor_code = models.ForeignKey(ActorCode, related_name='activities', on_delete=models.PROTECT, blank=True, null=True)
    actor_name = models.CharField(max_length=255, blank=True, null=True)
    actor_rolecode = models.ForeignKey(ActorRole, related_name='activities', on_delete=models.PROTECT, blank=True, null=True)
    ###
    activity_code = models.ForeignKey(ActivityCode, related_name='activities', on_delete=models.PROTECT)
    activity_subcode = models.ForeignKey(ActivitySubcode, related_name='activities', on_delete=models.PROTECT)
    activity_date = models.DateField()
    fuzzy_date = models.CharField(max_length=30, blank=True, null=True)
    date_code = models.ForeignKey(DateCode, related_name='activities', on_delete=models.PROTECT)
    status_code = models.ForeignKey(StatusCode, related_name='activities', on_delete=models.PROTECT)
    financial_code = models.ForeignKey(FinancialCode, related_name='activities', on_delete=models.PROTECT, null=True, blank=True)
    dollar_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    locations = models.CharField(max_length=50, blank=True, null=True)
    parser_notes = models.CharField(max_length=500, blank=True, null=True)
    #for now, this is extract. in the next version, we'll include modules between extracting and parsing
    extract = models.ForeignKey(Extract, related_name='activities', on_delete=models.PROTECT)
    current_user = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True)
    current_status = models.CharField(max_length=10, blank=True, choices=[('PARM','parsed_m'),('PARQ','parsed_q')])

class Actor(models.Model):
    # each Actor is just a specific mention of an actor and is only unique to each Activity
    # so there may be several Actors with the same values spread across multiple activities
    activity = models.ForeignKey(Activity, related_name='actors', on_delete=models.CASCADE) # deleting an activity should delete all its actor instances
    actor_code = models.ForeignKey(ActorCode, related_name='actors', on_delete=models.PROTECT)
    actor_name = models.CharField(max_length=255)
    actor_rolecode = models.ForeignKey(ActorRole, related_name='actors', on_delete=models.PROTECT)


    
