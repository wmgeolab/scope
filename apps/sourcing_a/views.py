from django.shortcuts import render
from django.apps import apps

from django.core.files.storage import FileSystemStorage

import os

from domain.models import SourceCode
from .models import Source
# Create your views here.

def home(request):
    return render(request, 'templates/sourcing_a/home.html')

#def auto_import(request, pk):
    #if request.method == 'GET':
        #return render(request, 'templates/sourcing_a/source_add.html', {'form':form})

    #form = AutoImportForm()
    #if request.method == 'POST':
        #form = AutoImportForm(request.POST)
        #if form.is_valid():

            #conn = pymysql.connect(host="mysql.scopedata.org", user="scopesql",
                                 #password="fY7Ukl52UI", db="scopesourcedata")

            #curs = conn.cursor()
