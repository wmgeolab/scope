from django.shortcuts import render, redirect
from django.apps import apps

from .forms import UserForm

# Create your views here.

def profile(request):
    form = UserForm(instance=request.user)
    return render(request, 'templates/reqUsers/profile.html', {'form':form})
