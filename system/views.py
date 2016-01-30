#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta

from system.models import(
    Domain,
    Server,
    Site,
    DomainDetail
)

from system.aggregate import(
    get_domain_info,
    get_server_info,
    get_site_info,
    get_special_domain,
    get_domain_detail,
    get_special_server
)


@login_required
def home(request):
    data = {'domain': [], 'server': []}
    raw_domain_datas = get_domain_info()
    for domain_data in raw_domain_datas:
        tmp = {}
        tmp['domain'] = domain_data[1]
        tmp['japanese'] = domain_data[2]
        tmp['updated_at'] = domain_data[3]
        tmp['company'] = domain_data[4]
        data['domain'].append(tmp)
    raw_server_datas = get_server_info()
    for server_data in raw_server_datas:
        tmp = {}
        tmp['company'] = server_data[1]
        tmp['updated_at'] = server_data[2]
        tmp['host'] = server_data[3]
        data['server'].append(tmp)
    result = {'data': data}
    return render(request, 'system/index.html', result)


@login_required
def server(request):
    data = []
    raw_server_datas = get_server_info()
    for server_data in raw_server_datas:
        if server_data[11] != "not_update":
            tmp = {}
            tmp['id'] = server_data[0]
            tmp['company'] = server_data[1]
            tmp['updated_at'] = server_data[2]
            tmp['host'] = server_data[3]
            data.append(tmp)
    result = {'data': data}
    return render(request, 'system/server.html', result)


@login_required
def site(request):
    data = []
    raw_site_datas = get_site_info()
    for site_data in raw_site_datas:
        tmp = {}
        tmp['id'] = site_data[0]
        tmp['title'] = site_data[2]
        tmp['url'] = site_data[3]
        tmp['group'] = site_data[1]
        tmp['japanese'] = site_data[4]
        tmp['server'] = site_data[5]
        data.append(tmp)
    result = {'data': data}
    return render(request, 'system/site.html', result)


@login_required
def domain(request):
    data = []
    raw_domain_datas = get_domain_info()
    for domain_data in raw_domain_datas:
        if domain_data[6] != "not_update":
            try:
                tmp = {}
                tmp['id'] = domain_data[0]
                tmp['domain'] = domain_data[1]
                tmp['japanese'] = domain_data[2]
                tmp['updated_at'] = domain_data[3]
                tmp['company'] = domain_data[4]
                tmp['company_url'] = domain_data[5]
                domaindetail = DomainDetail.objects.get(
                    domain_id=domain_data[0],
                    is_representative=True
                )
                tmp['representative'] = domaindetail.url
                data.append(tmp)
            except:
                tmp = {}
                tmp['id'] = domain_data[0]
                tmp['domain'] = domain_data[1]
                tmp['japanese'] = domain_data[2]
                tmp['updated_at'] = domain_data[3]
                tmp['company'] = domain_data[4]
                tmp['company_url'] = domain_data[5]
                tmp['representative'] = "not selected"
                data.append(tmp)
    result = {'data': data}
    return render(request, 'system/domain.html', result)


@login_required
def server_unup(request):
    if request.method == "POST":
        update_id = request.POST['id']
        Server.objects.filter(id=update_id).update(update_method="not_update")
    data = []
    raw_server_datas = get_server_info()
    for server_data in raw_server_datas:
        if server_data[11] == "not_update":
            tmp = {}
            tmp['id'] = server_data[0]
            tmp['company'] = server_data[1]
            tmp['updated_at'] = server_data[2]
            tmp['host'] = server_data[3]
            data.append(tmp)
    result = {'data': data}
    return render(request, 'system/server_unup.html', result)


@login_required
def domain_unup(request):
    if request.method == "POST":
        update_id = request.POST['id']
        Domain.objects.filter(id=update_id).update(update_method="not_update")
    data = []
    raw_domain_datas = get_domain_info()
    for domain_data in raw_domain_datas:
        if domain_data[6] == "not_update":
            tmp = {}
            tmp['id'] = domain_data[0]
            tmp['domain'] = domain_data[1]
            tmp['japanese'] = domain_data[2]
            tmp['updated_at'] = domain_data[3]
            tmp['company'] = domain_data[4]
            data.append(tmp)
    result = {'data': data}
    return render(request, 'system/domain_unup.html', result)


