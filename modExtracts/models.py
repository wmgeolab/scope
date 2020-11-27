from django.db import models

from modSourcing.models import Source

# Create your models here.
class Extract(models.Model):
    source = models.ForeignKey(Source, related_name='extracts', on_delete=models.PROTECT)
    text = models.TextField(blank=True, null=True)
