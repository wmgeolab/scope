# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-02-22 19:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scopeBackend', '0003_query_start_datetime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='query',
            name='completed',
        ),
        migrations.RemoveField(
            model_name='query',
            name='title',
        ),
        migrations.RemoveField(
            model_name='scopebackend',
            name='title',
        ),
        migrations.AddField(
            model_name='query',
            name='q_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='scopebackend',
            name='id',
            field=models.PositiveIntegerField(primary_key=True, serialize=False),
        ),
    ]