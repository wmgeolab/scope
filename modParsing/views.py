from django.shortcuts import render, redirect
from django.apps import apps

import os

from .models import ActorCode, ActivityCode, StatusCode, Activity
from .forms import ActorCodeForm, ActivityCodeForm, StatusCodeForm, ActivityForm

from modSourcing.models import Source
from modSourcing.forms import SourceForm

# Create your views here.

def home(request):
    sources = Source.objects.all()
    return render(request, 'templates/parsing/home.html', {'sources':sources,
                                                      })

##def settings(request):
##    activities = Activity.objects.all()
##    actorcodes = ActorCode.objects.all()
##    activitycodes = ActivityCode.objects.all()
##    statuscodes = StatusCode.objects.all()
##    return render(request, 'templates/parsing/settings.html', {'activities':activities,
##                                                         'actorcodes':actorcodes,
##                                                         'activitycodes':activitycodes,
##                                                      'statuscodes':statuscodes
##                                                      })

def settings(request):
    datamodels = list(apps.get_app_config('parsing').get_models())
    for datamodel in datamodels:
        datamodel.get_class_name = datamodel._meta.object_name
        datamodel.get_count = datamodel.objects.all().count()
    return render(request, 'templates/parsing/settings.html', {'datamodels':datamodels})

# generic model

def datamodel(request, name):
    datamodel = apps.get_app_config('parsing').get_model(name)
    datamodel.get_class_name = datamodel._meta.object_name
    datamodel.get_count = datamodel.objects.all().count()
    datamodel.get_fields = datamodel._meta.fields
    objects = [(obj,[getattr(obj,fl.name) for fl in datamodel.get_fields]) for obj in datamodel.objects.all()]
    return render(request, 'templates/parsing/datamodel.html', {'datamodel':datamodel, 'objects':objects})

def datamodel_view(request, name, pk):
    datamodel = apps.get_app_config('parsing').get_model(name)
    inst = datamodel.objects.get(pk=pk)
    from . import forms
    formclass = getattr(forms, name+'Form')
    if request.method == 'GET':
        form = formclass(instance=inst)
        return render(request, 'templates/parsing/datamodel_view.html', {'form':form, 'name':name, 'pk':pk})
    elif request.method == 'POST':
        form = formclass(request.POST)
        if form.is_valid():
            form.save()
            return redirect('parsing')
        else:
            print(form.errors)

def datamodel_add(request, name):
    app_models = apps.get_app_config('parsing').get_model(name)
    from . import forms
    formclass = getattr(forms, name+'Form')

    if request.method == 'GET':
        form = formclass()
        return render(request, 'templates/parsing/datamodel_add.html', {'form':form, 'name':name})
    elif request.method == 'POST':
        form = formclass(request.POST)
        if form.is_valid():
            form.save()
            return redirect('parsing')
        else:
            print(form.errors)

def datamodel_add_from_csv(request, name, csvstream):
    import csv
    datamodel = apps.get_app_config('parsing').get_model(name)
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
    for name in ['ActivityCode', 'ActorCode', 'StatusCode', 'Activity']:
        print(name)
        fil = 'parsing/data/'+name+'.csv'
        if os.path.lexists(fil):
            print('importing from', fil)
            csvstream = open(fil, encoding='utf-8')
            datamodel_add_from_csv(request, name, csvstream)

    return redirect('parsing_settings')

# actorcode

def actorcode_view(request, pk):
    actorcode = ActorCode.objects.get(pk=pk)
    form = ActorCodeForm(instance=actorcode)
    return render(request, 'templates/parsing/actorcode_view.html', {'form':form})

def actorcode_add(request):
    if request.method == 'GET':
        form = ActorCodeForm()
        return render(request, 'templates/parsing/actorcode_add.html', {'form':form})
    elif request.method == 'POST':
        form = ActorCodeForm(request.POST)
        #assert form.is_valid()
        form.save()
        return redirect('parsing')

# activitycode

def activitycode_view(request, pk):
    activitycode = ActivityCode.objects.get(pk=pk)
    form = ActivityCodeForm(instance=activitycode)
    return render(request, 'templates/parsing/activitycode_view.html', {'form':form})

def activitycode_add(request):
    if request.method == 'GET':
        form = ActivityCodeForm()
        return render(request, 'templates/parsing/activitycode_add.html', {'form':form})
    elif request.method == 'POST':
        form = ActivityCodeForm(request.POST)
        #assert form.is_valid()
        form.save()
        return redirect('parsing')

# statuscode

def statuscode_view(request, pk):
    statuscode = StatusCode.objects.get(pk=pk)
    form = StatusCodeForm(instance=statuscode)
    return render(request, 'templates/parsing/statuscode_view.html', {'form':form})

def statuscode_add(request):
    if request.method == 'GET':
        form = StatusCodeForm()
        return render(request, 'templates/parsing/statuscode_add.html', {'form':form})
    elif request.method == 'POST':
        form = StatusCodeForm(request.POST)
        #assert form.is_valid()
        form.save()
        return redirect('parsing')

# activity

def activity_view(request, pk):
    activity = Activity.objects.get(pk=pk)
    form = ActivityForm(instance=activity)
    return render(request, 'templates/parsing/activity_view.html', {'form':form})

def activity_add(request):
    if request.method == 'GET':
        form = ActivityForm()
        return render(request, 'templates/parsing/activity_add.html', {'form':form})
    elif request.method == 'POST':
        form = ActivityForm(request.POST)
        #assert form.is_valid()
        form.save()
        return redirect('parsing')



def landing(request, current_user):
    try:
        continue_event = Activity.objects.get(current_user=current_user)
    except:
        continue_event = None
    context = {'continue_event': continue_event}
    return render(request, 'templates/parsing/landing.html', context)
