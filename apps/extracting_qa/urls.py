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
    re_path('^$', views.home, name='extracting_qa'),
    re_path('^extract/(?P<pk>[\w]+)/qa', views.extract_qa, name='extract_qa'),
    re_path('^extract/(?P<pk>[\w]+)/release', views.extract_release_qa, name='extract_release_qa'),
    re_path('^extract/(?P<pk>[\w]+)/assess', views.extract_assess, name='extract_assess'),
    re_path('^extract/list$', views.extract_list_qa, name='extract_list_qa'),
]
