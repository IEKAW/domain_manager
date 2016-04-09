# coding: utf8

from django.db import connection


def get_domain_info(search_index, reverse):
    if search_index is None:
        if reverse is True:
            sql = """
                SELECT
                    *
                FROM
                    system_domain
                ORDER BY
                    updated_date DESC
            """
        else:
            sql = """
                SELECT
                    *
                FROM
                    system_domain
                ORDER BY
                    updated_date
            """
    else:
        search_index = '%' + search_index + '%'
        if reverse is True:
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
                ORDER BY
                    updated_date DESC
            """ % (search_index, search_index, search_index)
        else:
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
                ORDER BY
                    updated_date
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
        if search_index == 'all':
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


def get_domain_near_info(day):
    sql = """
        SELECT
            *
        FROM
            system_domain
        WHERE
            updated_date <= '%s'
        ORDER BY
            updated_date DESC
    """ % day
    cursor = connection.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        yield row


def get_server_near_info(day):
    sql = """
        SELECT
            *
        FROM
            system_server
        WHERE
            updated_date <= '%s'
    """ % day
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
            ORDER BY
                updated_date
        """ % (search_index)
    else:
        if search_index is None or search_index == 'all':
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
                ORDER BY
                    updated_date
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


def get_site_detail(site_id):
    sql = """
        SELECT
            *
        FROM
            system_site
        WHERE
            id =  %s
    """ % site_id
    cursor = connection.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        yield row


def get_site_comment(site_id):
    sql = """
        SELECT
            *
        FROM
            system_sitecomment
        WHERE
            site_id = %s
        ORDER BY
            created_at DESC
    """ % site_id
    cursor = connection.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        yield row


def get_site_list():
    sql = """
        SELECT
            site_title,
            url
        FROM
            system_site
        ORDER BY
            url
    """
    cursor = connection.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        yield row


def raw_get_site_from_url(url):
    sql = """
        SELECT
            site_title
        FROM
            system_site
    """
    cursor = connection.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        yield row


def raw_get_url_from_site(site_title):
    sql = """
        SELECT
            url
        FROM
            system_site
        WHERE
            site_title = '%s'
        ORDER BY
            url
    """ % site_title
    cursor = connection.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        yield row


def get_exact_group(site_id):
    sql = """
        SELECT
            *
        FROM
            system_group
        WHERE
            id = %s
    """ % site_id
    cursor = connection.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        yield row


def get_exact_templates(site_id):
    sql = """
        SELECT
            *
        FROM
            system_templates
        WHERE
            id = %s
    """ % site_id
    cursor = connection.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        yield row

def get_exact_link(site_id):
    sql = """
        SELECT
            *
        FROM
            system_setting_link
        WHERE
            id = %s
    """ % site_id
    cursor = connection.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        yield row


def get_exact_payment(site_id):
    sql = """
        SELECT
            *
        FROM
            system_payment
        WHERE
            id = %s
    """ % site_id
    cursor = connection.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        yield row


def get_exact_server(site_id):
    sql = """
        SELECT
            *
        FROM
            system_setting_server
        WHERE
            id = %s
    """ % site_id
    cursor = connection.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        yield row


def get_link_info(site_id):
    sql = """
        SELECT
            *
        FROM
            system_link
        WHERE
            from_id = %s
    """ % site_id
    cursor = connection.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        yield row
