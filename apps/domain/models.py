from django.db import models

# Create your models here.

class Domain(models.Model):
	domain = models.TextField()
	#this needs to always only be at most 1 row (or 0 if it hasn't been set yet)

class TriggerWord(models.Model):
    triggerword = models.TextField() #should probably make this a primary_key so we don't get duplicates; needs to be a charfield not a textfield
    #in the future should also add a Domain module which will determine which activity_codes and trigger words to preload in
    	#this is where the PM can design the fields to include, etc.
    #may add a field later which counts the number of relevant detections for each triggerword

class ActivityCode(models.Model):
    activity_code = models.CharField(max_length=30, primary_key=True)
    activity_desc = models.CharField(max_length=255)

    def __str__(self):
        return '{} - {}'.format(self.activity_code, self.activity_desc)

class ActivitySubcode(models.Model):
    activity_subcode = models.CharField(max_length=30, primary_key=True)
    activity_subdesc = models.CharField(max_length=255)
    activity_code = models.ForeignKey('ActivityCode', related_name='activity_subcodes', on_delete=models.PROTECT)

    def __str__(self):
        return '{} - {} - {}'.format(self.activity_subcode, self.activity_code.activity_desc[:30]+'...', self.activity_subdesc)

class ActorCode(models.Model):
    actor_code = models.CharField(max_length=10, primary_key=True)
    actor_desc = models.CharField(max_length=255)

    def __str__(self):
        return '{} - {}'.format(self.actor_code, self.actor_desc)

class ActorRole(models.Model):
    actor_rolecode = models.CharField(max_length=10, primary_key=True)
    actor_roledesc = models.CharField(max_length=255)

    def __str__(self):
        return '{} - {}'.format(self.actor_rolecode, self.actor_roledesc)

class DateCode(models.Model):
    date_code = models.CharField(max_length=10, primary_key=True)
    date_desc = models.CharField(max_length=255)

    def __str__(self):
        return '{} - {}'.format(self.date_code, self.date_desc)

class StatusCode(models.Model):
    status_code = models.CharField(max_length=10, primary_key=True)
    status_desc = models.CharField(max_length=255)

    def __str__(self):
        return '{} - {}'.format(self.status_code, self.status_desc)

class FinancialCode(models.Model):
    financial_code = models.CharField(max_length=10, primary_key=True)
    financial_desc = models.CharField(max_length=255)

    def __str__(self):
        return '{} - {}'.format(self.financial_code, self.financial_desc)

class SourceCode(models.Model):
    source_code = models.CharField(max_length=15, primary_key=True)
    source_desc = models.CharField(max_length=255)

    def __str__(self):
        return '{} - {}'.format(self.source_code, self.source_desc)
