from django.shortcuts import render, redirect
from django.apps import apps

import os

from sourcing.models import Source
from extraction.models import Extract
from .models import Activity

from .forms import  ActivityForm


# Create your views here.
def home(request):
    return redirect('extract_list')

# extract_list (formerly source_list)
def extract_list(request):
    # get all extracts
    #sources = Source.objects.filter(current_status='EX') #filter(current_user = None)
    #print(sources)
    #obviously this isn't how to access a queryset, but for illustrative purposes
    #how do I get only the extracts which have been submitted, since we don't have a "current_status" field in the extract model
    extracts = Extract.objects.filter(source_id__current_status="EX")

    # check if user already has checked out a source
    try:
        cont = Extract.objects.get(current_user=request.user)
        print(cont)
    except:
        cont = None

    return render(request, 'templates/parsing/extract_list.html', {'extracts':extracts, 'cont':cont})

# extract_checkout (formerly activity_checkout)
def extract_checkout(request, pk):
    extract = Extract.objects.get(pk=pk)
    extract.current_user = request.user
    extract.save()
    return redirect('extract_parse', pk)

# extract_release (formerly activity_release)
def extract_release(request, pk):
    extract = Extract.objects.get(pk=pk)
    extract.current_user = None
    extract.save()
    return redirect('extract_list')

# extract_parse (formerly activity_edit)
def extract_parse(request, pk):
    if request.method == 'GET':
        extract = Extract.objects.get(pk=pk)
        form = ActivityForm(instance=extract)
        context = {'form': form}
        return render(request, 'templates/parsing/extract_parse.html', {'extract':extract,'context':context})
    elif request.method == 'POST':
        form = ActivityForm(request.POST)
        assert form.is_valid()
        form.save()
        return redirect('extract_release')