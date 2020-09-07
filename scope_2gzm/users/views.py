from django.shortcuts import render
from .forms import UserForm

# Create your views here.
def login(request):
	if request.method == "GET":
		form = UserForm()
		return render(request, 'templates/users/login.html', {"form":form})
	if request.method == "POST":
		return