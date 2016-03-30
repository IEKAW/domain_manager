from __future__ import unicode_literals

from django.db import models


class Domain(models.Model):
    """docstring for Domain"""
    domain_name = models.CharField(max_length=255)
    japanese = models.CharField(max_length=255)
    updated_date = models.DateField()
    domain_company = models.CharField(max_length=255)
    domain_company_url = models.CharField(max_length=255, null=True)
    server_company = models.CharField(max_length=255, null=True)
    update_method = models.CharField(max_length=255, null=True)


class Site(models.Model):
    """docstring for Site"""
    group_name = models.CharField(max_length=255)
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
    update_method = models.CharField(max_length=255, null=True)


class SiteComment(models.Model):
    """docstring for SiteComment"""
    site_id = models.IntegerField()
    comment = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField()


class Link(models.Model):
    """docstring for Link"""
    site_title = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255, null=True)
    server = models.CharField(max_length=255, null=True)
    to_url = models.CharField(max_length=255, null=True)
    to_site = models.CharField(max_length=255, null=True)
    link_position = models.CharField(max_length=255, null=True)
    from_id = models.IntegerField(null=True)
    to_id = models.IntegerField(null=True)
    created_at = models.DateField()


class DomainDetail(models.Model):
    """docstring for DomainDetail"""
    domain_id = models.IntegerField()
    url = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255, null=True)
    is_representative = models.BooleanField(default=False)


class Group(models.Model):
    group = models.CharField(max_length=255)


class Payment(models.Model):
    payment = models.CharField(max_length=255)


class Setting_Link(models.Model):
    link = models.CharField(max_length=255)


class Templates(models.Model):
    templates = models.CharField(max_length=255)


class Setting_Server(models.Model):
    server_company = models.CharField(max_length=255)
    login_url = models.CharField(max_length=255)
    login_id = models.CharField(max_length=255, null=True)
    login_pass = models.CharField(max_length=255, null=True)
    nameserver1 = models.CharField(max_length=255, null=True)
    nameserver2 = models.CharField(max_length=255, null=True)
    nameserver3 = models.CharField(max_length=255, null=True)
    nameserver4= models.CharField(max_length=255, null=True)
    nameserver5 = models.CharField(max_length=255, null=True)


class Setting_Domain(models.Model):
    domain_company = models.CharField(max_length=255)
    login_url = models.CharField(max_length=255)
    login_id = models.CharField(max_length=255, null=True)
    login_pass = models.CharField(max_length=255, null=True)


class Keywords(models.Model):
    keyword = models.CharField(max_length=255)
    site_id = models.IntegerField(null=False)
    created_date = models.DateField()
