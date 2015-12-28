#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, 'system/index.html')


@login_required
def server(request):
    return render(request, 'system/server.html')


@login_required
def site(request):
    return render(request, 'system/site.html')


@login_required
def domain(request):
    return render(request, 'system/domain.html')


@login_required
def server_unup(request):
    return render(request, 'system/server_unup.html')


@login_required
def domain_unup(request):
    return render(request, 'system/domain_unup.html')


@login_required
def domain_detail(request):
    return render(request, 'system/domain_detail.html')


@login_required
def server_detail(request):
    return render(request, 'system/server_detail.html')


@login_required
def update_domain(request):
    return render(request, 'system/update_domain.html')


@login_required
def update_server(request):
    return render(request, 'system/update_server.html')


@login_required
def site_detail(request):
    return render(request, 'system/site_detail.html')


@login_required
def link(request):
    return render(request, 'system/link.html')


@login_required
def create_server(request):
    return render(request, 'system/create_server.html')


@login_required
def create_domain(request):
    return render(request, 'system/create_domain.html')


@login_required
def create_site(request):
    return render(request, 'system/create_site.html')


@login_required
def create_link(request):
    return render(request, 'system/create_link.html')


@login_required
def setting(request):
    return render(request, 'system/setting.html')
