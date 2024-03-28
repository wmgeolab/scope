# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core import serializers
from django.http import HttpResponse

from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from .serializers import (
    UserSerializer, 
    QuerySerializer, 
    ResultSerializer, 
    RunSerializer, 
    SourceSerializer, 
    WorkspaceSerializer, 
    WorkspaceMembersSerializer, 
    WorkspaceEntriesSerializer,
    TagSerializer
)
from .models import User, Query, Result, Source, Run, Workspace, WorkspaceMembers, WorkspaceEntries, Tag
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.core.paginator import Paginator

from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

import logging
logger = logging.getLogger(__name__)

#from newspaper import Article
#imports for text extraction from articles
import requests
from readability import Document
import regex
import json

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

    def get_queryset(self):
        logger.error(f"ResultView get_queryset call request: {self.request}")
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

    # def create(self, request):
    #     logger.error(f"RunView create run call request: {self.request}")
    #     serializer = self.get_serializer(data=request.data)
    #     print('Serealizer: ', serializer)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(user=self.request.user)
    #     # self.perform_create(serializer=serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     logger.error(f"QueryView create call user ID: {self.request.user.id}")
    #     print(self.get_object())
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        queryset = Run.objects.all()
        user = self.request.user.id
        if user:
            queryset = queryset.filter(user_id=user)
        return queryset

class SourceView(viewsets.ModelViewSet):
    logger.error("SourceView here!")
    permission_classes = [IsAuthenticated]
    serializer_class = SourceSerializer
    queryset = Source.objects.all()

    def get_queryset(self, query_id, page_id):
        runs = Run.objects.filter(query_id=query_id).values_list()
        print("RElevant runs: ", runs)
        print("Most recent run: ", Run.objects.filter(
            query_id=query_id).values('id')[len(runs)-1])
        run_id = Run.objects.filter(
            query_id=query_id).values('id')[len(runs)-1]['id']
        print(run_id)
        # now get all the relevant results linked to that run
        results = Result.objects.filter(run_id=run_id).values('id')
        results = results[0:len(results)-1]
        result_ids = []
        print("ID's for results: ", results)
        for result in results:
            result_ids.append(result['id'])
        source_ids = []
        for result_id in result_ids:
            source_ids.append(Result.objects.filter(
                id=result_id).values('source_id'))

        print("List of source IDs: ", source_ids)
        # WE NOW HAVE ALL OUR SOURCE ID'S RELATED TO THAT QUERY!!
        source_ids = source_ids[0:len(source_ids)-1]
        print(source_ids)
        source_ids_v2 = []
        for source_id in source_ids:
            source_ids_v2.append(source_id[0])
        print("Source IDs: ", source_ids_v2)
        source_id_list = []
        for src_id in source_ids_v2:
            source_id_list.append(src_id['source_id'])
        print("Source IDs: ", source_id_list)
        print("Count: ", Source.objects.count())
        # sources = Source.objects.all()
        # LOOP THROUGH EVERY SOURCE ID AND ADD IT TO ALL SOURCES RETURNED
        sources = Source.objects.filter(pk__in=source_id_list)
        print("sources", sources)
        p = Paginator(sources, 5)    #pagination
        print("p:", p.num_pages)



        data = serializers.serialize('json', p.get_page(page_id)) 
        # look into how this works and why pagination isn't applied
        return HttpResponse(data)
    
class CountView(viewsets.ModelViewSet):

    def get_count(self, query_id):
        runs = Run.objects.filter(query_id=query_id).values_list()
        print("Most recent run: ", Run.objects.filter(
            query_id=query_id).values('id')[len(runs)-1])
        run_id = Run.objects.filter(
            query_id=query_id).values('id')[len(runs)-1]['id']
        print(run_id)
        # now get all the relevant results linked to that run
        results = Result.objects.filter(run_id=run_id).values('id')
        results = results[0:len(results)-1]
        result_ids = []
        print("ID's for results: ", results)
        for result in results:
            result_ids.append(result['id'])
        source_ids = []
        for result_id in result_ids:
            source_ids.append(Result.objects.filter(
                id=result_id).values('source_id'))

        print("List of source IDs: ", source_ids)
        # WE NOW HAVE ALL OUR SOURCE ID'S RELATED TO THAT QUERY!!
        source_ids = source_ids[0:len(source_ids)-1]
        print(source_ids)
        source_ids_v2 = []
        for source_id in source_ids:
            source_ids_v2.append(source_id[0])
        print("Source IDs: ", source_ids_v2)
        source_id_list = []
        for src_id in source_ids_v2:
            source_id_list.append(src_id['source_id'])
        print("Source IDs: ", source_id_list)
        print("Final Count: ", len(source_id_list))
        count = len(source_id_list)

        return HttpResponse(count)
    
