# Generated by Django 3.1.3 on 2021-03-25 01:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0002_auto_20210325_0156'),
        ('parsing_m', '0005_auto_20210325_0229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_subcode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='domain.activitysubcode'),
        ),
    ]