#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta
from util.common import (
    url_idna_quote,
    url_pyu_quote
)
from datetime import datetime as dt

from system.models import(
    Domain,
    Server,
    Site,
    DomainDetail,
    SiteComment,
    Link,
    Payment,
    Templates,
    Setting_Link,
    Setting_Server,
    Group,
    Setting_Domain,
    Keywords
)

from system.aggregate import(
    get_domain_info,
    get_server_info,
    get_site_info,
    get_special_domain,
    get_domain_detail,
    get_special_server,
    get_site_detail,
    get_site_comment,
    get_site_list,
    raw_get_site_from_url,
    get_exact_group,
    get_exact_server,
    get_exact_payment,
    get_exact_link,
    get_exact_templates,
    get_link_info,
    get_domain_near_info,
    get_server_near_info,
    raw_get_url_from_site,
)

COLOR_LIST = [
    'info',
    'success',
    'warning',
    'danger',
    'active'
]


@login_required
def home(request):
    data = {'domain': [], 'server': []}
    today = datetime.today() + timedelta(weeks=4)
    day = datetime.strftime(today, '%Y-%m-%d')
    raw_domain_datas = get_domain_near_info(day)
    for domain_data in raw_domain_datas:
        if domain_data[6] != "not_update":
            try:
                tmp = {}
                tmp['id'] = domain_data[0]
                tmp['domain'] = domain_data[1]
                tmp['japanese'] = domain_data[2]
                tmp['updated_at'] = domain_data[3]
                tmp['company'] = domain_data[4]
                setting_domain = Setting_Domain.objects.get(
                    domain_company=domain_data[4]
                )
                tmp['company_url'] = setting_domain.login_url
                domaindetail = DomainDetail.objects.get(
                    domain_id=domain_data[0],
                    is_representative=True
                )
                tmp['representative'] = domaindetail.title
                tmp['site_id'] = -1
                tmp['server_id'] = -1
                try:
                    site_id = Site.objects.get(site_title=domaindetail.title)
                    tmp['site_id'] = site_id.id
                except:
                    pass
                try:
                    server_id = Server.objects.get(server=domain_data[7])
                    tmp['server_id'] = server_id.id
                except:
                    pass
                data['domain'].append(tmp)
            except:
                tmp = {}
                tmp['id'] = domain_data[0]
                tmp['domain'] = domain_data[1]
                tmp['japanese'] = domain_data[2]
                tmp['updated_at'] = domain_data[3]
                tmp['company'] = domain_data[4]
                try:
                    setting_domain = Setting_Domain.objects.get(
                        domain_company=domain_data[4]
                        )
                    tmp['company_url'] = setting_domain.login_url
                except:
                    tmp['company_url'] = ""
                tmp['representative'] = "not selected"
                tmp['server_id'] = -1
                data['domain'].append(tmp)
            if tmp['domain'] == tmp['japanese']:
                tmp['japanese'] = ""
    raw_server_datas = get_server_near_info(day)
    for server_data in raw_server_datas:
        if server_data[11] != "not_update":
            tmp = {}
            tmp['id'] = server_data[0]
            tmp['company'] = server_data[1]
            tmp['updated_at'] = server_data[2]
            tmp['host'] = server_data[3]
            data['server'].append(tmp)
    result = {'data': data}
    return render(request, 'system/index.html', result)


@login_required
def server(request):
    data = []
    server = []
    search_index = None
    try:
        search_index = request.GET['search']
    except:
        pass
    raw_server_datas = get_server_info(search_index)
    for server_data in raw_server_datas:
        if server_data[11] != "not_update":
            tmp = {}
            tmp['id'] = server_data[0]
            tmp['company'] = server_data[1]
            tmp['updated_at'] = server_data[2]
            tmp['host'] = server_data[3]
            data.append(tmp)
    raw_server = get_server_info(None)
    for r in raw_server:
        if server_data[11] != "not_update":
            if r[1] not in server and r[12] == r[1]:
                    server.append(r[1])
    result = {'data': data, 'method': 'server', 'server': server}
    return render(request, 'system/server.html', result)


@login_required
def site(request):
    data = []
    group = []
    search_index = None
    if request.method == 'POST':
        search_index = request.POST['search']
    try:
        search_index = request.GET['search']
        raw_site_datas = get_site_info(search_index, False)
    except:
        raw_site_datas = get_site_info(search_index)
    for site_data in raw_site_datas:
        tmp = {}
        tmp['id'] = site_data[0]
        tmp['title'] = site_data[2]
        tmp['url'] = site_data[3]
        tmp['group'] = site_data[1]
        tmp['japanese'] = site_data[4]
        tmp['server'] = site_data[5]
        tmp['server_id'] = -1
        if tmp['japanese'] == tmp['url']:
            tmp['japanese'] = ''
        try:
            server_id = Server.objects.get(server_company=site_data[5])
            tmp['server_id'] = server_id.id
        except:
            pass
        data.append(tmp)
    groups = Group.objects.all()
    for raw in groups:
        if raw.group not in group:
            group.append(raw.group)
    result = {'data': data, 'method': 'site', 'group': group}
    return render(request, 'system/site.html', result)


@login_required
def domain(request):
    reverse = False
    search_index = None
    if request.method == 'POST':
        search_index = request.POST['search']
    elif request.method == 'GET':
        try:
            if request.GET['search_index'] == 'None':
                search_index = None
            else:
                search_index = request.GET['search_index']
        except:
            search_index = None
    if request.method == 'GET':
        try:
            if request.GET['reverse'] == 'False':
                reverse = False
            else:
                reverse = True
        except:
            reverse = False
    data = []
    raw_domain_datas = get_domain_info(search_index, reverse)
    for domain_data in raw_domain_datas:
        if domain_data[6] != "not_update":
            try:
                tmp = {}
                tmp['id'] = domain_data[0]
                tmp['domain'] = domain_data[1]
                tmp['japanese'] = domain_data[2]
                tmp['updated_at'] = domain_data[3]
                tmp['company'] = domain_data[4]
                try:
                    setting_domain = Setting_Domain.objects.get(
                        domain_company=domain_data[4]
                    )
                    tmp['company_url'] = setting_domain.login_url
                except:
                    tmp['company_url'] = ""
                domaindetail = DomainDetail.objects.get(
                    domain_id=domain_data[0],
                    is_representative=True
                )
                tmp['representative'] = domaindetail.title
                tmp['site_id'] = -1
                tmp['server_id'] = -1
                try:
                    site_id = Site.objects.get(site_title=domaindetail.title)
                    tmp['site_id'] = site_id.id
                except:
                    pass
                try:
                    server_id = Server.objects.get(server=domain_data[7])
                    tmp['server_id'] = server_id.id
                except:
                    pass
                if tmp['japanese'][:7] == 'http://':
                    tmp['japanese'] = tmp['japanese'][7:]
                data.append(tmp)
            except:
                tmp = {}
                tmp['id'] = domain_data[0]
                tmp['domain'] = domain_data[1]
                tmp['japanese'] = domain_data[2]
                tmp['updated_at'] = domain_data[3]
                tmp['company'] = domain_data[4]
                try:
                    setting_domain = Setting_Domain.objects.get(
                        domain_company=domain_data[4]
                    )
                    tmp['company_url'] = setting_domain.login_url
                except:
                    tmp['company_url'] = ""
                tmp['representative'] = "not selected"
                if tmp['japanese'][:7] == 'http://':
                    tmp['japanese'] = tmp['japanese'][7:]
                data.append(tmp)
            if tmp['domain'] == tmp['japanese']:
                tmp['japanese'] = ""
    result = {'data': data, 'method': 'domain', 'search_index': search_index, 'reverse': reverse}
    return render(request, 'system/domain.html', result)


