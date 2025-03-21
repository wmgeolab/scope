# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.conf import settings

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=120)
    first = models.CharField(max_length=120)
    last = models.CharField(max_length=120)
    def __str__(self):
        return self.username

class Query(models.Model):
    id = models.AutoField(primary_key=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=120)
    description = models.TextField()

    def __str__(self):
        return self.name

class KeyWord(models.Model):
   query = models.ForeignKey(Query, related_name='keywords', on_delete=models.CASCADE)
   word = models.CharField(max_length=120)

   def __str__(self):
       return self.word

class SourceType(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

class Source(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    url = models.URLField()
    sourceType = models.ForeignKey(SourceType, on_delete=models.CASCADE)

    def __str__(self):
        return self.url


class Run(models.Model):
    id = models.AutoField(primary_key=True)
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    time = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title

class Result(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

    def __str__(self):
        return self.id

class Workspace(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120, unique=True)
    password = models.CharField(max_length=120)
    hidden = models.BooleanField(default=False)
    
    creatorId = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id

class WorkspaceMembers(models.Model):
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)

    def __str__(self):
        return self.id

class WorkspaceEntries(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

    def __str__(self):
        return self.id

class Tag(models.Model):
    workspace = models.ForeignKey(Workspace, related_name='tags', on_delete=models.CASCADE)
    tag = models.CharField(max_length=120)
    
    def __str__(self):
        return self.tag

class AiResponse(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, unique=True)
    summary = models.TextField()
    entities = models.TextField()
    locations = models.TextField()
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.id

class Revision(models.Model):
    id = models.AutoField(primary_key=True)
    summary = models.TextField()
    entities = models.TextField()
    locations = models.TextField()

    original_response = models.ForeignKey(AiResponse, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.id

class WorkspaceQuestions(models.Model):
    workspace = models.ForeignKey("Workspace", on_delete=models.CASCADE)  # Link to a workspace
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who asked the question
    text = models.TextField()  # The question text
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of creation

    def __str__(self):
        return f"Question by {self.user.username} in {self.workspace.id}: {self.text}"
