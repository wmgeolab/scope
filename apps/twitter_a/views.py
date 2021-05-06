from django.shortcuts import render, redirect
from django.apps import apps
from django.template import Context
from django.core.files.storage import FileSystemStorage

import os
from .forms import TwitterSearchForm
from .models import *
from .twitter_search import *

# Create your views here.

def home(request):
    return redirect("twitter_import")

def twitter_import(request):
    if request.method == 'POST':
        form = TwitterSearchForm(request.POST)
        vals = []
        if form.is_valid():
            form.save(commit=False)
            pkw = []
            skw = []
            tkw = []
            for i in form.cleaned_data['primary_keywords'].split(','):  pkw.append(i.strip())
            for i in form.cleaned_data['secondary_keywords'].split(','):  skw.append(i.strip())
            for i in form.cleaned_data['tertiary_keywords'].split(','):  tkw.append(i.strip())
            tweets = twitter_search(form.cleaned_data['start_date'].strftime('%m/%d/%Y'), form.cleaned_data['end_date'].strftime('%m/%d/%Y'), pkw, skw, tkw)
            for x in tweets:
                TwitterSource.objects.create(source_id=x.source_id, source_text=x.source_text, source_date=x.source_created_at, source_url=x.source_url)
            vals = TwitterSource.objects.all()
            return render(request, "templates/twitter_a/results.html", {'vals': vals})
    else:  form = TwitterSearchForm()
    return render(request, 'templates/twitter_a/search.html', {'form': form})

def twitter_results(request):
    if request.method == 'POST':
        return render(request, 'templates/twitter_a/results.html')