@login_required
def server_unup(request):
    if request.method == "POST":
        update_id = request.POST['id']
        Server.objects.filter(id=update_id).update(update_method="not_update")
    data = []
    server = []
    today = datetime.now()
    search_index = None
    try:
        search_index = request.GET['search']
    except:
        pass
    raw_server_datas = get_server_info(search_index)
    for server_data in raw_server_datas:
        if server_data[11] == "not_update":
            tmp = {}
            tmp['id'] = server_data[0]
            tmp['company'] = server_data[1]
            tmp['updated_at'] = server_data[2]
            tmp['host'] = server_data[3]
            if (today > dt.strptime(dt.strftime(server_data[2], '%Y-%m-%d'), '%Y-%m-%d')) == True:
                tmp['pass'] = 1
            else:
                tmp['pass'] = 0
            data.append(tmp)
    raw_server = get_server_info(None)
    for r in raw_server:
        if server_data[11] == "not_update":
            if r[1] not in server:
                    server.append(r[1])
    result = {'data': data, 'index': search_index, 'server': server}
    return render(request, 'system/server_unup.html', result)


@login_required
def domain_unup(request):
    reverse = False
    if request.method == "POST":
        update_id = request.POST['id']
        Domain.objects.filter(id=update_id).update(update_method="not_update")
    if request.method == 'GET':
        try:
            if request.GET['reverse'] == 'False':
                reverse = False
            else:
                reverse = True
        except:
            reverse = False
    data = []
    today = datetime.now()
    raw_domain_datas = get_domain_info(None, reverse)
    for domain_data in raw_domain_datas:
        if domain_data[6] == "not_update":
            try:
                tmp = {}
                tmp['id'] = domain_data[0]
                tmp['domain'] = domain_data[1]
                tmp['japanese'] = domain_data[2]
                tmp['updated_at'] = domain_data[3]
                tmp['company'] = domain_data[4]
                setting_domain = Setting_Domain.objects.get(
                    domain_company=domain_data[4]
                )
                tmp['company_url'] = setting_domain.login_url
                domaindetail = DomainDetail.objects.get(
                    domain_id=domain_data[0],
                    is_representative=True
                )
                tmp['representative'] = domaindetail.title
                tmp['site_id'] = -1
                tmp['server_id'] = -1
                try:
                    site_id = Site.objects.get(site_title=domaindetail.title)
                    tmp['site_id'] = site_id.id
                except:
                    pass
                try:
                    server_id = Server.objects.get(server=domain_data[7])
                    tmp['server_id'] = server_id.id
                except:
                    pass
                if (today > dt.strptime(dt.strftime(domain_data[3], '%Y-%m-%d'), '%Y-%m-%d')) == True:
                    tmp['pass'] = 1
                else:
                    tmp['pass'] = 0
                if tmp['japanese'][:7] == 'http://':
                    tmp['japanese'] = tmp['japanese'][7:]
                data.append(tmp)
            except:
                tmp = {}
                tmp['id'] = domain_data[0]
                tmp['domain'] = domain_data[1]
                tmp['japanese'] = domain_data[2]
                tmp['updated_at'] = domain_data[3]
                tmp['company'] = domain_data[4]
                try:
                    setting_domain = Setting_Domain.objects.get(
                        domain_company=domain_data[4]
                        )
                    tmp['company_url'] = setting_domain.login_url
                except:
                    tmp['company_url'] = ""
                if (today > dt.strptime(dt.strftime(domain_data[3], '%Y-%m-%d'), '%Y-%m-%d')) == True:
                    tmp['pass'] = 1
                else:
                    tmp['pass'] = 0
                tmp['representative'] = "not selected"
                if tmp['japanese'][:7] == 'http://':
                    tmp['japanese'] = tmp['japanese'][7:]
                data.append(tmp)
    result = {'data': data, 'reverse': reverse}
    return render(request, 'system/domain_unup.html', result)


@login_required
def domain_detail(request):
    if request.method == 'POST':
        domain_id = request.POST['domain_id']
        try:
            representative = DomainDetail.objects.get(
                domain_id=domain_id,
                is_representative=True
            )
            representative.is_representative = False
            representative.save()
        except:
            pass
        detail_id = request.POST['id']
        domain_obj = DomainDetail.objects.get(
            id=detail_id
        )
        domain_obj.is_representative = True
        domain_obj.save()
        data = {'detail': []}
        domain = get_special_domain(domain_id)
        details = get_domain_detail(domain_id)
        for raw in domain:
            data['domain'] = raw[1]
            data['japanese'] = raw[2]
            data['updated_at'] = raw[3]
            data['company'] = raw[4]
            setting_domain = Setting_Domain.objects.get(
                domain_company=raw[4]
            )
            data['company_url'] = setting_domain.login_url
            data['server'] = raw[7]
            if data['japanese'][:7] == 'http://':
                data['japanese'] = data['japanese'][7:]
        for detail in details:
            tmp = {}
            tmp['id'] = detail[0]
            tmp['domain_id'] = detail[1]
            tmp['url'] = detail[2]
            site_obj = Site.objects.filter(url=tmp['url']).all()[:1].get()
            tmp['site_id'] = site_obj.id
            tmp['title'] = detail[3]
            tmp['is_represetative'] = detail[4]
            try:
                server_id = Server.objects.get(server_company=data['server'])
                tmp['server_id'] = server_id.id
            except:
                tmp['server_id'] = -1
            data['detail'].append(tmp)
        result = {'data': data, 'id': domain_id}
        return render(request, 'system/domain_detail.html', result)
    elif request.method == 'GET':
        data = {'detail': []}
        domain_id = request.GET['domain_id']
        domain = get_special_domain(domain_id)
        details = get_domain_detail(domain_id)
        for raw in domain:
            data['updated_at'] = raw[3]
            data['company'] = raw[4]
            try:
                setting_domain = Setting_Domain.objects.get(
                    domain_company=raw[4]
                )
                data['company_url'] = setting_domain.login_url
            except:
                data['company_url'] = ""
            data['domain'] = raw[1]
            data['japanese'] = raw[2]
            data['server'] = raw[7]
            if data['japanese'][:7] == 'http://':
                data['japanese'] = data['japanese'][7:]
        for detail in details:
            tmp = {}
            tmp['id'] = detail[0]
            tmp['domain_id'] = detail[1]
            tmp['url'] = detail[2]
            site_obj = Site.objects.filter(url=tmp['url']).all()[:1].get()
            tmp['site_id'] = site_obj.id
            tmp['title'] = detail[3]
            tmp['is_represetative'] = detail[4]
            try:
                server_id = Server.objects.get(server_company=data['server'])
                tmp['server_id'] = server_id.id
            except:
                tmp['server_id'] = -1
            data['detail'].append(tmp)
        result = {'data': data, 'method': 'domain', 'id': domain_id}
        return render(request, 'system/domain_detail.html', result)


