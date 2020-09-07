from django.shortcuts import render, redirect
from django.apps import apps

import os

from .models import Source
from .forms import SourceForm

# Create your views here.

def home(request):
    sources = Source.objects.all()
    return render(request, 'templates/sourcing/home.html', {'sources':sources})

def settings(request):
    datamodels = list(apps.get_app_config('sourcing').get_models())
    for datamodel in datamodels:
        datamodel.get_class_name = datamodel._meta.object_name
        datamodel.get_count = datamodel.objects.all().count()
    return render(request, 'templates/sourcing/settings.html', {'datamodels':datamodels})

# generic model

def datamodel(request, name):
    datamodel = apps.get_app_config('sourcing').get_model(name)
    datamodel.get_class_name = datamodel._meta.object_name
    datamodel.get_count = datamodel.objects.all().count()
    datamodel.get_fields = datamodel._meta.fields
    objects = [(obj,[getattr(obj,fl.name) for fl in datamodel.get_fields]) for obj in datamodel.objects.all()]
    return render(request, 'templates/sourcing/datamodel.html', {'datamodel':datamodel, 'objects':objects})

def datamodel_view(request, name, pk):
    datamodel = apps.get_app_config('sourcing').get_model(name)
    inst = datamodel.objects.get(pk=pk)
    from . import forms
    formclass = getattr(forms, name+'Form')
    if request.method == 'GET':
        form = formclass(instance=inst)
        return render(request, 'templates/sourcing/datamodel_view.html', {'form':form, 'name':name, 'pk':pk})
    elif request.method == 'POST':
        form = formclass(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sourcing')
        else:
            print(form.errors)

def datamodel_add(request, name):
    app_models = apps.get_app_config('sourcing').get_model(name)
    from . import forms
    formclass = getattr(forms, name+'Form')
    
    if request.method == 'GET':
        form = formclass()
        return render(request, 'templates/sourcing/datamodel_add.html', {'form':form, 'name':name})
    elif request.method == 'POST':
        form = formclass(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sourcing')
        else:
            print(form.errors)

def datamodel_add_from_csv(request, name, csvstream):
    import csv
    datamodel = apps.get_app_config('sourcing').get_model(name)
    dialect = csv.Sniffer().sniff(csvstream.read(1024))
    csvstream.seek(0)
    
    reader = csv.DictReader(csvstream, dialect=dialect)
    for row in reader:
        for k in list(row.keys()):
            # some csv files have annoying start-of-file junk characters
            if k.startswith('\ufeff'):
                val = row.pop(k)
                k = k.replace('\ufeff','')
                row[k] = val
            # get related model instance from id
            field = getattr(datamodel, k).field
            if field.is_relation:
                _id = row[k]
                obj = field.related_model.objects.get(pk=_id)
                row[k] = obj
        print(row)
                
        obj = datamodel(**row)
        obj.save()
        print(obj)

def import_from_data_folder(request):
    for name in ['SourceCode', 'Source']:
        print(name)
        fil = 'sourcing/data/'+name+'.csv'
        if os.path.lexists(fil):
            print('importing from', fil)
            csvstream = open(fil, encoding='utf-8')
            datamodel_add_from_csv(request, name, csvstream)

    return redirect('sourcing_settings')
    

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
