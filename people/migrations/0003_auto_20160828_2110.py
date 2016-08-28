# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-28 21:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0002_auto_20160828_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.EmailField(error_messages={'unique': 'A user with that email already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, verbose_name='username'),
        ),
    ]