@login_required
def server_detail(request):
    data = {}
    server_id = request.GET['server_id']
    server = get_special_server(server_id)
    for raw in server:
        data['server'] = raw[1]
        try:
            obj = Setting_Server.objects.get(
                server_company=raw[12]
            )
            data['nameserver1'] = obj.nameserver1
            data['nameserver2'] = obj.nameserver2
            data['nameserver3'] = obj.nameserver3
            data['nameserver4'] = obj.nameserver4
            data['nameserver5'] = obj.nameserver5
            data['url'] = obj.login_url
        except:
            data['nameserver1'] = ''
            data['nameserver2'] = ''
            data['nameserver3'] = ''
            data['nameserver4'] = ''
            data['nameserver5'] = ''
            data['url'] = ''
        data['update_at'] = raw[2]
        data['host'] = raw[3]
        data['username'] = raw[8]
        data['ftp_pass'] = raw[5]
        data['db_pass'] = raw[4]
        data['payment'] = raw[6]
        data['remarks'] = raw[7]
        data['login_url'] = raw[13]
        data['login_id'] = raw[9]
        data['login_pass'] = raw[10]
    result = {'data': data, 'method': 'server', 'server_id': server_id}
    return render(request, 'system/server_detail.html', result)


@login_required
def update_domain(request):
    if request.method == 'GET':
        data = {}
        domain_id = request.GET['domain_id']
        domain = get_special_domain(domain_id)
        data['id'] = domain_id
        for raw in domain:
            data['domain'] = raw[1]
            year_int = raw[3].year + 1
            year = '%d' % year_int
            if raw[3].month < 10:
                month = '0%d' % raw[3].month
            else:
                month = '%d' % raw[3].month
            if raw[3].day < 10:
                day = '0%d' % raw[3].day
            else:
                day = '%d' % raw[3].day
            data['update_at'] = year + '-' + month + '-' + day
        result = {'data': data}
        return render(request, 'system/update_domain.html', result)
    elif request.method == 'POST':
        domain_id = request.POST['id']
        update_at = request.POST['update_at']
        domain_obj = Domain.objects.get(id=domain_id)
        domain_obj.updated_date = update_at
        domain_obj.update_method = "hand"
        domain_obj.save()
        return HttpResponseRedirect('/django.cgi/domain')


@login_required
def update_server(request):
    if request.method == 'GET':
        data = {}
        server_id = request.GET['server_id']
        server = get_special_server(server_id)
        data['id'] = server_id
        for raw in server:
            data['server'] = raw[1]
            year_int = raw[2].year + 1
            year = '%d' % year_int
            if raw[2].month < 10:
                month = '0%d' % raw[2].month
            else:
                month = '%d' % raw[2].month
            if raw[2].day < 10:
                day = '0%d' % raw[2].day
            else:
                day = '%d' % raw[2].day
            data['update_at'] = year + '-' + month + '-' + day
        result = {'data': data}
        return render(request, 'system/update_server.html', result)
    elif request.method == 'POST':
        server_id = request.POST['id']
        update_at = request.POST['update_at']
        server_obj = Server.objects.get(id=server_id)
        server_obj.updated_date = update_at
        server_obj.update_method = "hand"
        server_obj.save()
        return HttpResponseRedirect('/django.cgi/server')


@login_required
def site_detail(request):
    data = {}
    if request.method == 'POST':
        site_id = request.POST['site_id']
        comment = request.POST['memo']
        server_id = request.POST['server_id']
        site_comment_obj = SiteComment(
            site_id=site_id,
            comment=comment,
            created_at=datetime.now()
        )
        site_comment_obj.save()
    else:
        site_id = request.GET['site_id']
        server_id = request.GET['server_id']
    site = get_site_detail(site_id)
    for raw in site:
        data['site_id'] = raw[0]
        data['group_name'] = raw[1]
        data['site_title'] = raw[2]
        data['url'] = raw[3]
        data['japanese'] = raw[4]
        data['server'] = raw[5]
        data['login_id'] = raw[6]
        data['login_pass'] = raw[7]
        data['login_url'] = raw[8]
        data['remarks'] = raw[9]
        data['template'] = raw[10]
        data['updated_date'] = raw[11]
    comment = []
    site_comments = get_site_comment(site_id)
    for raw in site_comments:
        tmp = {}
        tmp['id'] = raw[0]
        tmp['site_id'] = raw[1]
        tmp['comment'] = raw[2]
        tmp['created_at'] = raw[3]
        comment.append(tmp)
    key = []
    keyword = Keywords.objects.filter(site_id=site_id).all()
    for row in keyword:
        tmp = {}
        tmp['keyword'] = row.keyword
        key.append(tmp)
    count = [x for x in range(1, 300)]
    result = {"data": data, "comment": comment, "site_id": site_id, 'method': 'site', 'keywords': key, 'count': count, 'server_id': server_id}
    return render(request, 'system/site_detail.html', result)


@login_required
def link(request, site_id):
    links = get_link_info(site_id)
    data = []
    children_data = []
    for i, link in enumerate(links):
        tmp = {}
        tmp['date'] = link[3]
        tmp['url'] = link[5]
        tmp['anchr'] = link[10]
        tmp['title'] = link[1]
        tmp['position'] = link[2]
        tmp['color'] = COLOR_LIST[i]
        data.append(tmp)
        children = get_link_info(link[9])
        for child in children:
            tmp_child = {}
            tmp_child['date'] = child[3]
            tmp_child['url'] = child[5]
            tmp_child['title'] = child[1]
            tmp_child['position'] = child[2]
            tmp_child['color'] = COLOR_LIST[i]
            children_data.append(tmp_child)
    check_list = []
    for r in data:
        if r['position'] not in check_list:
            check_list.append(r['position'])
    children_list = []
    for r in children_data:
        if r['position'] not in children_list:
            children_list.append(r['position'])
    result = {
        'data': data,
        'children': children_data,
        'check': check_list,
        'children_check': children_list,
    }
    return render(request, 'system/link.html', result)