class ReadSource(viewsets.ModelViewSet):
    
    def get_queryset(self, source_id):
        # First, get the requested source from the db
        source = Source.objects.filter(id=source_id)
        print("Source: ", source[0].url)
        url = source[0].url
        response = requests.get(url)
        response.encoding = 'UTF-8'
        doc = Document(response.text)
        plain_text = doc.summary()
        plain_text = regex.sub('<[^<]+?>', '', plain_text)
        # article = Article(url)
        # article.download()
        # article.parse()
        #print(article.text)
        # plain_text = article.text
        # dictionary = '{ "text":"' + article.text + '"}'
        # result = json.loads(dictionary, strict=False)
        # print(result)
        return HttpResponse(plain_text)

class WorkspaceView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceSerializer

    # accessible at /api/workspaces/ [GET]
    def get_queryset(self):
        self.serializer_class = WorkspaceMembersSerializer
        queryset = WorkspaceMembers.objects.all()
        user = self.request.user.id
        # return all workspaces that user is part of
        return queryset.filter(member=user)

    # accessble at /api/workspaces/ [DELETE]
    # delete() is a built-in django method
    def delete(self, request):
        name = request.data['name']
        # custom responses to keep all error messages consistent
        # check if workspace exists
        try:
            workspace = Workspace.objects.get(name=name)
        except:
            return Response(data='Workspace does not exist', status=status.HTTP_404_NOT_FOUND)
        if not workspace:
            return Response(data='Workspace does not exist', status=status.HTTP_404_NOT_FOUND)
        # check password
        if workspace.password != request.data['password']:
            return Response(data='Incorrect password', status=status.HTTP_400_BAD_REQUEST)
        # check if creator
        if workspace.creatorId != self.request.user:
            return Response(data='Only the workspace creator can delete', status=status.HTTP_403_FORBIDDEN)
        workspace.delete()
        return Response(data='Workspace has been deleted', status=status.HTTP_200_OK)

    # accessible at /api/workspaces/ [POST]
    # create() is a built-in django method
    def create(self, request):
        # technically a duplicate check since name in models defined to be unique
        # returns response for consistent error message
        print(request.data, 'test ')
        if Workspace.objects.filter(name=request.data['name']):
            return Response(data='Workspace name already exists', status=status.HTTP_400_BAD_REQUEST)
        # create workspace and add creator to workspace
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creatorId=self.request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # accessible at /api/workspaces/join/ [POST]
    @action(detail=False, methods=['post'], url_path='join', url_name='join')
    def join_workspace(self, request):
        # check if workspace exists
        try:
            workspace = Workspace.objects.get(name=request.data['name'])
        except:
            return Response(data='Workspace does not exist', status=status.HTTP_404_NOT_FOUND)
        # check if password matches
        if workspace.password != request.data['password']:
            return Response(data='Incorrect password', status=status.HTTP_400_BAD_REQUEST)
        # check if user is already in the workspace
        if WorkspaceMembers.objects.filter(workspace=workspace, member=self.request.user):
            return Response(data='User already part of the workspace', status=status.HTTP_400_BAD_REQUEST)
        # add user to workspace
        self.request.data['workspace'] = workspace
        self.request.data['workspace_id'] = workspace.id
        serializer = WorkspaceMembersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(member=self.request.user, workspace=workspace)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

