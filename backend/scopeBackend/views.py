# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserSerializer, QuerySerializer
from .models import User, Query
# from backend.scopeBackend import serializers

# Create your views here.

class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class QueryView(viewsets.ModelViewSet):
    serializer_class = QuerySerializer
    queryset = Query.objects.all()

