# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserSerializer, QuerySerializer, ResultSerializer, RunSerializer, SourceSerializer
from .models import User, Query, Result, Source, Run
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

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
            queryset = queryset.filter(user_id=user)
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
    #queryset = Result.objects.all()

    # @api_view(['GET'])
    # @permission_classes([IsAuthenticated])

    def get_queryset(self):
        print(self.request)
    #     serializer = self.get_serializer(data = self.request.data)
    #     serializer.is_valid(raise_exception = True)
        queryset = Result.objects.all()
        user = self.request.user.id
        if user:
            queryset = Result.objects.filter(run__query__user=user)
        return queryset

    # make a separate method to return based on username
    def get_queryset_based_on_user(user_id):
        queryset = Query.objects.all()
        queryset = queryset.filter(user_id=user_id)
        return queryset


class RunView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RunSerializer
    queryset = Run.objects.all()


class SourceView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SourceSerializer
    queryset = Source.objects.all()