def add_tree(top_id):
    top_objs = Link.objects.filter(to_id=top_id).all()
    result = []
    for top_obj in top_objs:
        tmp = {}
        tmp["name"] = "leaf"
        tmp["title"] = top_obj.site_title
        tmp["url"] = top_obj.url
        tmp["created_at"] = datetime.strftime(top_obj.created_at, "%Y-%m-%d")
        tmp["server"] = top_obj.server
        tmp["to_site"] = top_obj.to_site
        tmp["link_position"] = top_obj.link_position
        tmp["children"] = add_tree(top_obj.from_id)
        result.append(tmp)
    return result


@login_required
def create_server(request):
    if request.method == 'GET':
        next_year = datetime.today() + timedelta(days=365)
        day = datetime.strftime(next_year, '%Y-%m-%d')
        server = Setting_Server.objects.all()
        pay = Payment.objects.all()
        return render(request, 'system/create_server.html', {'next_year': day, 'server': server, 'pay': pay})
    elif request.method == 'POST':
        company = request.POST['company']
        host = request.POST['host']
        account = request.POST['account']
        ftp_pass = request.POST['ftp_pass']
        db_pass = request.POST['db_pass']
        login_id = request.POST['login_id']
        login_pass = request.POST['login_pass']
        login_url = request.POST['login_url']
        try:
            pay = request.POST['pay']
        except:
            pay = ""
        remark = request.POST['remark']
        update_at = request.POST['update_at']
        server_count = Server.objects.filter(server=company).count()
        if server_count > 0:
            server_company = company + '-' + str(server_count + 1)
        else:
            server_company = company
        server_obj = Server(
            server_company=server_company,
            server=company,
            updated_date=update_at,
            host=host,
            db_pass=db_pass,
            ftp_pass=ftp_pass,
            payment=pay,
            remarks=remark,
            username=account,
            login_url=login_url,
            login_id=login_id,
            login_pass=login_pass
        )
        server_obj.save()
        return HttpResponseRedirect('/django.cgi/server')


@login_required
def create_domain(request):
    if request.method == 'GET':
        next_year = datetime.today() + timedelta(days=365)
        day = datetime.strftime(next_year, '%Y-%m-%d')
        company = Setting_Domain.objects.all()
        server = Server.objects.all()
        return render(request, 'system/create_domain.html', {"next_year": day, "company": company, 'server': server})
    elif request.method == 'POST':
        domain = request.POST['domain']
        japanese = None
        if domain != '':
            if domain[:7] == 'http://':
                domain = domain[7:]
            japanese = url_pyu_quote('http://' + domain).encode('utf8')
            if japanese[:7] == 'http://':
                japanese = japanese[7:]
        else:
            japanese = request.POST['japanese']
            if japanese[:7] == 'http://':
                japanese = japanese[7:]
                domain = url_idna_quote('http://' + japanese)
            else:
                domain = url_idna_quote('http://' + japanese)
            if domain[:7] == 'http://':
                domain = domain[7:]
        try:
            company = request.POST['company']
        except:
            company = ""
        update_at = request.POST['update_at']
        update_method = request.POST['update_method']
        server = request.POST['server']
        if domain[:4] == "www.":
            domain = domain[4:]
        if japanese[:4] == "www.":
            japanese = japanese[4:]
        domain_obj = Domain(
            domain_name=domain,
            japanese=japanese,
            domain_company=company,
            updated_date=update_at,
            update_method=update_method,
            server_company=server
        )
        domain_obj.save()
        return HttpResponseRedirect('/django.cgi/domain')


@login_required
def create_site(request):
    if request.method == 'GET':
        try:
            domain_id = request.GET['domain_id']
        except:
            domain_id = -1
        server = Server.objects.all()
        group = Group.objects.all()
        template = Templates.objects.all()
        next_year = datetime.today() + timedelta(days=365)
        day = datetime.strftime(next_year, '%Y-%m-%d')
        return render(request, 'system/create_site.html', {'server': server, 'group': group, 'template': template, 'day': day, 'domain_id': domain_id})
    elif request.method == 'POST':
        domain_id = request.POST['domain_id']
        title = request.POST['title']
        url = request.POST['url']
        japanese = None
        if url != '':
            japanese = url_pyu_quote(url).encode('utf8')
        else:
            japanese = request.POST['japanese']
            url = url_idna_quote(japanese)
        try:
            group = request.POST['group']
        except:
            group = ""
        update_at = request.POST['update_at']
        try:
            template = request.POST['template']
        except:
            template = ""
        login_url = request.POST['login_url']
        login_id = request.POST['login_id']
        login_pass = request.POST['login_pass']
        remarks = request.POST['remarks']
        try:
            server = request.POST['server']
        except:
            server = ""
        domain_name = url.split('/')[2]
        if domain_name[:4] == "www.":
            domain_name = domain_name[4:]
        try:
            domain = Domain.objects.get(
                domain_name=domain_name
            )
        except:
            data = {
                'title': title,
                'url': url,
                'japanese': japanese,
                'group_name': group,
                'updated_date': update_at,
                'template': template,
                'login_id': login_id,
                'login_url': login_url,
                'login_pass': login_pass,
                'remarks': remarks,
                'domain_name': domain_name,
                'server': server
            }
            params = "?"
            for key, value in data.iteritems():
                if key == 'japanese':
                    value = urllib.quote_plus(value)
                params += key + '=' + value + '&'
            return redirect(reverse('system.views.domain_warning') + params[:-1])
        # server = domain.server_company
        if DomainDetail.objects.filter(domain_id=domain.id).count() == 0:
            domain_detail = DomainDetail(
                domain_id=domain.id,
                url=url,
                title=title,
                is_representative=True
            )
        else:
            domain_detail = DomainDetail(
                domain_id=domain.id,
                url=url,
                title=title,
                is_representative=False
            )
        domain_detail.save()
        site_obj = Site(
            site_title=title,
            url=url,
            japanese=japanese,
            group_name=group,
            server=server,
            updated_date=update_at,
            template=template,
            login_url=login_url,
            login_id=login_id,
            login_pass=login_pass,
            remarks=remarks
        )
        site_obj.save()
        if domain_id == -1:
            return HttpResponseRedirect('/django.cgi/domain/detail?domain_id=' + str(domain_id))
        else:
            return HttpResponseRedirect('/django.cgi/site')


