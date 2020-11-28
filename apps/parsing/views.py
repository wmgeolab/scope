from django.shortcuts import render, redirect
from django.apps import apps

import os

from .models import ActorCode, ActivityCode, StatusCode, Activity
from .forms import ActorCodeForm, ActivityCodeForm, StatusCodeForm, ActivityForm

from sourcing.models import Source
from sourcing.forms import SourceForm

# Create your views here.

def home(request):
    sources = Source.objects.all()
    return render(request, 'templates/parsing/home.html', {'sources':sources,
                                                      })

def landing(request, current_user):
    # NOTE: maybe rename, and maybe just integrate directly into home? 
    try:
        continue_event = Activity.objects.get(current_user=current_user)
    except:
        continue_event = None
    context = {'continue_event': continue_event}
    return render(request, 'templates/parsing/landing.html', context)

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

def activity_checkout(request, pk):
    activity = Activity.objects.get(pk=pk)
    activity.current_user = None
    return redirect('activity_list')

def activity_release(request, pk):
    activity = Activity.objects.get(pk=pk)
    activity.current_user = request.user
    return redirect('activity_edit')

def activity_list():
    activities = Activity.objects.filter(current_user=None)
    context = {'activities': activities}
    return render('templates/parsing/activity_list.html', context)

def activity_edit(request, pk):
    if request.method == 'GET':
        activity = Activity.objects.get(pk=pk)
        form = ActivityForm(instance=activity)
        context = {'form': form}
        return render(request, 'templates/parsing/activity_edit.html', context)
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        #assert form.is_valid()
        form.save()
        return redirect('activity_release')

