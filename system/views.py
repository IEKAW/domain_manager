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
