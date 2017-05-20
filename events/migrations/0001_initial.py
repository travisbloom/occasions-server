# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-20 14:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssociatedEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-datetime_updated',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, default='')),
                ('is_default_event', models.BooleanField(default=True)),
                ('is_reoccuring_yearly', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-datetime_updated',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EventDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_dates', to='events.Event')),
            ],
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('display_name', models.CharField(max_length=255)),
                ('is_externally_visible', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-datetime_updated',),
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='event',
            name='event_types',
            field=models.ManyToManyField(related_name='events', to='events.EventType'),
        ),
    ]
