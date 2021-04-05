from django.db import models
from django.utils import timezone

from users.models import User
from domain.models import SourceCode

from sourcing_m.models import Source

# Create your models here.

class Source(models.Model):
    source = models.ForeignKey(Source, related_name='sources', on_delete=models.PROTECT)
    source_relevance = models.IntegerField(blank=True, null=True)
    current_status = models.CharField(max_length=9, blank=True, default = 'SRCA', choices=[('SRCA','sourced_a')])
