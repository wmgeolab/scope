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

    def __str__(self):
        return self.username

class Query(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    description = models.TextField()

    def __str__(self):
        return self.name

class KeyWord(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    word = models.CharField(max_length=120)

    def __str__(self):
        return self.word

class SourceType(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    description = models.TextField()
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

class Source(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    text = models.TextField()
    url = models.URLField()
    sourceType = models.ForeignKey(SourceType, on_delete=models.CASCADE)

    def __str__(self):
        return self.url

class Result(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    src = models.ForeignKey(Source, on_delete=models.CASCADE)

    def __str__(self):
        return self.id

class Run(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    result = models.ForeignKey(Result, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


"""
class ScopeBackend(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
"""

"""
class KeyWord(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    user_id = models.PositiveIntegerField(null=True, blank=True)
    name = models.CharField(max_length=120)
    #start_datetime = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
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

    def __str__(self):
        return self.title
"""