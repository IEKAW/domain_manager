# coding: utf8

from django.db import connection


def get_domain_info():
    sql = """
        SELECT
            *
        FROM
            system_domain
    """
    cursor = connection.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        yield row


def get_server_info():
    sql = """
        SELECT
            *
        FROM
            system_server
    """
    cursor = connection.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        yield row


def get_site_info():
    sql = """
        SELECT
            *
        FROM
            system_site
    """
    cursor = connection.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        yield row


def get_domain_detail(domain_id):
    sql = """
        SELECT
            *
        FROM
            system_domaindetail
        WHERE
            system_domaindetail.domain_id = %s
    """ % domain_id
    cursor = connection.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        yield row


def get_special_domain(domain_id):
    sql = """
        SELECT
            *
        FROM
            system_domain
        WHERE
            system_domain.id = %s
    """ % domain_id
    cursor = connection.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        yield row


def get_special_server(server_id):
    sql = """
        SELECT
            *
        FROM
            system_server
        WHERE
            system_server.id = %s
    """ % server_id
    cursor = connection.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        yield row
