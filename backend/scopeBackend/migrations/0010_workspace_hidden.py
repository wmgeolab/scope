# Generated by Django 4.1.1 on 2024-04-26 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scopeBackend', '0009_workspace_hidden_alter_airesponse_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='workspace',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]
