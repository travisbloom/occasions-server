# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-07 01:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20170205_0328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='country',
            field=models.CharField(blank=True, default='USA', max_length=100),
        ),
    ]
