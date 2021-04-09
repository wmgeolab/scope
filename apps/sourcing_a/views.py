from django.shortcuts import render
from django.apps import apps

from django.core.files.storage import FileSystemStorage

import os

from domain.models import SourceCode
from .models import Source
from .forms import AutoImportForm
# Create your views here.

def home(request):
    return render(request, 'templates/sourcing_a/home.html')

def auto_import(request):
    form = AutoImportForm()
    if request.method == 'GET':
        return render(request, 'templates/sourcing_a/auto_import.html', {'form':form})

    if request.method == 'POST':
        form = AutoImportForm(request.POST)
        if form.is_valid():

            context = {
            "forms": form
            }

            #conn = pymysql.connect(host="mysql.scopedata.org", user="scopesql",
                                 #password="fY7Ukl52UI", db="scopesourcedata")

            #curs = conn.cursor()

            #keyword = form.cleaned_data["primary_keyword"]

            #sql = "SELECT source_text FROM `SourceType1` WHERE source_text LIKE '%keyword%';"

            #df = pd.read_sql(sql,conn)

    return render(request, "templates/sourcing_a/home.html", context)
