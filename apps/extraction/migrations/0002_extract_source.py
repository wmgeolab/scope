# Generated by Django 3.1.3 on 2020-11-28 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sourcing', '0001_initial'),
        ('extraction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='extract',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='extracts', to='sourcing.source'),
        ),
    ]