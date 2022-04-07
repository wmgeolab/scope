# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserSerializer, QuerySerializer
from .models import User, Query
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

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
    permission_classes = [IsAuthenticated]
    serializer_class = QuerySerializer
    queryset = Query.objects.all()
    def create(self, request):
        print(self.request.headers)
        print(self.request.user)
        # q = self.get_object()
        return Response({'status': 'post received'})

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
