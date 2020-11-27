from django.shortcuts import render

from modSourcing.models import Source

from modExtracts.forms import ExtractFormSet


# Create your views here.
def home(request):
    # check if user already has checked out a source
    try:
        cont = Source.objects.get(current_user=request.user)
    except:
        cont = None
        
    if cont:
        # if yes, redirect to source extraction page
        redirect('source_extraction', cont.pk)
    else:
        # otherwise, show list of sources available for checking out
        return redirect('source_list')

def source_list(request):
    sources = Source.objects.filter(current_user = None)
    return render(request, 'templates/extracts/source_list.html', {'sources':sources,})

def source_checkout(request, pk):
    source = Source.objects.get(pk = pk)
    source.current_user = request.user
    return redirect('source_extract')

def source_release(request, pk):
    source = Source.objects.get(pk = pk)
    source.current_user = None
    return redirect('source_extract')

def source_extraction(request, pk):
    if request.method == 'GET':
        source = Source.objects.get(pk=pk)
        extracts = source.extracts.all()
        formset = ExtractFormSet(queryset=Extract.objects.filter(pk__in=extracts))
        return render(request, 'templates/extracts/source_extraction.html', {'formset':formset,})

    elif request.method == 'POST':
        formset = ExtractFormSet(request.POST)
        if formset.is_valid():
            formset.save()
        else:
            raise Exception('Failed to save...') # need better handling here
        
        return redirect('source_release')