@login_required
def domain_warning(request):
    if request.method == 'GET':
        title = request.GET['title']
        url = request.GET['url']
        japanese = request.GET['japanese']
        group_name = request.GET['group_name']
        updated_date = request.GET['updated_date']
        template = request.GET['template']
        login_id = request.GET['login_id']
        login_url = request.GET['login_url']
        login_pass = request.GET['login_pass']
        remarks = request.GET['remarks']
        domain_name = request.GET['domain_name']
        server = request.GET['server']
        japanese = urllib.unquote_plus(japanese)
        data = {
            'title': title,
            'url': url,
            'japanese': japanese,
            'group_name': group_name,
            'updated_date': updated_date,
            'tempalte': template,
            'login_id': login_id,
            'login_url': login_url,
            'login_pass': login_pass,
            'remarks': remarks,
            'domain_name': domain_name,
            'server_default': server
        }
        next_year = datetime.today() + timedelta(days=365)
        day = datetime.strftime(next_year, '%Y-%m-%d')
        company = Setting_Domain.objects.all()
        server = Server.objects.all()
        data['next_year'] = day
        data['company'] = company
        data['server'] = server
        japanese_domain = japanese.split('/')[2]
        if japanese_domain[:4] == "www.":
            japanese_domain = japanese_domain[4:]
        data['japanese_domain'] = japanese_domain
        return render(request, 'system/warning.html', data)
    elif request.method == 'POST':
        title = request.POST['title']
        url = request.POST['url']
        japanese = request.POST['japanese']
        group_name = request.POST['group_name']
        template = request.POST['template']
        login_id = request.POST['login_id']
        login_url = request.POST['login_url']
        login_pass = request.POST['login_pass']
        remarks = request.POST['remarks']
        domain_name = request.POST['domain_name']
        # ika
        domain = request.POST['domain']
        japanese_domain = request.POST['japanese_domain']
        try:
            company = request.POST['company']
        except:
            company = ""
        updated_date = request.POST['updated_date']
        update_method = request.POST['update_method']
        server = request.POST['server']
        if server == "new":
            server = ""
        domain_obj = Domain(
            domain_name=domain,
            japanese=japanese_domain,
            domain_company=company,
            updated_date=updated_date,
            update_method=update_method,
            server_company=server
        )
        domain_obj.save()
        if DomainDetail.objects.filter(domain_id=domain_obj.id).count() == 0:
            domain_detail = DomainDetail(
                domain_id=domain_obj.id,
                url=url,
                title=title,
                is_representative=True
            )
        else:
            domain_detail = DomainDetail(
                domain_id=domain_obj.id,
                url=url,
                title=title,
                is_representative=False
            )
        domain_detail.save()
        site_obj = Site(
            site_title=title,
            url=url,
            japanese=japanese,
            group_name=group_name,
            server=server,
            updated_date=updated_date,
            template=template,
            login_url=login_url,
            login_id=login_id,
            login_pass=login_pass,
            remarks=remarks
        )
        site_obj.save()
        return HttpResponseRedirect('/django.cgi/domain/detail?domain_id=' + str(domain_obj.id))


@login_required
def create_link(request):
    if request.method == 'GET':
        site_id = request.GET["site_id"]
        sites = Site.objects.get(id=site_id)
        raw_site_list = get_site_list()
        data = {}
        data["me"] = {"url": sites.url, "title": sites.site_title, "server": sites.server}
        data['site'] = []
        data['url'] = []
        today = datetime.today()
        data['day'] = datetime.strftime(today, '%Y-%m-%d')
        for i, site in enumerate(raw_site_list):
            data['site'].append({'num': i, 'site': site[0]})
            data['url'].append(site[1])
        position = Setting_Link.objects.all()
        data['position'] = position
        return render(request, 'system/create_link.html', data)
    elif request.method == 'POST':
        site_title = request.POST['site_title']
        url = request.POST['url']
        send_day = request.POST['send_day']
        link_url = request.POST['link_url']
        link_site = request.POST['link_site']
        link_pos = request.POST['link_pos']
        server = request.POST['server']
        anchr = request.POST['anchr']
        from_obj = Site.objects.get(url=url, site_title=site_title)
        from_id = from_obj.id
        to_obj = Site.objects.get(url=link_url, site_title=link_site)
        to_id = to_obj.id
        link_obj = Link(
            site_title=site_title,
            url=url,
            created_at=send_day,
            to_url=link_url,
            to_site=link_site,
            link_position=link_pos,
            server=server,
            from_id=from_id,
            to_id=to_id,
            anchr=anchr
        )
        link_obj.save()
        created_date = datetime.now()
        comment = link_site + ' ' + url + u'からリンクをもらう'
        obj = SiteComment(
            site_id=from_id,
            comment=comment,
            created_at=created_date
        )
        obj.save()
        url = reverse('link', kwargs={'site_id': from_id})
        return HttpResponseRedirect(url)


@login_required
def setting(request):
    return render(request, 'system/setting.html')


@login_required
def setting_templates(request):
    templates = Templates.objects.all()
    return render(request, 'system/setting_templates.html',{'templates' : templates})


@login_required
def setting_link(request):
    link = Setting_Link.objects.all()
    return render(request, 'system/setting_link.html',{'link' : link})


@login_required
def setting_group(request):
    group = Group.objects.all()
    return render(request, 'system/setting_group.html',{'group' : group})


@login_required
def setting_payment(request):
    payment = Payment.objects.all()
    return render(request, 'system/setting_payment.html',{'payment' : payment})


@login_required
def setting_domain(request):
    if request.method == 'POST':
        title = request.POST['title']
        url = request.POST['url']
        id = request.POST['id']
        password = request.POST['pass']
        obj = Setting_Domain(
            domain_company=title,
            login_url=url,
            login_id=id,
            login_pass=password,
        )
        obj.save()
    data = Setting_Domain.objects.all()
    return render(request, 'system/setting_domain.html', {'data': data})


@login_required
def setting_server(request):
    server = Setting_Server.objects.all()
    return render(request, 'system/setting_server.html',{'data': server})


@login_required
def create_setting_group(request):
    if request.method == 'GET':
        return render(request, 'system/create_setting_group.html')
    elif request.method == 'POST':
        group = request.POST['group']
        group_obj = Group(
            group=group
        )
        group_obj.save()
        return HttpResponseRedirect('/django.cgi/setting/group')


@login_required
def create_setting_server(request):
    if request.method == 'GET':
        return render(request, 'system/create_setting_server.html')
    elif request.method == 'POST':
        server_company = request.POST['server_company']
        login_url = request.POST['login_url']
        login_id = request.POST['login_id']
        login_pass = request.POST['login_pass']
        nameserver1 = request.POST['nameserver1']
        nameserver2 = request.POST['nameserver2']
        nameserver3 = request.POST['nameserver3']
        nameserver4 = request.POST['nameserver4']
        nameserver5 = request.POST['nameserver5']
        server_obj = Setting_Server(
            server_company = server_company,
            login_url = login_url,
            login_id = login_id,
            login_pass = login_pass,
            nameserver1 = nameserver1,
            nameserver2 = nameserver2,
            nameserver3 = nameserver3,
            nameserver4 = nameserver4,
            nameserver5 = nameserver5,
        )
        server_obj.save()
        return HttpResponseRedirect('/django.cgi/setting/server')


@login_required
def create_setting_domain(request):
    return render(request, 'system/create_setting_domain.html')


@login_required
def create_setting_payment(request):
    if request.method == 'GET':
        return render(request, 'system/create_setting_payment.html')
    elif request.method == 'POST':
        payment = request.POST['payment']
        payment_obj = Payment(
            payment = payment
        )
        payment_obj.save()
        return HttpResponseRedirect('/django.cgi/setting/payment')


