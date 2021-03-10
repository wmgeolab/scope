from django.db import models

from sourcing.models import Source

from users.models import User

# Create your models here.
class Extract(models.Model):
    source = models.ForeignKey(Source, related_name='extracts', on_delete=models.PROTECT)
    #may add a reference field to source_url
    text = models.TextField(blank=True, null=True)
    current_user = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True)
    current_status = models.CharField(max_length=10, blank=True, choices=[('EXTM','extracted_m'),('EXTQ','extracted_q'),('PARM','parsed_m')])

