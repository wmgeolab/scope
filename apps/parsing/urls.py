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
    # parsing data table
    re_path('^$', views.home, name='parsing'),
    re_path('^landing$', views.landing, name='landing'),
    # actorcodes
    re_path('^actorcode/add$', views.actorcode_add, name='actorcode_add'),
    re_path('^actorcode/(?P<pk>[\w]+)/view$', views.actorcode_view, name='actorcode_view'),
    # activitycodes
    re_path('^activitycode/add$', views.activitycode_add, name='activitycode_add'),
    re_path('^activitycode/(?P<pk>[\w]+)/view$', views.activitycode_view, name='activitycode_view'),
    # statuscodes
    re_path('^statuscode/add$', views.statuscode_add, name='statuscode_add'),
    re_path('^statuscode/(?P<pk>[\w]+)/view$', views.statuscode_view, name='statuscode_view'),
    # activities
    re_path('^activity/add$', views.activity_add, name='activity_add'),
    re_path('^activity/(?P<pk>[\w]+)/view$', views.activity_view, name='activity_view'),
    re_path('^activity/(?P<name>[\w]+)/checkout', views.activity_checkout, name='activity_checkout'),
    re_path('^activity/(?P<name>[\w]+)/release', views.activity_release, name='activity_release'),
    re_path('^activity/list$', views.activity_list, name='activity_list'),
    re_path('^activity/(?P<name>[\w]+)/edit$', views.activity_edit, name='activity_edit'),
]