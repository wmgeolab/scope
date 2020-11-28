from django.shortcuts import render, redirect

from sourcing.models import Source

from .models import Extract
from .forms import ExtractFormSet


# Create your views here.
def home(request):
    # check if user already has checked out a source
    try:
        cont = Source.objects.get(current_user=request.user)
    except:
        cont = None
        
    if cont:
        # if yes, redirect to source extraction page
        return redirect('source_extraction', cont.pk)
    else:
        # otherwise, show list of sources available for checking out
        return redirect('source_list')

def source_list(request):
    sources = Source.objects.filter(current_user = None)
    return render(request, 'templates/extraction/source_list.html', {'sources':sources,})

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
        import urllib
        source_html = urllib.request.urlopen(source.source_url).read()
        extracts = source.extracts.all()
        formset = ExtractFormSet(queryset=Extract.objects.filter(pk__in=extracts))
        return render(request, 'templates/extraction/source_extraction.html', {'source':source,
                                                                             'source_html':source_html,
                                                                             'formset':formset,}
                      )

    elif request.method == 'POST':
        formset = ExtractFormSet(request.POST)
        if formset.is_valid():
            formset.save()
        else:
            raise Exception('Failed to save...') # need better handling here
        
        return redirect('source_release')


