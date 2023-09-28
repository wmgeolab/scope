# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core import serializers
from django.http import HttpResponse

from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from .serializers import UserSerializer, QuerySerializer, ResultSerializer, RunSerializer, SourceSerializer, WorkspaceSerializer
from .models import User, Query, Result, Source, Run, Workspace, WorkspaceMembers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
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
    queryset = Workspace.objects.all()

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

    def get_queryset(self):
        queryset = Workspace.objects.all()
        return queryset

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

    # @action(detail=True, methods=['post'])
    # should be accessible at /api/workspaces/join/ [POST]
    @action(detail=False, methods=['post'], url_path=r'join')
    def join_workspace(self, request):
        password = request.data.get('password')
        workspaceID = request.data.get('id')
        user_id = request.user.id
        # check if workspace exists
        workspace = Workspace.objects.filter(id=workspaceID).first()
        
        member = WorkspaceMembers.objects.filter(workspace_id=workspace.id)
        if member:
            return Response({'error': 'You are already a member of this workspace'}, status=status.HTTP_400_BAD_REQUEST)
        # check if password is correct, if so add user to workspace
        if workspace.password == password:
            
            WorkspaceMembers.objects.create(id=user_id, workspace_id=workspace.id)
            serializer = WorkspaceSerializer(workspace)
            return Response(serializer.data)
        else:
            return Response({'error': 'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)
