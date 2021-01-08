from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from login.models import User

def index(request):

    return HttpResponse("hi")

def timer(request):

    request_context={}
    return render(request,'timer.html',request_context)

def rollcall(request):

    if request.session['utype']!='delegate':

        return HttpResponse('Access Denied')

    request_context={'committee':request.session['committee']}
    return render(request,'rollcall.html',request_context)

def markattendance(request):

    if request.session['utype']!='delegate':

        return HttpResponse('Access Denied')

    try:

        att=Attendance.objects.get(country=request.session['country'],committee=request.session['committee'])

    except:

        att=Attendance(country=request.session['country'],committee=request.session['committee'])

    att.status=request.GET['status']
    att.save()

    return redirect('delegate')

def delegate(request):

    return HttpResponse("")

# Create your views here.
