from __future__ import unicode_literals

from django.db import models


class Domain(models.Model):
    """docstring for Domain"""
    domain_name = models.CharField(max_length=255)
    japanese = models.CharField(max_length=255)
    updated_date = models.DateField()
    domain_company = models.CharField(max_length=255)
    domain_company_url = models.CharField(max_length=255, null=True)


class Site(models.Model):
    """docstring for Site"""
    group = models.CharField(max_length=255)
    site_title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    japanese = models.CharField(max_length=255)
    server = models.CharField(max_length=255)
    updated_date = models.DateField(null=True)
    template = models.CharField(max_length=255, null=True)
    login_url = models.CharField(max_length=255, null=True)
    login_id = models.CharField(max_length=255, null=True)
    login_pass = models.CharField(max_length=255, null=True)
    remarks = models.TextField(null=True)


class Server(models.Model):
    """docstring for Server"""
    server_company = models.CharField(max_length=255)
    updated_date = models.DateField()
    host = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True)
    ftp_pass = models.CharField(max_length=255, null=True)
    db_pass = models.CharField(max_length=255, null=True)
    payment = models.CharField(max_length=255, null=True)
    remarks = models.TextField(null=True)
    login_id = models.CharField(max_length=255, null=True)
    login_pass = models.CharField(max_length=255, null=True)


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


class DomainDetail(models.Model):
    """docstring for DomainDetail"""
    domain_id = models.IntegerField()
    url = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255, null=True)
    is_representative = models.BooleanField(default=False)
