from django.shortcuts import render, redirect
from django.apps import apps

from django.core.files.storage import FileSystemStorage

import os

from .models import  Domain, ActivityCode, ActivitySubcode, ActorCode, StatusCode, FinancialCode, SourceCode, TriggerWord

from .forms import DomainForm, ActivityCodeForm, ActivitySubcodeForm, ActorCodeForm, StatusCodeForm, FinancialCodeForm, SourceCodeForm, TriggerWordForm

# Create your views here.

def home(request):
    return redirect('overview')


def overview(request):
    domain = Domain.objects.all()
    activitycodes = ActivityCode.objects.all()
    activitysubcodes = ActivitySubcode.objects.all()
    actorcodes = ActorCode.objects.all()
    statuscodes = StatusCode.objects.all()
    financialcodes = FinancialCode.objects.all()
    sourcecodes = SourceCode.objects.all()
    triggerwords = TriggerWord.objects.all()
    return render(request, 'templates/domain/overview.html',
    	{'domain':domain, 'activitycodes':activitycodes, 'activitysubcodes':activitysubcodes,
    	'actorcodes':actorcodes, 'statuscodes':statuscodes, 'financialcodes':financialcodes,
    	'sourcecodes':sourcecodes, 'triggerwords':triggerwords})

def edit_domain(request):
	if request.method == 'GET':
		return render(request, 'templates/domain/edit_domain.html')
	elif request.method == 'POST':
		logger = [] # each entry will become a new line in a textstring
		uploaded_file = request.FILES['importdocument']
		import csv
		import io
		filewrapper = io.TextIOWrapper(uploaded_file, encoding=request.encoding) # see https://stackoverflow.com/questions/16243023/how-to-resolve-iterator-should-return-strings-not-bytes
		reader = csv.DictReader(filewrapper, delimiter=',') 
		logger.append('file received')
		count = 0
		for data_dict in reader:
			form = DomainForm(data_dict)
			if form.is_valid():
				form.save()
				count += 1
			else:
				logger.append(str(list(data_dict.values())) + ' --> ' + str(form.errors.as_data()))
		# finish up
		logger.append('import finished')
		logger.append('successfully imported {} domain'.format(count))
		importresults = '\n'.join(logger) # make logs into a multiline textstring
		return render(request, 'templates/domain/edit_domain.html', {'importresults':importresults})


def edit_activitycodes(request):
	if request.method == 'GET':
		return render(request, 'templates/domain/edit_activitycodes.html')
	elif request.method == 'POST':
		logger = [] # each entry will become a new line in a textstring
		uploaded_file = request.FILES['importdocument']
		import csv
		import io
		filewrapper = io.TextIOWrapper(uploaded_file, encoding=request.encoding) # see https://stackoverflow.com/questions/16243023/how-to-resolve-iterator-should-return-strings-not-bytes
		reader = csv.DictReader(filewrapper, delimiter=',') 
		logger.append('file received')
		count = 0
		for data_dict in reader:
			form = ActivityCodeForm(data_dict)
			if form.is_valid():
				form.save()
				count += 1
			else:
				logger.append(str(list(data_dict.values())) + ' --> ' + str(form.errors.as_data()))
		# finish up
		logger.append('import finished')
		logger.append('successfully imported {} activity codes'.format(count))
		importresults = '\n'.join(logger) # make logs into a multiline textstring
		return render(request, 'templates/domain/edit_activitycodes.html', {'importresults':importresults})


def edit_activitysubcodes(request):
	if request.method == 'GET':
		return render(request, 'templates/domain/edit_activitysubcodes.html')
	elif request.method == 'POST':
		logger = [] # each entry will become a new line in a textstring
		uploaded_file = request.FILES['importdocument']
		import csv
		import io
		filewrapper = io.TextIOWrapper(uploaded_file, encoding=request.encoding) # see https://stackoverflow.com/questions/16243023/how-to-resolve-iterator-should-return-strings-not-bytes
		reader = csv.DictReader(filewrapper, delimiter=',') 
		logger.append('file received')
		count = 0
		for data_dict in reader:
			form = ActivitySubcodeForm(data_dict)
			if form.is_valid():
				form.save()
				count += 1
			else:
				logger.append(str(list(data_dict.values())) + ' --> ' + str(form.errors.as_data()))
		# finish up
		logger.append('import finished')
		logger.append('successfully imported {} activity subcodes'.format(count))
		importresults = '\n'.join(logger) # make logs into a multiline textstring
		return render(request, 'templates/domain/edit_activitysubcodes.html', {'importresults':importresults})