@login_required
def create_setting_templates(request):
    if request.method == 'GET':
        return render(request, 'system/create_setting_templates.html')
    elif request.method == 'POST':
        templates = request.POST['templates']
        templates_obj = Templates(
            templates = templates
        )
        templates_obj.save()
        return HttpResponseRedirect('/django.cgi/setting/templates')


@login_required
def create_setting_link(request):
    if request.method == 'GET':
        return render(request, 'system/create_setting_link.html')
    elif request.method == 'POST':
        link = request.POST['link']
        link_obj = Setting_Link(
            link = link
        )
        link_obj.save()
        return HttpResponseRedirect('/django.cgi/setting/link')


@login_required
def delete(request):
    deleted_id = request.POST['id']
    if request.POST['kind'] == 'domain':
        obj = Domain.objects.filter(id=deleted_id)
        obj.delete()
        return redirect('system.views.domain_unup')
    elif request.POST['kind'] == 'server':
        obj = Server.objects.filter(id=deleted_id)
        obj.delete()
    elif request.POST['kind'] == 'set_domain':
        obj = Setting_Domain.objects.filter(id=deleted_id)
        obj.delete()
    elif request.POST['kind'] == 'set_group':
        obj = Group.objects.filter(id=deleted_id)
        obj.delete()
    elif request.POST['kind'] == 'link':
        obj = Link.objects.filter(id=deleted_id)
        obj.delete()
    elif request.POST['kind'] == 'payment':
        obj = Payment.objects.filter(id=deleted_id)
        obj.delete()
    elif request.POST['kind'] == 'set_server':
        obj = Setting_Server.objects.filter(id=deleted_id)
        obj.delete()
    elif request.POST['kind'] == 'template':
        obj = Templates.objects.filter(id=deleted_id)
        obj.delete()
    return redirect('system.views.server_unup')


@login_required
def delete_all(request):
    json_data = {
        "kind": request.GET['kind'],
        "id": request.GET['id']
    }
    if json_data['kind'] == 'domain':
        obj = Domain.objects.filter(id=json_data['id'])
        obj.delete()
    elif json_data['kind'] == 'server':
        obj = Server.objects.filter(id=json_data['id'])
        obj.delete()
    elif json_data['kind'] == 'set_domain':
        obj = Setting_Domain.objects.filter(id=json_data['id'])
        obj.delete()
    elif json_data['kind'] == 'set_group':
        obj = Group.objects.filter(id=json_data['id'])
        obj.delete()
    elif json_data['kind'] == 'link':
        obj = Setting_Link.objects.filter(id=json_data['id'])
        obj.delete()
    elif json_data['kind'] == 'payment':
        obj = Payment.objects.filter(id=json_data['id'])
        obj.delete()
    elif json_data['kind'] == 'set_server':
        obj = Setting_Server.objects.filter(id=json_data['id'])
        obj.delete()
    elif json_data['kind'] == 'template':
        obj = Templates.objects.filter(id=json_data['id'])
        obj.delete()
    return HttpResponse(json.dumps(json_data), content_type='application/json')


@login_required
def comment_delete(request):
    site_id = request.POST['site_id']
    comment_id = request.POST['comment_id']
    site_comment_obj = SiteComment.objects.filter(
        id=comment_id,
        site_id=site_id
    )
    site_comment_obj.delete()
    site = Site.objects.get(id=site_id)
    try:
        server_id = Server.objects.get(server=site.server).id
    except:
        server_id = -1
    redirect_url = '/django.cgi/site/detail?site_id=' + site_id + "&server_id=" + str(server_id)
    return HttpResponseRedirect(redirect_url)


@login_required
def comment_edit(request):
    if request.method == 'GET':
        comment = request.GET['comment']
        comment_id = request.GET['comment_id']
        site_id = request.GET['site_id']
        return render(
            request,
            'system/comment_edit.html',
            {'comment_id': comment_id, 'site_id': site_id, 'comment': comment}
        )
    elif request.method == 'POST':
        comment_id = request.POST['comment_id']
        site_id = request.POST['site_id']
        comment = request.POST['comment']
        created_at = datetime.now()
        SiteComment.objects.filter(
            id=comment_id,
            site_id=site_id
        ).update(comment=comment, created_at=created_at)
        site = Site.objects.get(id=site_id)
        try:
            server_id = Server.objects.get(server=site.server).id
        except:
            server_id = -1
        redirect_url = '/django.cgi/site/detail?site_id=' + site_id + "&server_id=" + str(server_id)
        return HttpResponseRedirect(redirect_url)


@login_required
def comment_all(request):
    site_id = request.GET['site_id']
    raw_comment_data = get_site_comment(site_id)
    comments = []
    for raw in raw_comment_data:
        tmp = {}
        tmp['id'] = raw[0]
        tmp['site_id'] = raw[1]
        tmp['comment'] = raw[2]
        tmp['created_at'] = raw[3]
        comments.append(tmp)
    result = {'comment': comments}
    return render(request, 'system/comment_all.html', result)


@login_required
def url_to_site(request):
    url = request.GET['url']
    site_names = raw_get_site_from_url(url)
    data = {}
    data['site'] = []
    for site_name in site_names:
        data['site'].append(site_name[0])
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def group_edit(request):
    if request.method == "GET":
        group_id = request.GET['group_id']
        group_obj = get_exact_group(group_id)
        group_a = {}
        for group in group_obj:
            group_a['group'] = group[1]
        data = {
            "group_id": group_id,
            "name": group_a["group"]
        }
        return render(request, 'system/edit_setting_group.html', data)
    elif request.method == "POST":
        group_id = request.POST['group_id']
        name = request.POST['group']
        Group.objects.filter(id=group_id).update(
            group=name
        )
        return redirect('system.views.setting_group')


@login_required
def templates_edit(request):
    if request.method == "GET":
        templates_id = request.GET['templates_id']
        templates_obj = get_exact_templates(templates_id)
        templates_a = {}
        for templates in templates_obj:
            templates_a['templates'] = templates[1]
        data = {
            "templates_id": templates_id,
            "name": templates_a["templates"]
        }
        return render(request, 'system/edit_setting_templates.html', data)
    elif request.method == "POST":
        templates_id = request.POST['templates_id']
        name = request.POST['templates']
        Templates.objects.filter(id=templates_id).update(
            templates=name
        )
        return redirect('system.views.setting_templates')


@login_required
def setting_link_edit(request):
    if request.method == "GET":
        link_id = request.GET['link_id']
        link_obj = get_exact_link(link_id)
        link_test = {}
        for link in link_obj:
            link_test['group'] = link[1]
        data = {
            "link_id": link_id,
            "name": link_test["group"]
        }
        return render(request, 'system/edit_setting_link.html', data)
    elif request.method == "POST":
        link_id = request.POST['link_id']
        name = request.POST['link']
        Setting_Link.objects.filter(id=link_id).update(
            link=name
        )
        return redirect('system.views.setting_link')


