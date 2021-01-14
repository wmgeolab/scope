from django.shortcuts import render, redirect

from sourcing.models import Source

from .models import Extract
from .forms import ExtractFormSet


# Create your views here.
def home(request):

    return redirect('source_list')

def source_list(request):
    # check if user already has checked out a source
    sources = Source.objects.all() #filter(current_user = None)

    try:
        cont = Source.objects.get(current_user=request.user)
    except:
        cont = None

    return render(request, 'templates/extraction/source_list.html', {'sources':sources, 'cont':cont})

def source_checkout(request, pk):
    source = Source.objects.get(pk = pk)
    source.current_user = request.user
    source.save()
    return redirect('source_extraction', pk)

def source_release(request, pk):
    source = Source.objects.get(pk = pk)
    source.current_user = None
    source.save()
    return redirect('source_list')

def source_extraction(request, pk):
    if request.method == 'GET':
        source = Source.objects.get(pk=pk)
        extracts = source.extracts.all()
        formset = ExtractFormSet(queryset=Extract.objects.filter(pk__in=extracts),
                                 initial=[{'source':pk}]
                                 )
        return render(request, 'templates/extraction/source_extraction.html', {'source':source,
                                                                             'formset':formset,}
                      )

    elif request.method == 'POST':
        source = Source.objects.get(pk=pk)
        extracts = source.extracts.all()

        # get data
        data = request.POST.copy()
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

        # handle models marked for deletion
        for form in formset.deleted_forms:
            print('del',form.cleaned_data)
            obj = form.cleaned_data['id']
            obj.delete()

        # save valid and non-empty forms
        if formset.is_valid():
            # register changed, new, and deleted objects (without saving to db)
            formset.save(commit=False)

            # manually save changed objects to db
            for obj in formset.changed_objects:
                obj.save()

            # manually save new objects to db
            for obj in formset.new_objects:
                if obj.text.strip():
                    # only save if form text is non-empty (ie the 'extra' forms)
                    obj.save()

            # manually delete objects from db
            for obj in formset.deleted_objects:
                obj.delete()

        else:
            for err in formset.errors:
                print(err)
            raise Exception

        return redirect('source_release', pk)
