from django.db import models
from django.utils import timezone

from users.models import User

# Create your models here.

class SourceCode(models.Model):
    source_code = models.CharField(max_length=15, primary_key=True)
    source_desc = models.CharField(max_length=255)

    def __str__(self):
        return '{} - {}'.format(self.source_code, self.source_desc)

class Source(models.Model):
    source_id = models.AutoField(primary_key=True)
    source_code = models.ForeignKey('SourceCode', on_delete=models.PROTECT)
    source_url = models.URLField(blank=True, unique = True)
    source_html = models.TextField(blank=True, null=True)
    source_text = models.TextField(blank=True, null=True)
    source_date = models.DateTimeField(blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now, blank=True)
    current_user = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True)
    current_status = models.CharField(max_length=10, blank=True, default='UN', choices=[('UN','unprocessed'),('EX','extracted'),('PAR','parsed')])
