from django.shortcuts import render

from modSourcing.models import Source


# Create your views here.
def home(request, pk):
    try:
        cont = Source.objects.get(pk = pk)
    except:
        cont = None
    return render(request, 'templates/extracts/home.html', {'continue':cont,})

def source_list(request):
    sources = Source.objects.filter(current_user = None)
    return render(request, 'templates/extracts/source_list.html', {'sources':sources,})

def source_checkout(request, pk):
    source = Source.objects.get(pk = pk)
    source.current_user = request.user
    return redirect('source_extract')



