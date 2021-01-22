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
        importresults = [] # each entry will become a new line in a textstring
        uploaded_file = request.FILES['importdocument']
        file_data = uploaded_file.read().decode("utf-8")
        importresults.append('file received')
        lines = file_data.split("\n")
        count = 0
        for line in lines:
            fields = line.split(",")
            data_dict = {}
            data_dict["source_code"] = fields[0]
            data_dict["source_url"] = fields[1]
            data_dict["source_html"] = fields[2]
            data_dict["source_text"] = fields[3]
            data_dict["source_date"] = fields[4]
            form = SourceForm(data_dict)
            if form.is_valid():
                form.save()
                count += 1
            else:
                print(line)
                importresults.append(str(line) + ' --> ' + str(form.errors.as_data()))
        # finish up
        importresults.append('import finished')
        importresults.append('successfully imported {} sources'.format(count))
        importresults = '\n'.join(importresults) # make importresults into a multiline textstring
        return render(request, 'templates/sourcing/source_import.html', {'importresults':importresults})
        
