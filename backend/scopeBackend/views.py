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
    TagSerializer,
    AiResponseSerializer,
    RevisionSerializer,
    WorkspaceQuestionsSerializer
)
from .models import User, Query, Result, Source, Run, Workspace, WorkspaceMembers, WorkspaceEntries, Tag,  AiResponse, Revision, WorkspaceQuestions
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
import os

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
    callback_url = os.getenv('GITHUB_CALLBACK_URL', 'http://localhost:3000/login')
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
        runs = Run.objects.filter(query_id=query_id)
        for run in reversed(runs):
            if len(Result.objects.filter(run_id=run.id)) != 0:
                run_id = run.id
                break

        print(run_id)
        # now get all the relevant results linked to that run
        results = Result.objects.filter(run_id=run_id).values('id')
        result_ids = []
        print("ID's for results: ", results, len(results))
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
        # return all workspaces that user is part of and are not hidden
        return queryset.filter(member=user)

    # accessble at /api/workspaces/ [DELETE]
    # delete() is a built-in django method
    def delete(self, request):
        name = request.data['name']
        workspace = Workspace.objects.get(name=name)
        # custom responses to keep all error messages consistent
        # check if workspace exists
        if not workspace:
            return Response({'error':'Workspace does not exist'}, status=status.HTTP_404_NOT_FOUND)
        # check password
        if workspace.password != request.data['password']:
            return Response({'error':'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)
        # check if creator
        if workspace.creatorId != self.request.user:
            return Response({'error':'Only the workspace creator can delete'}, status=status.HTTP_403_FORBIDDEN)
        # workspace.delete()
        workspace.hidden = True
        workspace.name = workspace.name + "_deleted_" + __import__('os').urandom(15).hex()
        workspace.save()
        return Response('Workspace has been deleted', status=status.HTTP_200_OK)

    # accessible at /api/workspaces/ [POST]
    # create() is a built-in django method
    def create(self, request):
        # technically a duplicate check since name in models defined to be unique
        # returns response for consistent error message
        print(request.data, 'test ')
        if Workspace.objects.filter(name=request.data['name']):
            return Response({'error':'Workspace name already exists'}, status=status.HTTP_400_BAD_REQUEST)
        # create workspace and add creator to workspace
        serializer = self.get_serializer(data=request.data)

        if any(c in request.data['name'] for c in ['/', '\\', '"']):
            return Response({'error':'Name contains illegal characters'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        workspace = serializer.save(creatorId=self.request.user)
        headers = self.get_success_headers(serializer.data)

        # Create 4 default WorkspaceQuestions
        default_questions = [
            {'question': 'No question set', 'workspace_id': workspace},
            {'question': 'No question set', 'workspace_id': workspace},
            {'question': 'No question set', 'workspace_id': workspace},
            {'question': 'No question set', 'workspace_id': workspace}
        ]
        
        # Save default questions to the database
        for question_data in default_questions:
            WorkspaceQuestions.objects.create(**question_data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # accessible at /api/workspaces/join/ [POST]
    @action(detail=False, methods=['post'], url_path='join', url_name='join')
    def join_workspace(self, request):
        # check if workspace exists
        workspace = Workspace.objects.get(name=request.data['name'])
        if not workspace:
            return Response({'error':'Workspace does not exist'}, status=status.HTTP_404_NOT_FOUND)
        # check if password matches
        if workspace.password != request.data['password']:
            return Response({'error':'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)
        # check if user is already in the workspace
        if WorkspaceMembers.objects.filter(workspace=workspace, member=self.request.user):
            return Response({'error':'User already part of the workspace'}, status=status.HTTP_400_BAD_REQUEST)
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
        workspace = Workspace.objects.get(id=id)
        member = WorkspaceMembers.objects.get(member=user, workspace=workspace)
        # check if workspace exists
        if not workspace:
            return Response({'error':'Workspace does not exist'}, status=status.HTTP_404_NOT_FOUND)
         # check if creator - creator cannot leave their own workspace
        if workspace.creatorId == self.request.user:
            return Response({'error':'The creator cannot leave the workspace. Perhaps you want to delete the workspace?'}, status=status.HTTP_403_FORBIDDEN)
        member.delete()
        return Response('Member has been removed from the workspace.', status=status.HTTP_200_OK)
    
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
            return Response({'error':'Source not found'}, status=status.HTTP_404_NOT_FOUND)
        if not workspace:
            return Response({'error':'Workspace not found'}, status=status.HTTP_404_NOT_FOUND)
        # check if source exists in workspace
        entry = WorkspaceEntries.objects.filter(source=request.data['source_id'], workspace=request.data['workspace'])
        if entry:
            return Response({'error':'Source already in workspace'}, status=status.HTTP_401_UNAUTHORIZED)
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
            return Response({'error':'Workspace does not exist'}, status=status.HTTP_404_NOT_FOUND)
        # check if source exists
        if not source:
            return Response({'error':'Source does not exist'}, status=status.HTTP_404_NOT_FOUND)
        # check if source in workspace
        entry = WorkspaceEntries.objects.filter(source=request.data['source'], workspace=request.data['workspace'])
        if not entry:
            return Response({'error':'Source is not in workspace'}, status=status.HTTP_404_NOT_FOUND)
        entry.delete()
        return Response('Source has been removed from the workspace.', status=status.HTTP_200_OK)

class WorkspaceQuestionsView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceQuestionsSerializer

    # accessible at /api/questions?workspace=(id) [GET]
    def get_queryset(self):
        # returns all questions and their responses for a workspace
        w_id = self.request.query_params.get('workspace')
        #print("Workspace ID: ", w_id)
        if w_id is not None:
            user_id = self.request.user.id
            #workspace = Workspace.objects.filter(id=w_id).first()
            # if not workspace:
            #     raise ValidationError(detail="Workspace does not exist.")
            in_workspace = True if WorkspaceMembers.objects.filter(member=user_id, workspace=w_id) else False
            if in_workspace:
                #return WorkspaceEntries.objects.filter(workspace=workspace).all()
                return WorkspaceQuestions.objects.filter(workspace_id=w_id).all()
            else:
                raise ValidationError(detail="Not part of this workspace.")
        raise ValidationError(detail="No workspace ID provided.")
    
    # accessible at /api/questions/ [PUT]
    def create(self, request):
        # store the workspace_id from the request
        w_id = request.data['workspace']
        q_id = request.data['id']
        print("Raw request: ", request.data)
        print("Workspace ID is: ", w_id)
        print("Question ID is: ", q_id)
        # returns response for consistent error message
        workspace = Workspace.objects.get(id=request.data['workspace'])
        if not workspace:
            return Response({'error':'Workspace not found'}, status=status.HTTP_404_NOT_FOUND)
        # check if question exists in workspace
        #question = WorkspaceQuestions.objects.filter(question=request.data['question'], workspace_id=request.data['workspace'])
        # question = request.data['question']
        # print("Question is: ", question)
        # question, created = WorkspaceQuestions.objects.update_or_create(
        #     question=question,
        #     workspace_id=workspace
        # )

        try:
            # Fetch the question by its ID and workspace_id from the request body
            question = WorkspaceQuestions.objects.get(id=q_id, workspace_id=w_id)
        except WorkspaceQuestions.DoesNotExist:
            return Response(
                {'error': 'Question not found or does not belong to the workspace'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        question.question = request.data['question']
        question.save()

        # SEND REQUEST FOR AI RESPONSE TO ML ROUTE

        # if question:
        #     return Response({'error':'Question already in workspace'}, status=status.HTTP_401_UNAUTHORIZED)
        # add question to workspace
        # self.request.data['source'] = question
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save(question=question, workspace_id=w_id)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # Serialize and return the response
        serializer = self.get_serializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    

class TagView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer

    def create(self, request):
        workspace = request.data['workspace']
        tag = request.data['tag']
        # check if workspace exists
        if not workspace:
            return Response({'error':'Workspace does not exist'}, status=status.HTTP_404_NOT_FOUND)
        workspace = Workspace.objects.get(id=workspace)
        # check if tag already exists
        if Tag.objects.filter(workspace=workspace, tag=tag):
            return Response({'error':'Tag already exists'}, status=status.HTTP_400_BAD_REQUEST)
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
            return Response({'error':'Workspace does not exist'}, status=status.HTTP_404_NOT_FOUND)
        # check if tag exists
        tag = Tag.objects.filter(workspace=workspace, tag=tag)
        if not tag:
            return Response({'error':'Tag does not exist'}, status=status.HTTP_404_NOT_FOUND)
        # delete tag
        tag.delete()
        return Response('Tag has been removed from the workspace.', status=status.HTTP_200_OK)
    
    # accessible at /api/tags/ [GET]
    # We want to pass in a user ID and return the tags for all the workspaces that the user is part of
    # Optional parameter:
    # - workspace
    def get_queryset(self):
        user = self.request.user.id
        queryset = Tag.objects.all()
        if user:
            # Tags only contain a workspace ID and tag text, so we need to check 
            # in the workspaces that the user is part of
            workspaces = WorkspaceMembers.objects.filter(member=user).values_list('workspace', flat=True)

            workspace_parameter = self.request.query_params.get('workspace')

            if workspace_parameter:
                # workspaces = union of workspaces that the user is part of and the workspace parameter
                #workspaces = workspaces | Workspace.objects.filter(id=workspace_parameter)
                queryset = queryset.filter(workspace_id=workspace_parameter, workspace_id__in=workspaces)

            # Now we need to filter tags by the workspaces that the user is part of
            #queryset = queryset.filter(workspace_id__in=workspaces).order_by('workspace')
            queryset = queryset.filter(workspace_id__in=workspaces)

            queryset = queryset.order_by('workspace')
    
        return queryset

# accessible at /api/test/ [GET]
class TestView(viewsets.ModelViewSet):

    def get_queryset(self):
        return Response({"success":"Test view reached!"}, status=status.HTTP_200_OK)
        
class AiResponseView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AiResponseSerializer
    
    # Pass in a workspace_id and receive an airesponse
    # accessible at /api/ai_responses/ [GET]
    def get_queryset(self):
        w_id = self.request.query_params.get('workspace')
        return AiResponse.objects.filter(workspace=w_id)
    
    # accessible at /api/ai_responses/ [POST]
    def create(self, request):
        source = request.data['source']
        summary = request.data['summary']
        entities = request.data['entities']
        locations = request.data['locations']
        workspace = request.data['workspace']
        # Check if source ID exists
        if not Source.objects.filter(id=source):
            return Response({'error':'Source does not exist'}, status=status.HTTP_404_NOT_FOUND)
        # Check if workspace exists
        if not Workspace.objects.filter(id=workspace):
            return Response({'error':'Workspace does not exist'}, status=status.HTTP_404_NOT_FOUND)
        # Check if summary exists
        if not summary:
            return Response({'error':'Summary cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
        # # Check if entities exist
        # if not entities:
        #     return Response({'error':'Entities cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
        # # Check if locations exist
        # if not locations:
        #     return Response({'error':'Locations cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
        # Create airesponse
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(source=source)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Update an existing AI response
    def update(self, request, *args, **kwargs):
        ai_response_id = kwargs.get('pk')  # Get ID from URL
        try:
            ai_response = AiResponse.objects.get(id=ai_response_id)
        except AiResponse.DoesNotExist:
            return Response({'error': 'AiResponse not found'}, status=status.HTTP_404_NOT_FOUND)

        # Use serializer to update the instance
        serializer = self.get_serializer(ai_response, data=request.data, partial=False)  # Full update with PUT
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)

# accessible at /api/revision/ [GET]
class RevisionView(viewsets.ModelViewSet):
    # Pass in a source and workspace ID and get the most recent revision
    permission_classes = [IsAuthenticated]
    serializer_class = RevisionSerializer


    # accessible at /api/revision/ [GET]
    def get_queryset(self):
        source = self.request.query_params.get('source')
        workspace = self.request.query_params.get('workspace')
        if not source or not workspace:
            return Response({'error': 'Source or workspace not specified.'}, status=status.HTTP_400_BAD_REQUEST)
        # We want to filter by Revisions whose original_response field, a foreign key to AiResponse, 
        # has a source field that points to a Source with the id that was passed in

        # First, retrieve the first AiResponse where the source is the one passed in
        ai_response_for_source = AiResponse.objects.filter(source=source).first()

        # Second, retrieve the first Revision where the original_response is the one from the first step
        revisions_of_original_response = Revision.objects.filter(original_response=ai_response_for_source)

        return revisions_of_original_response.order_by('-datetime')
            
    # accessible at /api/revision/ [POST]
    def create(self, request):
        source = request.data['source']
        workspace = request.data['workspace']
        summary = request.data['summary']
        entities = request.data['entities']
        locations = request.data['locations']

        # Test if workspace exists
        if not Workspace.objects.filter(id=workspace):
            return Response({'error': 'Workspace does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Test if user is part of workspace
        if not WorkspaceMembers.objects.filter(member=self.request.user, workspace=workspace):
            return Response({'error': 'User is not part of the workspace.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Test if source exists
        if not Source.objects.filter(id=source):
            return Response({'error': 'Source does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Test if summary exists
        if not summary:
            return Response({'error': 'Summary cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

        # Test if entities exist
        if not entities:
            return Response({'error': 'Entities cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

        # Test if locations exist
        if not locations:
            return Response({'error': 'Locations cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve original AiResponse
        try:
            original_response = AiResponse.objects.get(source=source)
        except AiResponse.DoesNotExist:
            return Response({'error': 'Original AiResponse does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Create revision
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(workspace=workspace, original_response=original_response)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)