@login_required
def domain_detail(request):
    if request.method == 'POST':
        domain_id = request.POST['domain_id']
        representative = DomainDetail.objects.get(
            domain_id=domain_id,
            is_representative=True
        )
        representative.is_representative = False
        representative.save()
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
            data['updated_at'] = raw[3]
            data['company'] = raw[4]
        for detail in details:
            tmp = {}
            tmp['id'] = detail[0]
            tmp['domain_id'] = detail[1]
            tmp['url'] = detail[2]
            tmp['title'] = detail[3]
            tmp['is_represetative'] = detail[4]
            data['detail'].append(tmp)
        result = {'data': data}
        return render(request, 'system/domain_detail.html', result)
    elif request.method == 'GET':
        data = {'detail': []}
        domain_id = request.GET['domain_id']
        domain = get_special_domain(domain_id)
        details = get_domain_detail(domain_id)
        for raw in domain:
            data['domain'] = raw[1]
            data['updated_at'] = raw[3]
            data['company'] = raw[4]
        for detail in details:
            tmp = {}
            tmp['id'] = detail[0]
            tmp['domain_id'] = detail[1]
            tmp['url'] = detail[2]
            tmp['title'] = detail[3]
            tmp['is_represetative'] = detail[4]
            data['detail'].append(tmp)
        result = {'data': data}
        return render(request, 'system/domain_detail.html', result)


@login_required
def server_detail(request):
    data = {}
    server_id = request.GET['server_id']
    server = get_special_server(server_id)
    for raw in server:
        data['server'] = raw[1]
        data['update_at'] = raw[2]
        data['host'] = raw[3]
        data['username'] = raw[4]
        data['ftp_pass'] = raw[5]
        data['db_pass'] = raw[6]
        data['payment'] = raw[7]
        data['remarks'] = raw[8]
        data['login_id'] = raw[9]
        data['login_pass'] = raw[10]
    result = {'data': data}
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
    return render(request, 'system/site_detail.html')


@login_required
def link(request):
    return render(request, 'system/link.html')


@login_required
def create_server(request):
    if request.method == 'GET':
        next_year = datetime.today() + timedelta(days=365)
        day = datetime.strftime(next_year, '%Y-%m-%d')
        return render(request, 'system/create_server.html', {'next_year': day})
    elif request.method == 'POST':
        company = request.POST['company']
        host = request.POST['host']
        company = request.POST['company']
        login_id = request.POST['id']
        login_pass = request.POST['pass']
        account = request.POST['account']
        ftp_pass = request.POST['ftp_pass']
        db_pass = request.POST['db_pass']
        pay = request.POST['pay']
        remark = request.POST['remark']
        update_at = request.POST['update_at']
        server_obj = Server(
            server_company=company,
            updated_date=update_at,
            host=host,
            db_pass=db_pass,
            ftp_pass=ftp_pass,
            payment=pay,
            remarks=remark,
            username=account,
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
        return render(request, 'system/create_domain.html', {"next_year": day})
    elif request.method == 'POST':
        domain = request.POST['domain']
        japanese = request.POST['japanese']
        company = request.POST['company']
        update_at = request.POST['update_at']
        update_method = request.POST['update_method']
        domain_obj = Domain(
            domain_name=domain,
            japanese=japanese,
            domain_company=company,
            updated_date=update_at,
            update_method=update_method
        )
        domain_obj.save()
        return HttpResponseRedirect('/django.cgi/domain')


@login_required
def create_site(request):
    if request.method == 'GET':
        return render(request, 'system/create_site.html')
    elif request.method == 'POST':
        title = request.POST['title']
        url = request.POST['url']
        japanese = request.POST['japanese']
        group = request.POST['group']
        update_at = request.POST['update_at']
        template = request.POST['template']
        login_url = request.POST['login_url']
        login_id = request.POST['login_id']
        login_pass = request.POST['login_pass']
        remarks = request.POST['remarks']
        site_obj = Site(
            site_title=title,
            url=url,
            japanese=japanese,
            group=group,
            updated_date=update_at,
            template=template,
            login_url=login_url,
            login_id=login_id,
            login_pass=login_pass,
            remarks=remarks
        )
        site_obj.save()
        try:
            domain_name = url.split('/')[2]
            domain = Domain.objects.get(domain_name=domain_name)
            domain_detail = DomainDetail(
                domain_id=domain.id,
                url=url,
                title=title,
                is_representative=False
            )
            domain_detail.save()
        except:
            return redirect(reverse('system.views.domain_warning'))
        return HttpResponseRedirect('/django.cgi/site')


@login_required
def domain_warning(request):
    data = {'message': 'There is something wrong with domain names'}
    return render(request, 'system/warning.html', data)


@login_required
def create_link(request):
    return render(request, 'system/create_link.html')


@login_required
def setting(request):
    return render(request, 'system/setting.html')


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
    return HttpResponse(json.dumps(json_data), content_type='application/json')
