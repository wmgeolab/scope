from django.shortcuts import render, redirect
from django.apps import apps

import os

from domain.models import ActivityCode, ActivitySubcode, ActorCode, ActorRole, DateCode, StatusCode, FinancialCode
from sourcing_m.models import Source
from extracting_m.models import Extract
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
    extracts = Extract.objects.filter(current_status="EXTQ")

    # check if user already has checked out a source
    try:
        cont = Extract.objects.get(current_user=request.user)
        print(cont)
    except:
        cont = None

    return render(request, 'templates/parsing_m/extract_list.html', {'extracts':extracts, 'cont':cont})

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
        #check if the activity has been created before, or if this first time
        try:
            activity = Activity.objects.get(extract=extract)
        except:
            activity = None

        if (activity):
            form = ActivityForm(instance=activity)
        else:
            form = ActivityForm(initial={'extract':pk})

        context = {'extract':extract,'form':form}
        return render(request, 'templates/parsing_m/extract_parse.html', context)

    elif request.method == 'POST':
        extract = Extract.objects.get(pk=pk)
        #if you want to edit an existing entry, you have to give it that instance
        try:
            activity = Activity.objects.get(extract=extract)
        except:
            activity = None

        if (activity):
            form = ActivityForm(request.POST, instance=activity)
        else:
            form = ActivityForm(request.POST)

        data = request.POST.copy()
        finish = request.POST.get('finish', 'no')
        print(data)

        if form.is_valid():
            form.save()
        else:
            print(form.errors)

        print(finish)
        if finish == 'yes':
            print('finish')
            # wait until we've revisited how things move between modules. I think the source om=mo
            extract.current_status = 'PARM'
            extract.current_user = None
            extract.save()
            activity = Activity.objects.get(extract=extract)
            activity.current_status = 'PARM'
            activity.current_user = None
            activity.save()
            return redirect('extract_list')
        else:
            print('save')
            return redirect('extract_parse', pk)


# Put utility functions here

def user_is_busy(user, extract):
    # check if the user already has checked out another extract (ie different from a reference extract)
    print('checking if user is busy')
    try:
        user_extract = Extract.objects.get(current_user=user)
    except Extract.DoesNotExist:
        user_extract = None
    print(user_extract, extract)
    if user_extract and user_extract != extract:
        errormsg = {'type':'user_busy', 'busy_with':user_extract}
        print(errormsg)
        return errormsg

def extract_is_busy(user, extract):
    print('checking if extract is busy', user, extract, extract.current_user)
    # check if someone else is currently working on this source
    if extract.current_user and extract.current_user != user:
        errormsg = {'type':'extract_busy', 'current_user':extract.current_user}
        print(errormsg)
        return errormsg

def extract_needs_checkout(user, extract):
    print('checking if extract needs checkout', user, extract, extract.current_user)
    # check if the source needs to be checked out
    if extract.current_user is None:
        errormsg = {'type':'extract_needs_checkout'}
        print(errormsg)
        return errormsg

def check_illegal_extract_modification(user, extract):
    # do a number of checks to see if user is "illegally" trying to modify an extract
    # returning the first encountered error
    
    # check
    err = user_is_busy(user, extract)
    if err:
        msg = "You tried to modify an extract different than the one you already have checked out."
        return msg

    # check
    err = extract_is_busy(user, extract)
    if err:
        msg = "You tried to modify an extract that is already checked out by {}. Please checkout a different extract.".format(err['current_user'])
        return msg

    # check
    err = extract_needs_checkout(user, extract)
    if err:
        msg = "You tried to modify an extract that isn't checked out. Please checkout the extract first."
        return msg

def check_illegal_extract_checkout(user, extract):
    # do a number of checks to see if user is "illegally" trying to checkout an extract
    # returning the first encountered error
    
    # check
    err = user_is_busy(user, extract)
    if err:
        msg = "You tried to checkout an extract different than the one you already have checked out."
        return msg

    # check
    err = source_is_busy(user, extract)
    if err:
        msg = "You tried to checkout an extract that is already checked out by {}. Please checkout a different extract.".format(err['current_user'])
        return msg
