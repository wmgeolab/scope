"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# url is deprecreated for Django 4+
# from django.conf.urls import url

from django.urls import path, include, re_path
from django.contrib import admin
from rest_framework import routers
from scopeBackend import views

router = routers.DefaultRouter()
router.register(r'scope', views.UserView, 'User')
router.register(r'queries', views.QueryView, 'Queries')
router.register(r'run', views.RunView, 'Run')
router.register(r'results', views.ResultView, 'Results')
router.register(r'sources', views.SourceView, 'Sources')

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('dj-rest-auth/github', views.GithubLogin.as_view(), name='github_login'),
    # testing out passing in specific queries:
    path('api/results/9',
         views.ResultView.get_queryset_based_on_user, name='Results')
]
