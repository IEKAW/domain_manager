from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def create(request):
    data = {"error_msg": ""}
    if request.method == 'GET':
        return render(request, 'accounts/create.html', data)
    elif request.method == 'POST':
        try:
            name = request.POST['name']
            e_mail = request.POST['e_mail']
            password = request.POST['password']
            if len(name) < 1 or len(password) < 1:
                data['error_msg'] = "name or password is empty"
                return render(request, 'accounts/create.html', data)
            if User.objects.filter(username=name):
                data['error_msg'] = "this account is already exist"
                return render(request, 'accounts/create.html', data)
            user = User.objects.create_user(name, e_mail, password)
            user.save()
            login(request, authenticate(username=name, password=password))
            return HttpResponseRedirect('/')
        except:
            data['error_msg'] = "something went wrong"
            return render(request, 'accounts/create.html', data)
