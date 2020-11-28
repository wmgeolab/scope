from django.shortcuts import render, redirect
from django.apps import apps

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
