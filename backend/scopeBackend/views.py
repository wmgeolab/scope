# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core import serializers
from django.http import HttpResponse

from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserSerializer, QuerySerializer, ResultSerializer, RunSerializer, SourceSerializer
from .models import User, Query, Result, Source, Run, KeyWord
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.core.paginator import Paginator

from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

import requests
from readability import Document


import logging
logger = logging.getLogger(__name__)

#from newspaper import Article
#imports for text extraction from articles
import requests
from readability import Document
import regex

import json
import re
import ast

#import custom rank function
def rank(primary_kw, secondary_kws, queryset):
    # 1. Reorder sources based on how many keywords were matched
    #   - the primary keyword match is most important so reorder on that basis first
    #   - then for every source, reorder based on how many secondary keywords were matched
    #   - return the final reordered set
    # 2. Reorder sources based on the highest count for every keyword
    #   - again priority is given to primary keyword so reorder first based on the amount
    #       of times the primary keyword appears in a given source
    #   - then for every source, store the counts for each secondary kw in a dictionary
    #       and reorder based on the cumulative counts
    #   - return the final reordered set

    #define regex patterns
    CLEANR = re.compile('<.*?>')

    def get_text(url):
        print("URL: ", url)
        body = get_body(url)
        body = re.sub(CLEANR, '', body).strip()
        body.replace("\n", "")
        return body
    
    article_bodies = []
    for query in queryset:
        article_bodies.append([query['id'], query['text'], query['url'], get_text(query['url'])])
            

    
    #print("Article Bodies: ", article_bodies[0])


    def prim(string):
        return string.upper().count(primary_kw.upper())

    def sec(string):
        return sum([
            string.upper().count(secondary.upper())
            for secondary in secondary_kws
        ])

    sorted_list = [{'id':query[0], 'text':query[1],'url':query[2], 'body':query[3], 'primary':prim(query[3]), 'secondary':sec(query[3])} for query in article_bodies]
    # print("LIST BEFORE SORTING: ")
    # for i in range(len(sorted_list)):
    #     print(sorted_list[i])
    sorted_list.sort(key=lambda a: -a['secondary'])
    sorted_list.sort(key=lambda a: -a['primary'])
    # print("SORTED LIST: ")
    # for i in range(len(sorted_list)):
    #     print(sorted_list[i])
    #     print('----------------------------------------------------------------------------------')
    #     print('\n')
    return sorted_list

# method to get body of an article:
def get_body(url):
    response = requests.get(url)
    doc = Document(response.text)
    return doc.summary()
    # article = Article(url)
    # article.download()
    # article.parse()
    # #print(article.text)
    # plain_text = article.text
    # # dictionary = '{ "text":"' + article.text + '"}'
    # # result = json.loads(dictionary, strict=False)
    # # print(result)
    # return HttpResponse(plain_text)

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
        # First, we need to store the keywords related to each query_id
        keywords = KeyWord.objects.filter(query_id=query_id).values('word')
        #print("KEYORDS: ", keywords)
        p_kw = keywords[0]['word']
        #print("Primary Keyword: ", p_kw)
        sec_kw = keywords[1]['word']
        #print("Secondary Keywords: ", sec_kw)
        # this finishes the storing of primary and secondary keywords as string variables
        runs = Run.objects.filter(query_id=query_id).values_list()
        #print("RElevant runs: ", runs)
        #print("Most recent run: ", Run.objects.filter(
        #    query_id=query_id).values('id')[len(runs)-1])
        run_id = Run.objects.filter(
            query_id=query_id).values('id')[len(runs)-1]['id']
        #print(run_id)
        # now get all the relevant results linked to that run
        results = Result.objects.filter(run_id=run_id).values('id')
        results = results[0:len(results)-1]
        result_ids = []
        #print("ID's for results: ", results)
        for result in results:
            result_ids.append(result['id'])
        source_ids = []
        for result_id in result_ids:
            source_ids.append(Result.objects.filter(
                id=result_id).values('source_id'))

        #print("List of source IDs: ", source_ids)
        # WE NOW HAVE ALL OUR SOURCE ID'S RELATED TO THAT QUERY!!
        source_ids = source_ids[0:len(source_ids)-1]
        #print(source_ids)
        source_ids_v2 = []
        for source_id in source_ids:
            source_ids_v2.append(source_id[0])
        #print("Source IDs V2: ", source_ids_v2)
        source_id_list = []
        for src_id in source_ids_v2:
            source_id_list.append(src_id['source_id'])
        #print("Source IDs: ", source_id_list)
        #print("Count: ", Source.objects.count())
        # sources = Source.objects.all()
        # LOOP THROUGH EVERY SOURCE ID AND ADD IT TO ALL SOURCES RETURNED
        sources = Source.objects.all().filter(pk__in=source_id_list)

        #form dictionary with id, text, and url for each source
        qset_dicts = []
        for source in sources:
            transformed = str(source)
            transformed = ast.literal_eval(transformed)
            qset_dicts.append(transformed)

        #print("QSET_DICTS: ", qset_dicts)
        # p = Paginator(qset_dicts, 5)    #pagination
        # print("p:", p.num_pages)

        ranked_data = rank(p_kw, sec_kw, qset_dicts)
        #queryset_to_rank = Source.objects.filter(pk__in=source_id_list).values('text', 'url')
        #print("FINAL SOURCES TO RANK: ", queryset_to_rank)
        # now we begin the reranking process by running the rank function defined at the top
        #ranked_results = rank(p_kw, sec_kw, sources)
        #print("RANKED RESULTS: ", ranked_results)
        #print("RANKED DATA: ", len(ranked_data))
        #print("Data to compare to: ", data.object_list)
        # GET LIST OF RANKED ID'S IN ORDER
        ranked_ids = []
        for x in ranked_data:
            ranked_ids.append(x['id'])
        #print(ranked_ids)
        # PAGINATE THE NEW RANKED DATA:
        # p2 = Paginator(ranked_data, 5)
        # print('p2:', p2.num_pages)
        # data2 = p2.get_page(page_id)
        # print(data2.object_list)

        #WHAT IT SHOULD LOOK LIKE:
        ranked_sources = []
        for y in range(len(ranked_ids)):
            ranked_sources.append(Source.objects.get(pk=ranked_ids[y]))
        #ranked_sources = Source.objects.filter(pk__in=ranked_ids)
        print("RANKED SOURCES: ", ranked_sources)
        p = Paginator(ranked_sources, 5)    #pagination
        print("p:", p.num_pages)
        data = serializers.serialize('json', p.get_page(page_id))
        print("FINAL DATA: ", data) 
        # # look into how this works and why pagination isn't applied
        # return HttpResponse(data)

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