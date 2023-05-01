# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from .serializers import UserSerializer, QuerySerializer, ResultSerializer, RunSerializer, SourceSerializer, WorkspaceSerializer
from .models import User, Query, Result, Source, Run, Workspace, WorkspaceMembers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView


import logging
logger = logging.getLogger(__name__)

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
        logger.error(f"QueryView create call user ID: {self.request.user.id}")
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
    logger.error("ResultView here!")

    def get_queryset(self):
        logger.error(f"ResultView get_queryset call request: {self.request}")
    #     serializer = self.get_serializer(data = self.request.data)
    #     serializer.is_valid(raise_exception = True)
        queryset = Result.objects.all()
        user = self.request.user.id
        if user:
            queryset = Result.objects.filter(run__query__user=user)
        return queryset


class RunView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RunSerializer
    queryset = Workspace.objects.all()


class SourceView(viewsets.ModelViewSet):
    logger.error("SourceView here!")
    permission_classes = [IsAuthenticated]
    serializer_class = SourceSerializer
    queryset = Source.objects.all()

class WorkspaceView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceSerializer

    def get_queryset(self):
        return Workspace.objects.filter(user=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        workspace = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(workspace)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add(self, request, pk=None):
        workspace = get_object_or_404(self.get_queryset(), pk=pk)
        result_ids = request.data.get('result_ids')
        if not result_ids:
            return Response({'error': 'result_ids field is required'}, status=status.HTTP_400_BAD_REQUEST)
        results = Result.objects.filter(pk__in=result_ids)
        workspace.results.add(*results)
        serializer = self.get_serializer(workspace)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def remove(self, request, pk=None):
        workspace = get_object_or_404(self.get_queryset(), pk=pk)
        result_ids = request.data.get('result_ids')
        if not result_ids:
            return Response({'error': 'result_ids field is required'}, status=status.HTTP_400_BAD_REQUEST)
        results = Result.objects.filter(pk__in=result_ids)
        workspace.results.remove(*results)
        serializer = self.get_serializer(workspace)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='create', url_name='create_workspace')
    def create_workspace(self, request):
        name = request.data.get('name')
        password = request.data.get('password')
        tags = request.data.get('tags')
        user = request.user

        # Check if name and password are not empty
        if not name or not password:
            return Response({'error': 'Name and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create workspace
        workspace = Workspace.objects.create(name=name, password=password, creatorId=user.id, tags=tags)

        # Add current user to the workspace as a member
        WorkspaceMembers.objects.create(user=user, workspace=workspace)

        serializer = WorkspaceSerializer(workspace)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        # Check if workspace exists
        workspace = get_object_or_404(self.get_queryset(), pk=pk)
        # Check if user is already a member of the workspace
        member = WorkspaceMembers.objects.filter(user=request.user, workspace=workspace)
        if member:
            return Response({'error': 'User is already a member of this workspace'}, status=status.HTTP_400_BAD_REQUEST)
        # Check that the user submitted a password
        if not workspace.password == request.data.get('password'):
            return Response({'error': 'Password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        # Add user to workspace
        WorkspaceMembers.objects.create(user=request.user, workspace=workspace)
        serializer = WorkspaceSerializer(workspace)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
