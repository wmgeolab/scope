# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models

# Create your models here.
class User(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    username = models.CharField(max_length=120)
    first = models.CharField(max_length=120)
    last = models.CharField(max_length=120)

    def _str_(self):
        return username

class Query(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    description = models.TextField()

    def _str_(self):
        return self.title

"""
class ScopeBackend(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    def _str_(self):
        return self.title
"""

"""
class KeyWord(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    user_id = models.PositiveIntegerField(null=True, blank=True)
    name = models.CharField(max_length=120)
    #start_datetime = models.DateTimeField(default=datetime.now, blank=True)

    def _str_(self):
        return self.title


class Query(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    keyWords = models.CharField(max_length=120)
    start_datetime = models.DateTimeField()
    start_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    def _str_(self):
        return self.title
"""