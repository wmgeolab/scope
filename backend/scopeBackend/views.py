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
from .models import User, Query, Result, Source, Run
# from backend.scopeBackend import serializers

# Create your views here.

class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class QueryView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = QuerySerializer

    #queryset = Query.objects.all()
    def get_queryset(self):
        queryset = Query.objects.all()
        user = self.request.user.id
        if user:
            queryset = queryset.filter(user_id = user)
        return queryset

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
    # queryset = Result.objects.all()
    
    #@api_view(['GET'])
    #@permission_classes([IsAuthenticated])
    
    # def get_queryset(self):
    #     serializer = self.get_serializer(data = self.request.data)
    #     serializer.is_valid(raise_exception = True)
    #     queryset = Result.objects.all()
    #     user = self.request.user.id
    #     queries = Query.objects.filter(user_id = user)
    #     runs = []
    #     for query in queries:
    #         run = Run.objects.filter(query_id = query.id)
    #         #print(run.id)
    #     #for run in runs:
    #         #result = 
    #     #run = Run.objects.filter(query_id = query).order_by('-time')
    #     #results = Result.objects.filter(run_id = run)
    #     return Response(serializer.data) #queries
    

class SourceView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SourceSerializer
    queryset = Source.objects.all()