@login_required
def payment_edit(request):
    if request.method == "GET":
        payment_id = request.GET['payment_id']
        payment_obj = get_exact_payment(payment_id)
        payment_a = {}
        for payment in payment_obj:
            payment_a['payment'] = payment[1]
        data = {
            "payment_id": payment_id,
            "name": payment_a["payment"]
        }
        return render(request, 'system/edit_setting_payment.html', data)
    elif request.method == "POST":
        payment_id = request.POST['payment_id']
        name = request.POST['payment']
        Payment.objects.filter(id=payment_id).update(
            payment=name
        )
        return redirect('system.views.setting_payment')


@login_required
def setting_server_edit(request):
    if request.method == "GET":
        server_id = request.GET['server_id']
        server_obj = Setting_Server.objects.get(id=server_id)
        return render(request, 'system/edit_setting_server.html', {'data': server_obj})
    elif request.method == "POST":
        server_id = request.POST['server_id']
        Setting_Server.objects.filter(id=server_id).update(
            server_company=request.POST['server_company'],
            login_url=request.POST['login_url'],
            login_id=request.POST['login_id'],
            login_pass=request.POST['login_pass'],
            nameserver1=request.POST['nameserver1'],
            nameserver2=request.POST['nameserver2'],
            nameserver3=request.POST['nameserver3'],
            nameserver4=request.POST['nameserver4'],
            nameserver5=request.POST['nameserver5']
        )
        return HttpResponseRedirect('/django.cgi/setting/server')


def rank(request):
    site_id = request.GET['site_id']
    site = Site.objects.get(id=site_id)
    server_id = Server.objects.get(server_company=site.server).id
    data = Keywords.objects.filter(site_id=site_id).all()
    return render(request, 'system/rank.html', {'data': data, 'site_id': site_id, 'server_id':server_id})


def create_keyword(request):
    if request.method == 'GET':
        site_id = request.GET['site_id']
        return render(request, 'system/create_keyword.html', {'site_id': site_id})
    elif request.method == 'POST':
        site_id = request.POST['site_id']
        keyword = request.POST['keyword']
        created_date = datetime.now()
        obj = Keywords(
            site_id=int(site_id),
            keyword=keyword,
            created_date=created_date
        )
        obj.save()
        comment = u'キーワード:' + keyword + u'を追加しました。'
        obj = SiteComment(
            site_id=site_id,
            comment=comment,
            created_at=created_date
        )
        obj.save()
        redirect_url = '/django.cgi/keyword?site_id=' + str(site_id)
        return HttpResponseRedirect(redirect_url)


@login_required
def domain_edit(request):
    if request.method == "GET":
        domain_id = request.GET['domain_id']
        data = Setting_Domain.objects.get(id=domain_id)
        r = {}
        r['id'] = domain_id
        r['domain_company'] = data.domain_company
        r['login_id'] = data.login_id
        r['login_url'] = data.login_url
        r['login_pass'] = data.login_pass
        return render(request, 'system/edit_setting_domain.html', r)
    elif request.method == "POST":
        group_id = request.POST['domain_id']
        domain = request.POST['title']
        login_url = request.POST['url']
        login_id = request.POST['id']
        login_pass = request.POST['pass']
        obj = Setting_Domain.objects.get(id=group_id)
        obj.domain_company = domain
        obj.login_url = login_url
        obj.login_id = login_id
        obj.login_pass = login_pass
        obj.save()
        return redirect('system.views.setting_domain')


@login_required
def updomain(request):
    if request.method == 'GET':
        domain_id = request.GET['domain_id']
        domain = Domain.objects.get(id=domain_id)
        domain_day = domain.updated_date
        year_int = domain_day.year + 1
        year = '%d' % year_int
        if domain_day.month < 10:
            month = '0%d' % domain_day.month
        else:
            month = '%d' % domain_day.month
        if domain_day.day < 10:
            day = '0%d' % domain_day.day
        else:
            day = '%d' % domain_day.day
        server_company = request.GET['server']
        server = Server.objects.all()
        update_date = year + '-' + month + '-' + day
        return render(request, 'system/updomain.html', {'server': server, 'server_company': server_company, 'data': domain, 'date': update_date})
    elif request.method == 'POST':
        domain_id = request.POST['id']
        update_at = request.POST['update_at']
        server = request.POST['server']
        Domain.objects.filter(
            id=domain_id
        ).update(updated_date=update_at, server_company=server)
        redirect_url = '/django.cgi/domain/detail?domain_id=' + str(domain_id)
        return HttpResponseRedirect(redirect_url)


@login_required
def upserver(request):
    if request.method == 'GET':
        server_id = request.GET['server_id']
        server = Server.objects.get(id=server_id)
        server_day = server.updated_date
        year_int = server_day.year + 1
        year = '%d' % year_int
        if server_day.month < 10:
            month = '0%d' % server_day.month
        else:
            month = '%d' % server_day.month
        if server_day.day < 10:
            day = '0%d' % server_day.day
        else:
            day = '%d' % server_day.day
        update_date = year + '-' + month + '-' + day
        pay = Payment.objects.all()
        return render(request, 'system/upserver.html', {'data': server, 'date': update_date, 'pay': pay, 'server_id': server_id})
    elif request.method == 'POST':
        server_id = request.POST['server_id']
        host = request.POST['host']
        login_url = request.POST['login_url']
        login_id = request.POST['login_id']
        login_pass = request.POST['login_pass']
        account = request.POST['account']
        ftp_pass = request.POST['ftp_pass']
        db_pass = request.POST['db_pass']
        update_at = request.POST['update_at']
        pay = request.POST['pay']
        remarks = request.POST['remark']
        Server.objects.filter(id=server_id).update(
            login_url=login_url,
            login_id=login_id,
            host=host,
            login_pass=login_pass,
            username=account,
            ftp_pass=ftp_pass,
            db_pass=db_pass,
            updated_date=update_at,
            payment=pay,
            remarks=remarks,
        )
        redirect_url = '/django.cgi/server/detail?server_id=' + str(server_id)
        return HttpResponseRedirect(redirect_url)


@login_required
def site_delete(request):
    site_id = request.GET['site_id']
    obj = Site.objects.filter(id=site_id)
    url = obj.all()[:1].get()
    DomainDetail.objects.filter(url=url.url).delete()
    Link.objects.filter(from_id=site_id).delete()
    Link.objects.filter(to_id=site_id).delete()
    obj.delete()
    return HttpResponseRedirect('/django.cgi/site')


