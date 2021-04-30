"""scope_2gzm URL Configuration

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
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),
    path('', views.home, name='home'),
    path('domain/', include('domain.urls')),
    path('download/', include('download.urls')),
    #path('GDELT_a/', include('GDELT_a.urls')),
    path('sourcing_m/', include('sourcing_m.urls')),
    path('sourcing_a/', include('sourcing_a.urls')),
    path('extracting_m/', include('extracting_m.urls')),
    path('extracting_qa/', include('extracting_qa.urls')),
    path('parsing_m/', include('parsing_m.urls')),
    path('parsing_qa/', include('parsing_qa.urls')),
]
