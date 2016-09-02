# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-29 02:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('people', '0004_auto_20160829_0252'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_updated', models.DateTimeField(auto_now=True)),
                ('street_number', models.CharField(max_length=50)),
                ('street_name', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=25)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PersonLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_updated', models.DateTimeField(auto_now=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.Location')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='people.Person')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='personlocation',
            unique_together=set([('person', 'location')]),
        ),
    ]