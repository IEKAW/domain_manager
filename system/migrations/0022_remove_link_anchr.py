# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-21 05:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0021_link_anchr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='anchr',
        ),
    ]