@login_required
def site_edit(request):
    if request.method == 'GET':
        site_id = request.GET['site_id']
        server_id = request.GET['server_id']
        obj = Site.objects.get(id=site_id)
        data = {}
        data['site_id'] = obj.id
        data['group_name'] = obj.group_name
        data['site_title'] = obj.site_title
        data['url'] = obj.url
        data['japanese'] = obj.japanese
        data['server'] = obj.server
        data['login_id'] = obj.login_id
        data['login_pass'] = obj.login_pass
        data['login_url'] = obj.login_url
        data['remarks'] = obj.remarks
        data['template'] = obj.template
        data['updated_date'] = datetime.strftime(obj.updated_date, '%Y-%m-%d')
        group = Group.objects.all()
        template = Templates.objects.all()
        server = Server.objects.all()
        return render(request, 'system/site_edit.html', {'data': data, 'group': group, 'template': template, 'server': server, 'server_id': server_id})
    elif request.method == 'POST':
        site_id = request.POST['site_id']
        server_id = request.POST['server_id']
        site = Site.objects.get(id=site_id)
        url = request.POST['url']
        japanese = request.POST['japanese']
        if request.POST['url'] != site.url:
            if japanese == site.japanese:
                if japanese[len(japanese) - 1] == '/':
                    japanese = japanese + request.POST['url'][len(site.url):]
                else:
                    japanese = japanese + '/' + request.POST['url'][len(site.url)-1:]
        elif japanese != site.japanese:
            if url == site.url:
                if url[len(url) - 1] == '/':
                    url = url + request.POST['japanese'][len(site.japanese):]
                else:
                    url = url + '/' + request.POST['japanese'][len(site.japanese)-1:]
        Site.objects.filter(id=site_id).update(
            url=url,
            group_name=request.POST['group'],
            japanese=japanese,
            server=request.POST['server'],
            login_url=request.POST['login_url'],
            login_id=request.POST['login_id'],
            login_pass=request.POST['login_pass'],
            remarks=request.POST['remarks'],
            template=request.POST['template'],
            updated_date=request.POST['update_at']
        )
        return HttpResponseRedirect('/django.cgi/site/detail?site_id=' + str(site_id) + '&server_id=' + str(server_id))


@login_required
def id_pass(request):
    server = request.GET['server']
    servers = Setting_Server.objects.filter(server_company=server).all()[:1].get()
    data = {}
    data['id'] = servers.login_id
    data['pass'] = servers.login_pass
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def site_key(request):
    if request.method == 'GET':
        site_id = request.GET['site_id']
        key = request.GET['key']
        Keywords.objects.filter(keyword=key).delete()
    elif request.method == 'POST':
        site_id = request.POST['site_id']
        key = request.POST['key']
        rank = request.POST['rank']
        comment = key + ':  ' + rank + u'位'
        site_comment_obj = SiteComment(
            site_id=site_id,
            comment=comment,
            created_at=datetime.now()
        )
        site_comment_obj.save()
    site = Site.objects.get(id=site_id)
    server_id = Server.objects.get(server=site.server).id
    return HttpResponseRedirect('/django.cgi/site/detail?site_id=' + str(site_id) + '&server_id=' + str(server_id))


@login_required
def delete_setting(request):
    deleted_id = request.GET['id']
    # if request.POST['kind'] == 'set_domain':
    #     obj = Setting_Domain.objects.filter(id=deleted_id)
    #     obj.delete()
    #     return redirect('system.views.setting_domain')
    # elif request.POST['kind'] == 'set_group':
    #     obj = Group.objects.filter(id=deleted_id)
    #     obj.delete()
    #     return redirect('system.views.setting_group')
    # elif request.POST['kind'] == 'link':
    #     obj = Setting_Link.objects.filter(id=deleted_id)
    #     obj.delete()
    #     return redirect('system.views.setting_link')
    # elif request.POST['kind'] == 'payment':
    #     obj = Payment.objects.filter(id=deleted_id)
    #     obj.delete()
    #     return redirect('system.views.setting_payment')
    # elif request.POST['kind'] == 'set_server':
    #     obj = Setting_Server.objects.filter(id=deleted_id)
    #     obj.delete()
    #     return redirect('system.views.setting_server')
    # elif request.POST['kind'] == 'template':
    #     obj = Templates.objects.filter(id=deleted_id)
    #     obj.delete()
    #     return redirect('system.views.setting_templates')
    if request.GET['kind'] == 'set_domain':
        obj = Setting_Domain.objects.filter(id=deleted_id)
        obj.delete()
        return redirect('system.views.setting_domain')
    elif request.GET['kind'] == 'set_group':
        obj = Group.objects.filter(id=deleted_id)
        obj.delete()
        return redirect('system.views.setting_group')
    elif request.GET['kind'] == 'link':
        obj = Setting_Link.objects.filter(id=deleted_id)
        obj.delete()
        return redirect('system.views.setting_link')
    elif request.GET['kind'] == 'payment':
        obj = Payment.objects.filter(id=deleted_id)
        obj.delete()
        return redirect('system.views.setting_payment')
    elif request.GET['kind'] == 'set_server':
        obj = Setting_Server.objects.filter(id=deleted_id)
        obj.delete()
        return redirect('system.views.setting_server')
    elif request.GET['kind'] == 'template':
        obj = Templates.objects.filter(id=deleted_id)
        obj.delete()
        return redirect('system.views.setting_templates')


@login_required
def site_to_url(request):
    site = request.GET['site']
    site_names = raw_get_url_from_site(site)
    data = {}
    data['url'] = []
    for site_name in site_names:
        data['url'].append(site_name[0])
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def delete_confirm(request):
    check_id = request.GET['check_id'][8:]
    kind = request.GET['kind']
    data = {
        'result': False,
        'reason': ""
    }
    if kind == 'templates':
        name = Templates.objects.get(id=check_id).templates
        if Site.objects.filter(template=name).count() != 0:
            data['result'] = 'yes'
            data['reason'] = 'site'
    elif kind == 'link':
        name = Setting_Link.objects.get(id=check_id).link
        if Link.objects.filter(link_position=name).count() != 0:
            data['result'] = 'yes'
            data['reason'] = 'link'
    elif kind == 'group':
        name = Group.objects.get(id=check_id).group
        if Site.objects.filter(group_name=name).count() != 0:
            data['result'] = 'yes'
            data['reason'] = 'site'
    elif kind == 'payment':
        name = Payment.objects.get(id=check_id).payment
        if Server.objects.filter(payment=name).count() != 0:
            data['result'] = 'yes'
            data['reason'] = 'server'
    elif kind == 'domain':
        name = Setting_Domain.objects.get(id=check_id).domain_company
        if Domain.objects.filter(domain_company=name).count() != 0:
            data['result'] = 'yes'
            data['reason'] = 'server'
    elif kind == 'server':
        name = Setting_Server.objects.get(id=check_id).server_company
        if Server.objects.filter(server=name).count() != 0:
            data['result'] = 'yes'
            data['reason'] = 'server'
    return HttpResponse(json.dumps(data), content_type='application/json')

@login_required
def get_login(request):
    server = request.GET['server']
    server_obj = Setting_Server.objects.get(server_company=server)
    data = {
        'login_url': server_obj.login_url,
        'login_id': server_obj.login_id,
        'login_pass': server_obj.login_pass,
    }
    return HttpResponse(json.dumps(data), content_type='application/json')
