from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import nltk
from nltk import find
from nltk import sent_tokenize

from domain.models import TriggerWord
from sourcing_m.models import Source

from .models import Extract
from .forms import ExtractFormSet


# Create your views here.
def home(request):
    return redirect('source_list')

def source_list(request):
    # get all sources
    sources = Source.objects.filter(current_status='SRCM') #filter(current_user = None)

    # check if user is logged in or busy
    if request.user.is_anonymous:
        messages.warning(request, 'You need to login before performing a task.')
        continue_source = None
    else:
        continue_source = user_is_busy(request.user, model=Source)

    return render(request, 'templates/extracting_m/source_list.html', {'sources':sources, 'continue_source':continue_source})

@login_required
def source_checkout(request, pk):
    source = Source.objects.get(pk=pk)
    
    # redirect if illegal source checkout
    error = check_illegal_object_checkout(request, source)
    if error:
        return redirect('source_list')
    
    source.current_user = request.user
    source.save()
    return redirect('source_extraction', pk)

@login_required
def source_release(request, pk):
    source = Source.objects.get(pk = pk)
    
    # redirect if illegal source modification
    error = check_illegal_object_modification(request, source)
    if error:
        return redirect('source_list')
    
    source.current_user = None
    source.save()
    return redirect('source_list')

@login_required
def source_extraction(request, pk):
    source = Source.objects.get(pk=pk)

    # redirect if illegal source modification
    error = check_illegal_object_modification(request, source)
    if error:
        return redirect('source_list')
    
    if request.method == 'GET':
        extracts = source.extracts.all()
        formset = ExtractFormSet(queryset=Extract.objects.filter(pk__in=extracts),
                                 initial=[{'source':pk}]
                                 )
        return render(request, 'templates/extracting_m/source_extraction.html', {'source':source,
                                                                             'formset':formset,}
                      )

    elif request.method == 'POST':
        extracts = source.extracts.all()

        # get data
        data = request.POST.copy()
        finish = request.POST.get('finish', 'no')
        print(data)

        # force set the source
##        num_forms = int(data['form-TOTAL_FORMS'])
##        for i in range(num_forms):
##            data['form-{}-source'.format(i)] = str(pk)
##        print(data)

        # create form
        formset = ExtractFormSet(data,
                                 queryset=Extract.objects.filter(pk__in=extracts), # to compare with original instances which were changed
                                 )

        # save valid and non-empty forms
        if formset.is_valid():
            # register changed, new, and deleted objects (without saving to db)
            formset.save(commit=False)

            # manually save changed objects to db
            for obj,changed_data in formset.changed_objects:
                #obj.current_status = 'EXTM'
                obj.save()

            # manually save new objects to db
            for obj in formset.new_objects:
                if obj.text.strip():
                    #obj.current_status = 'EXTM'
                    # only save if form text is non-empty (ie the 'extra' forms)
                    obj.save()

            # manually delete objects from db
            for obj in formset.deleted_objects:
                if obj is not None:
                    # if you try to delete a box the first time extracting from a source then the extract isn't created yet and 'instance' will be None
                    obj.delete()

        else:
            for err in formset.errors:
                print(err)
            raise Exception

        # what to do after saving the data
        print(finish)
        if finish == 'yes':
            print('finish')
            # finish by marking the source as extracted
            source.current_status = 'EXTM'
            source.current_user = None # also release from checkout
            source.save()
            # then redirect to list of sources for extraction
            extract = Extract.objects.filter(source=source)
            for obj in extract:
                obj.current_status = 'EXTM'
                obj.current_user = None
                obj.save()
            return redirect('source_list')
        else:
            print('save')
            # only save, stay on the same page (reload the extraction page)
            return redirect('source_extraction', pk)



@login_required
def source_autoassist(request, pk):
    source = Source.objects.get(pk=pk)

    # redirect if illegal source modification
    error = check_illegal_object_modification(request, source)
    if error:
        return redirect('source_list')

    source_text = source.source_text
    print(source_text)
    triggerwords = TriggerWord.objects.all()

    for trigger in triggerwords:
        tw = trigger.triggerword
        if (source_text.find(tw) > 0):
            print(tw, " - found")
            sent_tokens = sent_tokenize(source_text)
            n = 0
            for sent in sent_tokens:
                e = n + 3
                if (sent.find(tw) > 0):

                    try:
                        extract_text = ' '.join(sent_tokens[n:e])
                    except:
                        extract_text = sent_tokens[n]

                    extract = Extract(source=source, text=extract_text)
                    extract.save()

                n += 1

    return redirect('source_extraction', pk)

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



