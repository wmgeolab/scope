# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core import serializers
from django.http import HttpResponse

from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserSerializer, QuerySerializer, ResultSerializer, RunSerializer, SourceSerializer
from .models import User, Query, Result, Source, Run
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


# try running the algorithm in views:

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
        p = Paginator(sources, 3)    #pagination
        print("p:", p.num_pages)



        data = serializers.serialize('json', p.get_page(page_id)) 
        # look into how this works and why pagination isn't applied
        return HttpResponse(data)
