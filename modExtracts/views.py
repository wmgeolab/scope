from django.shortcuts import render

# Create your views here.
def home(request, pk = pk):
    try:
        continue = Source.objects.get(pk = pk)
    except:
        continue = None
    return render(request, 'templates/extracts/home.html', {'continue':continue,})

def source_list():
    sources = Source.objects.filter(current_user = None)
    return render(request, 'templates/extracts/source_list.html', {'sources':sources,})
