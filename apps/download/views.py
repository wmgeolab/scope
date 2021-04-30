from django.shortcuts import render, redirect
from django.apps import apps

from django.http import HttpResponse

import csv

from domain.models import SourceCode
from sourcing_m.models import Source
from extracting_m.models import Extract

# Create your views here.

def home(request):
    return redirect('overview')

# download
def overview(request):
    return render(request, 'templates/download/home.html')

#function to download sources
def download_sources(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="sources.csv"'
	writer = csv.writer(response)
	writer.writerow(['id','source_code','source_url', 'source_text', 'source_date','date_added', 'current_status'])
	data = Source.objects.filter()
	for row in data:
		rowobj = [row.id, row.source_code, row.source_url, row.source_text, row.source_date, row.date_added, row.current_status]
		writer.writerow(rowobj)
	return response

#function to download extracts
def download_extracts(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="extracts.csv"'
	writer = csv.writer(response)
	writer.writerow(['id','source','text','current_status'])
	data = Extract.objects.filter()
	for row in data:
		rowobj = [row.id, row.source.id, row.text, row.current_status]
		writer.writerow(rowobj)
	return response