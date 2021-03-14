from django.db import models

# Create your models here.

class Domain(models.Model):
	domain = models.TextField()
	#this needs to always only be at most 1 row (or 0 if it hasn't been set yet)

class TriggerWord(models.Model):
    triggerword = models.TextField()
    #in the future should also add a Domain module which will determine which activity_codes and trigger words to preload in
    	#this is where the PM can design the fields to include, etc.
    #may add a field later which counts the number of relevant detections for each triggerword

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

class SourceCode(models.Model):
    source_code = models.CharField(max_length=15, primary_key=True)
    source_desc = models.CharField(max_length=255)

    def __str__(self):
        return '{} - {}'.format(self.source_code, self.source_desc)