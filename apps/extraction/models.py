from django.db import models

from sourcing.models import Source

# Create your models here.
class Extract(models.Model):
    source = models.ForeignKey(Source, related_name='extracts', on_delete=models.PROTECT)
    #may add a reference field to source_url
    text = models.TextField(blank=True, null=True)
