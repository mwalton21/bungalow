# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-08-01 01:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zillow', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField()),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tax_value', models.PositiveIntegerField()),
                ('tax_year', models.PositiveIntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='listing',
            name=b'price',
        ),
        migrations.RemoveField(
            model_name='listing',
            name=b'tax_value',
        ),
        migrations.RemoveField(
            model_name='listing',
            name=b'tax_year',
        ),
        migrations.AddField(
            model_name='tax',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zillow.Listing'),
        ),
        migrations.AddField(
            model_name='price',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zillow.Listing'),
        ),
    ]