def edit_actorcodes(request):
	if request.method == 'GET':
		return render(request, 'templates/domain/edit_actorcodes.html')
	elif request.method == 'POST':
		logger = [] # each entry will become a new line in a textstring
		uploaded_file = request.FILES['importdocument']
		import csv
		import io
		filewrapper = io.TextIOWrapper(uploaded_file, encoding=request.encoding) # see https://stackoverflow.com/questions/16243023/how-to-resolve-iterator-should-return-strings-not-bytes
		reader = csv.DictReader(filewrapper, delimiter=',') 
		logger.append('file received')
		count = 0
		for data_dict in reader:
			form = ActorCodeForm(data_dict)
			if form.is_valid():
				form.save()
				count += 1
			else:
				logger.append(str(list(data_dict.values())) + ' --> ' + str(form.errors.as_data()))
		# finish up
		logger.append('import finished')
		logger.append('successfully imported {} actor codes'.format(count))
		importresults = '\n'.join(logger) # make logs into a multiline textstring
		return render(request, 'templates/domain/edit_actorcodes.html', {'importresults':importresults})


def edit_statuscodes(request):
	if request.method == 'GET':
		return render(request, 'templates/domain/edit_statuscodes.html')
	elif request.method == 'POST':
		logger = [] # each entry will become a new line in a textstring
		uploaded_file = request.FILES['importdocument']
		import csv
		import io
		filewrapper = io.TextIOWrapper(uploaded_file, encoding=request.encoding) # see https://stackoverflow.com/questions/16243023/how-to-resolve-iterator-should-return-strings-not-bytes
		reader = csv.DictReader(filewrapper, delimiter=',') 
		logger.append('file received')
		count = 0
		for data_dict in reader:
			form = StatusCodeForm(data_dict)
			if form.is_valid():
				form.save()
				count += 1
			else:
				logger.append(str(list(data_dict.values())) + ' --> ' + str(form.errors.as_data()))
		# finish up
		logger.append('import finished')
		logger.append('successfully imported {} status codes'.format(count))
		importresults = '\n'.join(logger) # make logs into a multiline textstring
		return render(request, 'templates/domain/edit_statuscodes.html', {'importresults':importresults})


def edit_financialcodes(request):
	if request.method == 'GET':
		return render(request, 'templates/domain/edit_financialcodes.html')
	elif request.method == 'POST':
		logger = [] # each entry will become a new line in a textstring
		uploaded_file = request.FILES['importdocument']
		import csv
		import io
		filewrapper = io.TextIOWrapper(uploaded_file, encoding=request.encoding) # see https://stackoverflow.com/questions/16243023/how-to-resolve-iterator-should-return-strings-not-bytes
		reader = csv.DictReader(filewrapper, delimiter=',') 
		logger.append('file received')
		count = 0
		for data_dict in reader:
			form = FinancialCodeForm(data_dict)
			if form.is_valid():
				form.save()
				count += 1
			else:
				logger.append(str(list(data_dict.values())) + ' --> ' + str(form.errors.as_data()))
		# finish up
		logger.append('import finished')
		logger.append('successfully imported {} financial codes'.format(count))
		importresults = '\n'.join(logger) # make logs into a multiline textstring
		return render(request, 'templates/domain/edit_financialcodes.html', {'importresults':importresults})


def edit_sourcecodes(request):
	if request.method == 'GET':
		return render(request, 'templates/domain/edit_sourcecodes.html')
	elif request.method == 'POST':
		logger = [] # each entry will become a new line in a textstring
		uploaded_file = request.FILES['importdocument']
		import csv
		import io
		filewrapper = io.TextIOWrapper(uploaded_file, encoding=request.encoding) # see https://stackoverflow.com/questions/16243023/how-to-resolve-iterator-should-return-strings-not-bytes
		reader = csv.DictReader(filewrapper, delimiter=',') 
		logger.append('file received')
		count = 0
		for data_dict in reader:
			form = SourceCodeForm(data_dict)
			if form.is_valid():
				form.save()
				count += 1
			else:
				logger.append(str(list(data_dict.values())) + ' --> ' + str(form.errors.as_data()))
		# finish up
		logger.append('import finished')
		logger.append('successfully imported {} source codes'.format(count))
		importresults = '\n'.join(logger) # make logs into a multiline textstring
		return render(request, 'templates/domain/edit_sourcecodes.html', {'importresults':importresults})


def edit_triggerwords(request):
	if request.method == 'GET':
		return render(request, 'templates/domain/edit_triggerwords.html')
	elif request.method == 'POST':
		logger = [] # each entry will become a new line in a textstring
		uploaded_file = request.FILES['importdocument']
		import csv
		import io
		filewrapper = io.TextIOWrapper(uploaded_file, encoding=request.encoding) # see https://stackoverflow.com/questions/16243023/how-to-resolve-iterator-should-return-strings-not-bytes
		reader = csv.DictReader(filewrapper, delimiter=',') 
		logger.append('file received')
		count = 0
		for data_dict in reader:
			form = TriggerWordForm(data_dict)
			if form.is_valid():
				form.save()
				count += 1
			else:
				logger.append(str(list(data_dict.values())) + ' --> ' + str(form.errors.as_data()))
		# finish up
		logger.append('import finished')
		logger.append('successfully imported {} trigger words'.format(count))
		importresults = '\n'.join(logger) # make logs into a multiline textstring
		return render(request, 'templates/domain/edit_triggerwords.html', {'importresults':importresults})