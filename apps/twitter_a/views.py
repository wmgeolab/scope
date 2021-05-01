from django.shortcuts import render, redirect
from django.apps import apps
from django.template import Context
from django.core.files.storage import FileSystemStorage

import os
from .forms import TwitterSearchForm
from .models import *
from .twitter_search import *

# Create your views here.

class Abc:
    def __init__(self, a):
        self.source_text = a

def home(request):
    return redirect("twitter_import")

def twitter_import(request):
    vals = [1, 2, 3]
    if request.method == 'POST':
        form = TwitterSearchForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            pkw = []
            skw = []
            tkw = []
            for i in form.cleaned_data['primary_keywords'].split(','):  pkw.append(i.strip())
            for i in form.cleaned_data['secondary_keywords'].split(','):  skw.append(i.strip())
            for i in form.cleaned_data['tertiary_keywords'].split(','):  tkw.append(i.strip())
            # vals = twitter_search(form.cleaned_data['start_date'], form.cleaned_data['end_date'], pkw, skw, tkw)
            # for x in vals:  sql_conn(x)
            return render(request, "templates/twitter_a/results.html", {'vals': vals})
    else:  form = TwitterSearchForm()
    return render(request, 'templates/twitter_a/search.html', {'form': form})

def twitter_loading(request):
    return render(request, 'templates/twitter_a/loading.html')

def twitter_results(request):
    if request.method == 'POST':
        return render(request, 'templates/twitter_a/results.html')