class WorkspaceMembersView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceMembersSerializer

    # accessible at /api/member/ [DELETE]
    def delete(self, request):
        user = self.request.user
        id = request.data['workspace']
        member = WorkspaceMembers.objects.get(member=user, workspace=workspace)
        # check if workspace exists
        try:
            workspace = Workspace.objects.get(id=id)
        except:
            return Response(data='Workspace does not exist', status=status.HTTP_404_NOT_FOUND)
         # check if creator - creator cannot leave their own workspace
        if workspace.creatorId == self.request.user:
            return Response(data='The creator cannot leave the workspace. Perhaps you want to delete the workspace?', status=status.HTTP_403_FORBIDDEN)
        member.delete()
        return Response(data='Member has been removed from the workspace.', status=status.HTTP_200_OK)
    
class WorkspaceEntriesView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceEntriesSerializer
    
    # accessible at /api/entries?workspace=(id) [GET]
    def get_queryset(self):
        # returns all sources(entries) in a workspace
        w_id = self.request.query_params.get('workspace')
        if w_id is not None:
            user_id = self.request.user.id
            workspace = Workspace.objects.filter(id=w_id).first()
            if not workspace:
                raise ValidationError(detail="Workspace does not exist.")
            in_workspace = True if WorkspaceMembers.objects.filter(member=user_id, workspace=w_id) else False
            if in_workspace:
                return WorkspaceEntries.objects.filter(workspace=workspace).all()
            else:
                raise ValidationError(detail="Not part of this workspace.")
        raise ValidationError(detail="No workspace ID provided.")
    
    # accessible at /api/entries/ [POST]
    def create(self, request):
        # returns response for consistent error message
        workspace = Workspace.objects.get(id=request.data['workspace'])
        source = Source.objects.get(id=request.data['source_id'])
        if not source:
            return Response(data='Source not found', status=status.HTTP_404_NOT_FOUND)
        if not workspace:
            return Response(data='Workspace not found', status=status.HTTP_404_NOT_FOUND)
        # check if source exists in workspace
        entry = WorkspaceEntries.objects.filter(source=request.data['source_id'], workspace=request.data['workspace'])
        if entry:
            return Response(data='Source already in workspace', status=status.HTTP_401_UNAUTHORIZED)
        # add source to workspace
        self.request.data['source'] = source
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(workspace=workspace, source=source)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # accessible at /api/entries/ [DELETE]
    def delete(self, request):
        workspace = Workspace.objects.get(id=request.data['workspace'])
        source = Source.objects.get(id=request.data['source'])
        # check if workspace exists
        if not workspace:
            return Response(data='Workspace does not exist', status=status.HTTP_404_NOT_FOUND)
        # check if source exists
        if not source:
            return Response(data='Source does not exist', status=status.HTTP_404_NOT_FOUND)
        # check if source in workspace
        entry = WorkspaceEntries.objects.filter(source=request.data['source'], workspace=request.data['workspace'])
        if not entry:
            return Response(data='Source is not in workspace', status=status.HTTP_404_NOT_FOUND)
        entry.delete()
        return Response(data='Source has been removed from the workspace.', status=status.HTTP_200_OK)

class TagView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer

    def create(self, request):
        workspace = request.data['workspace']
        tag = request.data['tag']
        # check if workspace exists
        if not workspace:
            return Response(data='Workspace does not exist', status=status.HTTP_404_NOT_FOUND)
        workspace = Workspace.objects.get(id=workspace)
        # check if tag already exists
        if Tag.objects.filter(workspace=workspace, tag=tag):
            return Response(data='Tag already exists', status=status.HTTP_400_BAD_REQUEST)
        # add tag
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(workspace=workspace)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def delete(self, request):
        workspace = request.data['workspace']
        tag = request.data['tag']
        # check if workspace exists
        if not workspace:
            return Response(data='Workspace does not exist', status=status.HTTP_404_NOT_FOUND)
        # check if tag exists
        if not Tag.objects.filter(workspace=workspace, tag=tag):
            return Response(data='Tag does not exist', status=status.HTTP_404_NOT_FOUND)
        # delete tag
        tag.delete()
        return Response(data='Tag has been removed from the workspace.', status=status.HTTP_200_OK)

# accessible at /api/test/ [GET]
class TestView(viewsets.ModelViewSet):

    def get_queryset(self):
        return Response(data="Test view reached!", status=status.HTTP_200_OK)
