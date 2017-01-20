# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-20 04:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ['-datetime_updated']},
        ),
        migrations.AlterField(
            model_name='location',
            name='datetime_created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='datetime_updated',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='personlocation',
            name='datetime_created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='personlocation',
            name='datetime_updated',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
    ]