# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-02-22 19:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scopeBackend', '0002_query'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='start_datetime',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]