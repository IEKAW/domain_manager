# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-21 05:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0020_server_login_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='anchr',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
