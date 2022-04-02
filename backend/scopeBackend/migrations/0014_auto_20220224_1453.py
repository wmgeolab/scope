# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-02-24 19:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scopeBackend', '0013_auto_20220224_1432'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result',
            old_name='src',
            new_name='source',
        ),
        migrations.RemoveField(
            model_name='run',
            name='result',
        ),
        migrations.AddField(
            model_name='result',
            name='run',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='scopeBackend.Run'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='run',
            name='time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='result',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='run',
            name='id',
            field=models.PositiveIntegerField(primary_key=True, serialize=False),
        ),
    ]