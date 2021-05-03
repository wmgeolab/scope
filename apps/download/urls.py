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
    re_path('^$', views.home, name='download'),
    # source
    re_path('^select$', views.select, name='select'),
    re_path('^download/sources$', views.download_sources, name='download_sources'),
    re_path('^download/extracts$', views.download_extracts, name='download_extracts'),
    re_path('^download/activities$', views.download_activities, name='download_activities'),
]
