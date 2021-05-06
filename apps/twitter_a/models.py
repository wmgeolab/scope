from django.db import models

class TwitterSource(models.Model):
    source_id = models.CharField(max_length=100)
    source_url = models.CharField(max_length=100)
    source_text = models.CharField(max_length=100)
    source_date = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'twitter_a_twittersource'
