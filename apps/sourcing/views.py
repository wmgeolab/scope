from django.shortcuts import render, redirect
from django.apps import apps

from django.core.files.storage import FileSystemStorage

import os

from .models import Source
from .forms import SourceForm

# Create your views here.

def home(request):
    sources = Source.objects.all()
    return render(request, 'templates/sourcing/home.html', {'sources':sources})

# source

def source_view(request, pk):
    source = Source.objects.get(pk=pk)
    form = SourceForm(instance=source)
    return render(request, 'templates/sourcing/source_view.html', {'form':form, 'pk':pk})


def source_add(request):
    if request.method == 'GET':
        form = SourceForm()
        return render(request, 'templates/sourcing/source_add.html', {'form':form})
    elif request.method == 'POST':
        form = SourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sourcing')
        else:
            print(form.errors)

# make this more robust later
def source_import(request):
    if request.method == 'GET':
        return render(request, 'templates/sourcing/source_import.html')
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
            form = SourceForm(data_dict)
            if form.is_valid():
                form.save()
                count += 1
            else:
                logger.append(str(list(data_dict.values())) + ' --> ' + str(form.errors.as_data()))
        # finish up
        logger.append('import finished')
        logger.append('successfully imported {} sources'.format(count))
        importresults = '\n'.join(logger) # make logs into a multiline textstring
        return render(request, 'templates/sourcing/source_import.html', {'importresults':importresults})
        
