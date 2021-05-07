from django.db import models

class TwitterSource(models.Model):
    source_search_id = models.CharField(primary_key=True, max_length=100, default='.')
    source_id = models.CharField(max_length=100)
    source_url = models.CharField(max_length=100)
    source_text = models.CharField(max_length=100)
    source_date = models.CharField(max_length=100)
