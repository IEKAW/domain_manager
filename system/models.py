from __future__ import unicode_literals

from django.db import models


class Domain(models.Model):
    """docstring for Domain"""
    domain_name = models.CharField(max_length=255)
    japanese = models.CharField(max_length=255)
    updated_date = models.DateField()
    domain_company = models.CharField(max_length=255)
    representative = models.CharField(max_length=255)


class Site(models.Model):
    """docstring for Site"""
    group = models.CharField(max_length=255)
    site_title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    japanese = models.CharField(max_length=255)
    server = models.CharField(max_length=255)


class Server(models.Model):
    """docstring for Server"""
    server_company = models.CharField(max_length=255)
    updated_date = models.DateField()
    host = models.CharField(max_length=255)


class SiteComment(models.Model):
    """docstring for SiteComment"""
    site_id = models.IntegerField()
    comment = models.CharField(max_length=255)
    created_at = models.DateField()


class Link(models.Model):
    """docstring for Link"""
    from_site = models.IntegerField()
    to_site = models.IntegerField()
    link_position = models.CharField(max_length=255)
    created_at = models.DateField()
