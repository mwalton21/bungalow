# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-08-01 01:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zillow', '0002_auto_20200731_2012'),
    ]

    operations = [
        migrations.CreateModel(
            name='RentEstimate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estimate_amount', models.PositiveIntegerField()),
                ('estimate_date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='building',
            name=b'listing',
        ),
        migrations.RemoveField(
            model_name='rent',
            name=b'estimate_amount',
        ),
        migrations.RemoveField(
            model_name='rent',
            name=b'estimate_date',
        ),
        migrations.AddField(
            model_name='listing',
            name='bathrooms',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='bedrooms',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='size',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='year_build',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='rent',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.DeleteModel(
            name='Building',
        ),
        migrations.AddField(
            model_name='rentestimate',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zillow.Listing'),
        ),
    ]
