# coding: utf8

from django.db import connection


def get_domain_info(search_index):
    if search_index is None:
        sql = """
            SELECT
                *
            FROM
                system_domain
        """
    else:
        search_index = '%' + search_index + '%'
        sql = """
            SELECT
                *
            FROM
                system_domain
            WHERE
                domain_company
            LIKE
                '%s'
            OR
                domain_name
            LIKE
                '%s'
            OR
                japanese
            LIKE
                '%s'
        """ % (search_index, search_index, search_index)
    cursor = connection.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        yield row


def get_server_info(search_index):
    if search_index is None:
        sql = """
            SELECT
                *
            FROM
                system_server
        """
    else:
        search_index = '%' + search_index + '%'
        sql = """
            SELECT
                *
            FROM
                system_server
            WHERE
                server_company
            LIKE
                '%s'
        """ % (search_index)
    cursor = connection.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        yield row


def get_site_info(search_index, is_all=True):
    if is_all is False:
        search_index = '%' + search_index + '%'
        sql = """
            SELECT
                *
            FROM
                system_site
            WHERE
                group_name
            LIKE
                '%s'
        """ % (search_index)
    else:
        if search_index is None:
            sql = """
                SELECT
                    *
                FROM
                    system_site
            """
        else:
            search_index = '%' + search_index + '%'
            sql = """
                SELECT
                    *
                FROM
                    system_site
                WHERE
                    site_title
                LIKE
                    '%s'
                OR
                    url
                LIKE
                    '%s'
                OR
                    site_title
                LIKE
                    '%s'
                OR
                    japanese
                LIKE
                    '%s'
                OR
                    server
                LIKE
                    '%s'
            """ % (
                search_index,
                search_index,
                search_index,
                search_index,
                search_index
            )
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
