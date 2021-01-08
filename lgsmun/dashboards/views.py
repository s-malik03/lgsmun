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

def getcountrylist(request):

    att=Attendance.objects.filter(committee=request.session['committee']).exclude(status="Absent").order_by('country')

    list=''

    for a in att:

        list=list+a.country+'<br>'

    return HttpResponse(list)

def logout(request):

    att=Attendance.objects.get(committee=request.session['committee'],country=request.session['country'])

    att.status='Absent'

    att.save()

    return HttpResponse("Logged Out Successfully")

def getattendance(request):

    att=Attendance.objects.filter(committee=request.session['committee']).exclude(status="Absent").order_by('country')

    list=''

    for a in att:

        list=list+a.country+' | '+a.status+' | Recognized: '+str(a.recognized)+'<br>\n'

    return HttpResponse(list)

def delegate(request):

    return HttpResponse("")

# Create your views here.
