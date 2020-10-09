from django.db import models

from sourcing.models import Source

from users.models import User

# Create your models here.

class ActivityCode(models.Model):
    activity_code = models.CharField(max_length=30, primary_key=True)
    activity_desc = models.CharField(max_length=255)

    def __str__(self):
        return '{} - {}'.format(self.activity_code, self.activity_desc)

class ActorCode(models.Model):
    actor_code = models.CharField(max_length=10, primary_key=True)
    actor_desc = models.CharField(max_length=255)

    def __str__(self):
        return '{} - {}'.format(self.actor_code, self.actor_desc)

class StatusCode(models.Model):
    status_code = models.CharField(max_length=10, primary_key=True)
    status_desc = models.CharField(max_length=255)

    def __str__(self):
        return '{} - {}'.format(self.status_code, self.status_desc)

##from . import IATI
##loctypes = IATI.LocationTypes['LocationType']
##loctypes = sorted(loctypes, key=lambda l: l['code'])
##
##class Location(models.Model):
##    name = models.CharField(max_length=400)
##    type = models.CharField(max_length=50,
##                          choices=[(l['code'],l['name'])
##                                   for l in loctypes]
##                            )
##    note = models.TextField(blank=True, null=True)
##    geom = models.TextField(blank=True, null=True)

class Activity(models.Model):
    activity_id = models.AutoField(primary_key=True)
    actor_code = models.ForeignKey(ActorCode, related_name='activities', on_delete=models.PROTECT)
    activity_code = models.ForeignKey(ActivityCode, related_name='activities', on_delete=models.PROTECT)
    activity_date = models.DateField()
    fuzzy_date = models.CharField(max_length=30, blank=True, null=True)
    status_code = models.ForeignKey(StatusCode, related_name='+', on_delete=models.PROTECT, null=True)
    notes = models.TextField(blank=True, null=True)
    #locations = ...
    source_id = models.ForeignKey(Source, related_name='+', on_delete=models.PROTECT)
    current_user = models.OneToOneField(User, on_delete=models.PROTECT, null=True)
