# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-04 02:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0014_link_server'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='from_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='link',
            name='to_id',
            field=models.IntegerField(null=True),
        ),
    ]