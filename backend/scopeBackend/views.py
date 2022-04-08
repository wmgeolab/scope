# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserSerializer, QuerySerializer
from .models import User, Query
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

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


    # def create(self, request):
    #     request.data['user'] = str(request.user)
    #     return super().create(request)
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        # self.perform_create(serializer=serializer)
        headers = self.get_success_headers(serializer.data)
        print(self.request.user.id)
        # q = self.get_object()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # return Response({'status': 'post received'})



class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = "http://localhost:3000/login"
    client_class = OAuth2Client
    
class ResultView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ResultSerializer
    queryset = Result.objects.all()

class SourceView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SourceSerializer
    queryset = Source.objects.all()
