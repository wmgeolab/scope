# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserSerializer, QuerySerializer
from .models import User, Query

from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from .serializers import SourceSerializer, UserSerializer, QuerySerializer, ResultSerializer
from .models import User, Query, Result, Source
# from backend.scopeBackend import serializers

# Create your views here.

class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class QueryView(viewsets.ModelViewSet):
    serializer_class = QuerySerializer
    queryset = Query.objects.all()

class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = "http://localhost:3000/login"
    client_class = OAuth2Client
    
class ResultView(viewsets.ModelViewSet):
    serializer_class = ResultSerializer
    queryset = Result.objects.all()

class SourceView(viewsets.ModelViewSet):
    serializer_class = SourceSerializer
    queryset = Source.objects.all()
