# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-04 01:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0013_auto_20160223_0431'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='server',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
