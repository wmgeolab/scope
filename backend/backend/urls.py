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
router.register(r'count', views.CountView, 'Count')
router.register(r'text', views.ReadSource, 'Text')
router.register(r'workspaces', views.WorkspaceView, 'Workspaces')

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    # testing out passing in specific queries:
    path('api/sources/<int:query_id>/<int:page_id>/',
         views.SourceView.get_queryset, name='Sources'),
    path('api/count/<int:query_id>/', views.CountView.get_count, name='Count'),
    path('api/text/<int:source_id>/', views.ReadSource.get_queryset, name='Text'),
    path('api/', include(router.urls)),
    path('dj-rest-auth/github', views.GithubLogin.as_view(), name='github_login'),

]
