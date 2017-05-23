# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-23 02:51
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssociatedLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'app_associated_location',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_updated', models.DateTimeField(auto_now=True)),
                ('street_address_line1', models.CharField(max_length=455)),
                ('street_address_line2', models.CharField(blank=True, default='', max_length=255)),
                ('postal_code', models.CharField(max_length=25)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(blank=True, default='USA', max_length=100)),
            ],
            options={
                'db_table': 'app_location',
            },
        ),
        migrations.AddField(
            model_name='associatedlocation',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.Location'),
        ),
    ]
