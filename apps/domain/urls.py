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
    re_path('^$', views.home, name='domain'),
    # domain
    re_path('^overview$', views.overview, name='overview'),
    re_path('^edit/domain$', views.edit_domain, name='edit_domain'),
    re_path('^edit/activitycodes$', views.edit_activitycodes, name='edit_activitycodes'),
    re_path('^edit/actorcodes$', views.edit_actorcodes, name='edit_actorcodes'),
    re_path('^edit/statuscodes$', views.edit_statuscodes, name='edit_statuscodes'),
    re_path('^edit/sourcecodes$', views.edit_sourcecodes, name='edit_sourcecodes'),
    re_path('^edit/triggerwords$', views.edit_triggerwords, name='edit_triggerwords'),
]
