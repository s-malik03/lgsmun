from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserInformation
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import string
import random
from django.core.mail import send_mail
import datetime
from pytz import timezone

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

        if not request.POST['username']:

            return render(request, 'login/register.html', {'username_taken': 'Please provide a username!'})

        elif len(request.POST['password'])<8:

            return render(request, 'login/register.html',
                          {'username_taken': 'You must provide a password of at least 8 characters!'})

        elif request.POST['password'] != request.POST['confirm_password']:

            return render(request, 'login/register.html',
                          {'username_taken': 'Passwords do not match!'})

        elif not request.POST['email']:

            return render(request, 'login/register.html', {'username_taken': 'Please provide a valid E-mail address.'})

        elif not request.POST['mobile']:

            return render(request, 'login/register.html', {'username_taken': 'Please provide a valid mobile number!'})

        elif not request.POST['grade']:

            return render(request, 'login/register.html', {'username_taken': 'Please provide your current grade!'})

        elif not request.POST['school']:

            return render(request, 'login/register.html', {'username_taken': 'Please provide the name of your institution!'})

        user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'],
                                        password=request.POST['password'])
        user.save()
        additional_information = UserInformation(user=user, role='delegate',
                                                 mobile=request.POST['mobile'],
                                                 grade=request.POST['grade'],
                                                 school=request.POST['school'])
        vcode = ''

        for i in range(12):

            vcode += random.choice(string.ascii_letters)

        additional_information.verification_code = vcode
        additional_information.save()

        send_mail('Thank you for registering on LGSMUN!',
                  recipient_list=[request.POST['email']],
                  fail_silently=True,
                  from_email='lgsesports@gmail.com',
                  message='Dear ' +
                               request.POST['username'] +
                               ",\nWelcome to the LGSMUN debate portal. Your password is: \n" +
                               request.POST['password'] +
                               "\nTo complete your registration please click on the link below to verify your account\n" +
                               '127.0.0.1:8000/verify/'+vcode
                  )

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


def verify(request, vcode):

    try:

        user = UserInformation.objects.get(verification_code=vcode)
        user.verified = True
        user.save()
        return HttpResponse("Verified!")

    except:

        return HttpResponse("Unable to Verify Account!")


def remove_unverified(request):

    users = UserInformation.objects.filter(verified=False)
    for u in users:
        tz = timezone('Asia/Karachi')
        current_time = tz.localize(datetime.datetime.now())
        time_diff = current_time - u.date_created
        days = time_diff.days
        if days >= 1:
            u.user.delete()
            u.delete()
    return HttpResponse('Successful')
