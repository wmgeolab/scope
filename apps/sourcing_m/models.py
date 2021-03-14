from django.db import models
from django.utils import timezone

from users.models import User
from domain.models import SourceCode

# Create your models here.

class Source(models.Model):
    source_code = models.ForeignKey(SourceCode, related_name='sources', on_delete=models.PROTECT)
    source_url = models.URLField(blank=True, unique = True)
    source_html = models.TextField(blank=True, null=True)
    source_text = models.TextField(blank=True, null=True)
    source_date = models.DateTimeField(blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now, blank=True)
    current_user = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True)
    current_status = models.CharField(max_length=10, blank=True, default='SRCM', choices=[('SRCM','sourced_m'),('EXTM','extracted_m')])
