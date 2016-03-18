# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-18 04:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0015_auto_20160304_1105'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Setting_Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain_company', models.CharField(max_length=255)),
                ('login_url', models.CharField(max_length=255)),
                ('login_id', models.CharField(max_length=255, null=True)),
                ('login_pass', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Setting_Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Setting_Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_company', models.CharField(max_length=255)),
                ('login_url', models.CharField(max_length=255)),
                ('login_id', models.CharField(max_length=255, null=True)),
                ('login_pass', models.CharField(max_length=255, null=True)),
                ('nameserver1', models.CharField(max_length=255, null=True)),
                ('nameserver2', models.CharField(max_length=255, null=True)),
                ('nameserver3', models.CharField(max_length=255, null=True)),
                ('nameserver4', models.CharField(max_length=255, null=True)),
                ('nameserver5', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Templates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('templates', models.CharField(max_length=255)),
            ],
        ),
    ]
