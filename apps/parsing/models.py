from django.db import models

from extraction.models import Extract

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

class Activity(models.Model):
    activity_id = models.AutoField(primary_key=True)
    #actor_code may need to be reassessed in the future
    actor_code = models.ForeignKey(ActorCode, related_name='activities', on_delete=models.PROTECT)
    activity_code = models.ForeignKey(ActivityCode, related_name='activities', on_delete=models.PROTECT)
    activity_date = models.DateField()
    fuzzy_date = models.CharField(max_length=30, blank=True, null=True)
    status_code = models.ForeignKey(StatusCode, related_name='activities', on_delete=models.PROTECT, null=True)
    dollar_amount = models.CharField(max_length=30, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    locations = models.CharField(max_length=50, blank=True, null=True)
    #for now, this is extract. in the next version, we'll include modules between extracting and parsing
    extract = models.ForeignKey(Extract, related_name='activities', on_delete=models.PROTECT)
    current_user = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True)
