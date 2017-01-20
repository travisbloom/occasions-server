# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-20 04:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20160905_2319'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='associatedevent',
            options={'ordering': ['-datetime_updated']},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['-datetime_updated']},
        ),
        migrations.AlterField(
            model_name='associatedevent',
            name='datetime_created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='associatedevent',
            name='datetime_updated',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='datetime_created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='datetime_updated',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
    ]
