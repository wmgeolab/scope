from django.shortcuts import render

# Create your views here.
def home(request, pk = pk):
    try:
        continue = Source.objects.get(pk = pk)
    except:
        continue = None
    return render(request, 'templates/extracts/home.html', {'continue':continue,})
