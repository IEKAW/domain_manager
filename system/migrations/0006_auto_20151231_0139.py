# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-30 16:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0005_auto_20151231_0116'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='login_id',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='site',
            name='login_pass',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='site',
            name='login_url',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='site',
            name='remarks',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='site',
            name='template',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='site',
            name='updated_date',
            field=models.DateField(null=True),
        ),
    ]
