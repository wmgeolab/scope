from django.shortcuts import render, redirect
from django.apps import apps

from django.http import HttpResponse

import csv

from domain.models import SourceCode
from sourcing_m.models import Source
from extracting_m.models import Extract
from parsing_m.models import Activity
from parsing_m.models import Actor

# Create your views here.

def home(request):
    return redirect('select')

# download
def select(request):
    return render(request, 'templates/download/home.html')

#function to download sources
def download_sources(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="sources.csv"'
	writer = csv.writer(response)
	writer.writerow(['id', 'source_code', 'source_url', 'source_text', 'source_date', 'date_added', 'current_status'])
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
	writer.writerow(['id', 'source', 'text', 'current_status'])
	data = Extract.objects.filter()
	for row in data:
		rowobj = [row.id, row.source.id, row.text, row.current_status]
		writer.writerow(rowobj)
	return response

#function to download activities
def download_activities(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="activities.csv"'
	writer = csv.writer(response)
	writer.writerow(['id', 'extract', 'activity_subcodes', 'actor_codes', 'actor_names', 'actor_rolecodes', 'activity_date', 'date_code', 'status_code', 'financial_code', 'dollar_amount', 'locations', 'parser_notes', 'current_status'])
	data = Activity.objects.all()
	for row in data:
		rowobj = [row.id, row.extract.id, ' | '.join([row.activity_subcode for row in row.activity_subcodes.all()]), ' | '.join([row.actor_code.actor_code for row in row.actors.all()]), ' | '.join([row.actor_name for row in row.actors.all()]), ' | '.join([row.actor_rolecode.actor_rolecode for row in row.actors.all()]), row.activity_date, row.date_code, row.status_code, row.financial_code, row.dollar_amount, row.locations, row.parser_notes, row.current_status]
		writer.writerow(rowobj)

	return response