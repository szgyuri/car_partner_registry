# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-11-05 19:08
from __future__ import unicode_literals

from django.db import migrations, models
import unixtimestampfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=160)),
                ('city', models.CharField(max_length=180)),
                ('address', models.CharField(max_length=200)),
                ('company_name', models.CharField(max_length=200)),
                ('created_at', unixtimestampfield.fields.UnixTimeStampField(auto_now_add=True)),
                ('modified_at', unixtimestampfield.fields.UnixTimeStampField(auto_now=True)),
                ('deleted_at', unixtimestampfield.fields.UnixTimeStampField(blank=True)),
            ],
        ),
    ]
