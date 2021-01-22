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

# fix this later
def source_import_test(request):
    testresults = {}
    sdfghj
    #return testresults
    # if request.method == 'GET':
    #     return render(request, 'templates/sourcing/source_import.html')
    # elif request.method == 'POST':
    #     testresults = {}
    #     uploaded_file = request.FILES['importdocument']
    #     file_data = uploaded_file.read().decode("utf-8")
    return render(request, 'templates/sourcing/source_import.html', testresults)

# make this more robust later
def source_import(request):
    if request.method == 'GET':
        return render(request, 'templates/sourcing/source_import.html')
    elif request.method == 'POST':
        uploaded_file = request.FILES['importdocument']
        file_data = uploaded_file.read().decode("utf-8")
        lines = file_data.split("\n")
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
            else:
                print(line)
                print(form.errors.as_data())
                return render(request, 'templates/sourcing/source_import.html')
        return redirect('sourcing')
        