# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-23 02:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
        ('locations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('people', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_updated', models.DateTimeField(auto_now=True)),
                ('cost_usd', models.DecimalField(decimal_places=2, max_digits=5)),
                ('product_notes', models.TextField()),
                ('stripe_transaction_id', models.CharField(blank=True, default='', max_length=255)),
                ('associated_event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='events.AssociatedEvent')),
                ('associated_event_date', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='events.EventDate')),
                ('associated_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='locations.AssociatedLocation')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='products.Product')),
                ('receiving_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_transactions', to='people.Person')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'app_transaction',
                'default_related_name': 'transactions',
            },
        ),
    ]
