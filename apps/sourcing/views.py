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


def source_import(request):
    if request.method == 'GET':
        return render(request, 'templates/sourcing/source_import.html')
    elif request.method == 'POST':
        uploaded_file = request.FILES['importdocument']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        return redirect('sourcing')
        