from django.db import models


class TwitterSearch(models.Model):
    primary_keywords = models.CharField(max_length=100)
    secondary_keywords = models.CharField(max_length=100)
    tertiary_keywords = models.CharField(max_length=100)
    start_date = models.DateTimeField(max_length=100)
    end_date = models.DateTimeField(max_length=100)

class TwitterSource(models.Model):
    source_url = models.URLField(blank=True, unique = True)
    source_text = models.TextField(blank=True, null=True)
    source_date = models.DateTimeField(blank=True, null=True)
