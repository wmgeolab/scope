from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
        error = user_is_busy(request.user, None)
        if error:
            continue_source = error['busy_with']
        else:
            continue_source = None

    return render(request, 'templates/extracting_m/source_list.html', {'sources':sources, 'continue_source':continue_source})

@login_required
def source_checkout(request, pk):
    source = Source.objects.get(pk=pk)
    
    # redirect if illegal source checkout
    error = check_illegal_source_checkout(request.user, source)
    if error:
        print('illegal action, redirect')
        messages.error(request, error)
        return redirect('source_list')
    
    source.current_user = request.user
    source.save()
    return redirect('source_extraction', pk)

@login_required
def source_release(request, pk):
    source = Source.objects.get(pk = pk)
    
    # redirect if illegal source modification
    error = check_illegal_source_modification(request.user, source)
    if error:
        print('illegal action, redirect')
        messages.error(request, error)
        return redirect('source_list')
    
    source.current_user = None
    source.save()
    return redirect('source_list')

@login_required
def source_extraction(request, pk):
    source = Source.objects.get(pk=pk)

    # redirect if illegal source modification
    error = check_illegal_source_modification(request.user, source)
    if error:
        print('illegal action, redirect')
        messages.error(request, error)
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
                obj.current_status = 'EXTM'
                obj.save()

            # manually save new objects to db
            for obj in formset.new_objects:
                if obj.text.strip():
                    obj.current_status = 'EXTM'
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
            return redirect('source_list')
        else:
            print('save')
            # only save, stay on the same page (reload the extraction page)
            return redirect('source_extraction', pk)



# Put utility functions here

def user_is_busy(user, source):
    # check if the user already has checked out another source (ie different from a reference source pk)
    print('checking if user is busy')
    try:
        user_source = Source.objects.get(current_user=user)
    except Source.DoesNotExist:
        user_source = None
    print(user_source, source)
    if user_source and user_source != source:
        errormsg = {'type':'user_busy', 'busy_with':user_source}
        print(errormsg)
        return errormsg

def source_is_busy(user, source):
    print('checking if source is busy', user, source, source.current_user)
    # check if someone else is currently working on this source
    if source.current_user and source.current_user != user:
        errormsg = {'type':'source_busy', 'current_user':source.current_user}
        print(errormsg)
        return errormsg

def source_needs_checkout(user, source):
    print('checking if source needs checkout', user, source, source.current_user)
    # check if the source needs to be checked out
    if source.current_user is None:
        errormsg = {'type':'source_needs_checkout'}
        print(errormsg)
        return errormsg

def check_illegal_source_modification(user, source):
    # do a number of checks to see if user is "illegally" trying to modify a source
    # returning the first encountered error
    
    # check
    err = user_is_busy(user, source)
    if err:
        msg = "You tried to modify a source different than the one you already have checked out."
        return msg

    # check
    err = source_is_busy(user, source)
    if err:
        msg = "You tried to modify a source that is already checked out by {}. Please checkout a different source.".format(err['current_user'])
        return msg

    # check
    err = source_needs_checkout(user, source)
    if err:
        msg = "You tried to modify a source that isn't checked out. Please checkout the source first."
        return msg

def check_illegal_source_checkout(user, source):
    # do a number of checks to see if user is "illegally" trying to checkout a source
    # returning the first encountered error
    
    # check
    err = user_is_busy(user, source)
    if err:
        msg = "You tried to checkout a source different than the one you already have checked out."
        return msg

    # check
    err = source_is_busy(user, source)
    if err:
        msg = "You tried to checkout a source that is already checked out by {}. Please checkout a different source.".format(err['current_user'])
        return msg



