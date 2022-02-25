# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-02-22 20:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scopeBackend', '0004_auto_20220222_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='query',
            name='description',
        ),
        migrations.RemoveField(
            model_name='query',
            name='q_id',
        ),
        migrations.RemoveField(
            model_name='query',
            name='start_datetime',
        ),
        migrations.AddField(
            model_name='query',
            name='name',
            field=models.CharField(default='', max_length=120),
        ),
        migrations.AlterField(
            model_name='query',
            name='id',
            field=models.PositiveIntegerField(primary_key=True, serialize=False),
        ),
    ]
