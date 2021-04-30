from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserInformation
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User


# Create your views here.

def signout(request):
    logout(request)

    return redirect('/')


def homepage(request):
    if request.user.is_authenticated:

        uinfo = UserInformation.objects.get(user=request.user)
        if uinfo.role == 'admin':
            request.session['utype'] = 'admin'
            return redirect('/menu/admin')
        elif uinfo.role == 'dais':
            request.session['utype'] = 'dais'
            return redirect('/menu/dais')
        else:
            request.session['utype'] = 'delegate'
            return redirect('/menu/delegate')

    else:

        return redirect('login')

    return HttpResponse('')


def index(request):
    request_context = {'invalid': ' '}
    return render(request, 'login/login.html', request_context)


def register(request):
    request_context = {'username_taken': ' '}
    return render(request, 'login/register.html', request_context)


def create_user(request):
    try:

        User.objects.get(username=request.POST['username'])
        return render(request, 'login/register.html', {'username_taken': 'This username is already taken!'})

    except User.DoesNotExist:

        user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'],
                                        password=request.POST['password'])
        user.save()
        additional_information = UserInformation(user=user, role='delegate',
                                                 mobile=request.POST['mobile'],
                                                 grade=request.POST['grade'],
                                                 school=request.POST['school'])
        additional_information.save()
        return redirect('login')


def post_login(request):
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

    if user is not None:

        login(request, user)
        uinfo = UserInformation.objects.get(user=user)
        if uinfo.role == 'admin':
            request.session['utype'] = 'admin'
            return redirect('/menu/admin')
        elif uinfo.role == 'dais':
            request.session['utype'] = 'dais'
            return redirect('/menu/dais')
        else:
            request.session['utype'] = 'delegate'
            return redirect('/menu/delegate')

    else:

        return render(request, 'login/login.html', {'invalid': 'Invalid Username or Password'})
