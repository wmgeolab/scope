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
    re_path('^settings$', views.settings, name='sourcing_settings'),
    # generic datamodel
    re_path('^datamodel/(?P<name>[\w]+)/$', views.datamodel, name='sourcing_datamodel'),
    re_path('^datamodel/(?P<name>[\w]+)/add$', views.datamodel_add, name='sourcing_datamodel_add'),
    re_path('^datamodel/(?P<name>[\w]+)/view(?P<pk>[\w]+)/$', views.datamodel_view, name='sourcing_datamodel_view'),
    re_path('^import_from_data_folder$', views.import_from_data_folder, name='sourcing_import_from_data_folder'),
    # source
    re_path('^source/add$', views.source_add, name='source_add'),
    re_path('^source/(?P<pk>[\w]+)/view$', views.source_view, name='source_view'),
]
