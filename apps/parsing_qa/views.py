from django.shortcuts import render, redirect

from sourcing_m.models import Source

from extracting_m.models import Extract

from parsing_m.models import Activity

from .forms import ActivityQAForm


# Create your views here.
def home(request):
    return redirect('activity_list_qa')

def activity_list_qa(request):
    # get all activities
    activities = Activity.objects.filter(extract__current_status="PARM", current_status="PARM")

    # check if user already has checked out a source
    try:
        cont = Activity.objects.get(current_user=request.user)
        print(cont)
    except:
        cont = None

    return render(request, 'templates/parsing_qa/activity_list_qa.html', {'activities':activities, 'cont':cont})


def activity_list_complete(request):
    # get all extracts
    activities = Activity.objects.all()

    return render(request, 'templates/parsing_qa/activity_list_complete.html', {'activities':activities})


# activity_qa
def activity_qa(request, pk):
    activity = Activity.objects.get(pk=pk)
    activity.current_user = request.user
    activity.save()
    return redirect('activity_assess', pk)

# activity_release
def activity_release_qa(request, pk):
    activity = Activity.objects.get(pk=pk)
    activity.current_user = None
    activity.save()
    return redirect('activity_list_qa')

# activity_assess
def activity_assess(request, pk):
    if request.method == 'GET':
        activity = Activity.objects.get(pk=pk)

        form = ActivityQAForm(initial={'activity':pk})

        context = {'activity':activity,'form':form}
        return render(request, 'templates/parsing_qa/activity_qa.html', context)

    elif request.method == 'POST':
        activity = Activity.objects.get(pk=pk)
        extract = Extract.objects.get(id=activity.extract.id)
        #if you want to edit an existing entry, you have to give it that instance
        #try:
        #    activity = Activity.objects.get(activity=activity)
        #except:
        #    activity = None

        #if (activity):
        form = ActivityQAForm(request.POST, instance=activity)
        #else:
        #    form = ActivityQAForm(request.POST)


        data = request.POST.copy()
        finish = request.POST.get('finish', 'no')
        print(data)

        if form.is_valid():
            form.save()
        else:
            print(form.errors)

        if finish == 'yes':
            print('send forward')
            activity.current_status = 'PARQ'
            activity.current_user = None
            activity.save()
        else:
        	print('send backward')
        	extract.current_status = 'EXTQ'
        	extract.save()
        	activity.current_user = None
        	activity.save()

        return redirect('activity_list_qa')