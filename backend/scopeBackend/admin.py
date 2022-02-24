# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Query, User, KeyWord, SourceType, Source, Result, Run

class ScopeBackendAdmin(admin.ModelAdmin):
    #list_display = ('title', 'description', 'completed')
    list_display = ['id']

# Register your models here.
admin.site.register([Query, User, KeyWord, SourceType, Source, Result, Run], ScopeBackendAdmin)
