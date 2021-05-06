# Generated by Django 3.1.2 on 2021-03-30 02:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sourcing_m', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_status', models.CharField(blank=True, choices=[('SRCA', 'sourced_a')], default='SRCA', max_length=9)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sources', to='sourcing_m.source')),
            ],
        ),
    ]