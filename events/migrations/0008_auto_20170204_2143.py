# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-04 21:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20170204_2140'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='event_type',
            new_name='event_types',
        ),
    ]
