"""scope_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path, include

from . import views

urlpatterns = [
    re_path('^$', views.home, name='sourcing'),
    # source
    re_path('^source/add$', views.source_add, name='source_add'),
    re_path('^source/import$', views.source_import, name='source_import'),
    re_path('^source/test_import$', views.source_import_test, name='source_import_test'),
    re_path('^source/(?P<pk>[\w]+)/view$', views.source_view, name='source_view'),
]
