from django.shortcuts import render, redirect

from sourcing_m.models import Source

from extracting_m.models import Extract

from parsing_m.models import Activity

from .forms import ExtractQAForm


# Create your views here.
def home(request):
    return redirect('extract_list_qa')


def extract_list_qa(request):
    # get all extracts
    extracts = Extract.objects.filter(current_status="EXTM")

    # check if user already has checked out a source
    try:
        cont = Extract.objects.get(current_user=request.user)
        print(cont)
    except:
        cont = None

    return render(request, 'templates/extracting_qa/extract_list_qa.html', {'extracts':extracts, 'cont':cont})


def extract_list_complete(request):
    # get all extracts
    extracts = Extract.objects.all()

    return render(request, 'templates/extracting_qa/extract_list_complete.html', {'extracts':extracts})


# extract_qa
def extract_qa(request, pk):
    extract = Extract.objects.get(pk=pk)
    extract.current_user = request.user
    extract.save()
    return redirect('extract_assess', pk)


# extract_release
def extract_release_qa(request, pk):
    extract = Extract.objects.get(pk=pk)
    extract.current_user = None
    extract.save()
    return redirect('extract_list_qa')


# extract_assess (formerly activity_edit)
def extract_assess(request, pk):
    if request.method == 'GET':
        extract = Extract.objects.get(pk=pk)

        form = ExtractQAForm(initial={'extract':pk})

        context = {'extract':extract,'form':form}
        return render(request, 'templates/extracting_qa/extract_qa.html', context)

    elif request.method == 'POST':
        extract = Extract.objects.get(pk=pk)
        source = Source.objects.get(id=extract.source.id)

        form = ExtractQAForm(request.POST, instance=extract)

        data = request.POST.copy()
        finish = request.POST.get('finish', 'no')
        print(data)

        if form.is_valid():
            form.save()
        else:
            print(form.errors)

        if finish == 'yes':
            print('send forward')
            extract.current_status = 'EXTQ'
            extract.current_user = None
            extract.save()
        else:
            print('send backward')
            Activity.objects.filter(extract__in=Extract.objects.filter(source=extract.source.id)).delete() #any way to save this in another model or should we just completely delete it?
            source.current_status = 'SRCM'
            source.save()
            #Extract.objects.filter(source=extract.source.id).delete() #change this later to edit instead of delete. Requires checking for existing extract in the extraction/views.py
            extracts = Extract.objects.filter(source=extract.source.id)
            for obj in extracts:
                print(obj)
                print(obj.current_status)
                obj.current_status = 'EXTM'
                obj.save()
            extract.current_status = 'EXTM'
            extract.current_user = None
            extract.save()

        return redirect('extract_list_qa')