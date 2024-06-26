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
    re_path('^$', views.home, name='parsing_qa'),
    re_path('^activity/(?P<pk>[\w]+)/qa', views.activity_qa, name='activity_qa'),
    re_path('^activity/(?P<pk>[\w]+)/release', views.activity_release_qa, name='activity_release_qa'),
    re_path('^activity/(?P<pk>[\w]+)/assess', views.activity_assess, name='activity_assess'),
    re_path('^activity/list$', views.activity_list_qa, name='activity_list_qa'),
    re_path('^activity/listcomplete$', views.activity_list_complete, name='activity_list_complete'),
]
