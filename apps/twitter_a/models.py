from django.db import models


class TwitterSearch(models.Model):
    primary_keywords = models.CharField(max_length=100)
    secondary_keywords = models.CharField(max_length=100)
    tertiary_keywords = models.CharField(max_length=100)
    start_date = models.DateTimeField(max_length=100)
    end_date = models.DateTimeField(max_length=100)

class TwitterSource(models.Model):
    source_id = models.TextField(primary_key=True, max_length=50, blank=True, unique = True)
    source_url = models.URLField(blank=True, unique = True)
    source_text = models.TextField(blank=True, null=True)
    source_date = models.TextField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'twitter_a_twittersource'
