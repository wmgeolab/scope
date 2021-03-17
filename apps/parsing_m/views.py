from django.shortcuts import render, redirect
from django.apps import apps
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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

    # check if user is logged in or busy
    if request.user.is_anonymous:
        messages.warning(request, 'You need to login before performing a task.')
        continue_extract = None
    else:
        continue_extract = user_is_busy(request.user, model=Extract)

    return render(request, 'templates/parsing_m/extract_list.html', {'extracts':extracts, 'continue_extract':continue_extract})

# extract_checkout (formerly activity_checkout)
@login_required
def extract_checkout(request, pk):
    extract = Extract.objects.get(pk=pk)

    # redirect if illegal extract checkout
    error = check_illegal_object_checkout(request, extract)
    if error:
        return redirect('extract_list')
    
    extract.current_user = request.user
    extract.save()
    return redirect('extract_parse', pk)

# extract_release (formerly activity_release)
@login_required
def extract_release(request, pk):
    extract = Extract.objects.get(pk=pk)

    # redirect if illegal extract modification
    error = check_illegal_object_modification(request, extract)
    if error:
        return redirect('extract_list')
    
    extract.current_user = None
    extract.save()
    return redirect('extract_list')

# extract_parse (formerly activity_edit)
@login_required
def extract_parse(request, pk):
    extract = Extract.objects.get(pk=pk)

    # redirect if illegal extract modification
    error = check_illegal_object_modification(request, extract)
    if error:
        return redirect('extract_list')
    
    if request.method == 'GET':
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

def user_is_busy(user, obj=None, model=None):
    '''Check if the user has already checked out any object (if given model class)
    or another object different from a reference object (if given model instance),
    and if so return that object. 
    Can be any model class or model instance with a 'current_user' field.
    '''
    #print('checking if user is busy', user, obj)
    
    # check if given instance or model, and get the model class
    if obj:
        # get model class from instance
        model = obj._meta.model
    elif model:
        # model class already given
        pass
    else:
        raise Exception('Either obj or model args must be given')

    print(model)
    # get object if user is busy
    try:
        user_busy_with = model.objects.get(current_user=user)
    except model.DoesNotExist:
        user_busy_with = None

    # return
    if user_busy_with and user_busy_with != obj:
        return user_busy_with

def object_is_busy(user, obj):
    '''Check if someone else is currently working on this object, and if so return the current user.
    Can be any model instance with a 'current_user' attr.
    '''
    #print('checking if object is busy', user, obj, obj.current_user)
    if obj.current_user and obj.current_user != user:
        return obj.current_user

def object_needs_checkout(user, obj):
    '''Check if the object needs to be checked out, and if so return True.
    Can be any model instance with a 'current_user' attr.
    '''
    #print('checking if object needs checkout', user, obj, obj.current_user)
    if obj.current_user is None:
        return True

def check_illegal_object_modification(request, obj):
    '''Do a number of checks to see if request.user is "illegally" trying to modify an object,
    returning the first encountered error, and add it to message notification. 
    '''
    model_name = obj._meta.verbose_name
    user = request.user
    
    # check
    err = user_is_busy(user, obj)
    if err:
        msg = "You tried to modify a {object_type} different than the one you already have checked out.".format(model_name)
        messages.error(request, msg)
        return msg

    # check
    err = object_is_busy(user, obj)
    if err:
        msg = "You tried to modify a {object_type} that is already checked out by {current_user}. Please checkout a different {object_type}.".format(object_type=model_name, current_user=err)
        messages.error(request, msg)
        return msg

    # check
    err = object_needs_checkout(user, obj)
    if err:
        msg = "You tried to modify a {object_type} that isn't checked out. Please checkout the {object_type} first.".format(object_type=model_name)
        messages.error(request, msg)
        return msg

def check_illegal_object_checkout(request, obj):
    '''Do a number of checks to see if request.user is "illegally" trying to checkout an object,
    returning the first encountered error, and add it to message notification. 
    '''
    model_name = obj._meta.verbose_name
    user = request.user
    
    # check
    err = user_is_busy(user, obj)
    if err:
        msg = "You tried to checkout a {object_type} different than the one you already have checked out.".format(object_type=model_name)
        messages.error(request, msg)
        return msg

    # check
    err = object_is_busy(user, obj)
    if err:
        msg = "You tried to checkout a {object_type} that is already checked out by {current_user}. Please checkout a different {object_type}.".format(object_type=model_name, current_user=err)
        messages.error(request, msg)
        return msg
