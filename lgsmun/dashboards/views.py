from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from login.models import User

#general

def index(request):

    return HttpResponse("hi")

def logout(request):

    att=Attendance.objects.get(committee=request.session['committee'],country=request.session['country'])

    att.status='Absent'

    att.save()

    return HttpResponse("Logged Out Successfully")

#attendance

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

def getattendance(request):

    att=Attendance.objects.filter(committee=request.session['committee']).exclude(status="Absent").order_by('country')

    list=''

    for a in att:

        list=list+a.country+' | '+a.status+' | Recognized: '+str(a.recognized)+'<br>\n'

    return HttpResponse(list)

#GSL

def add_to_gsl(request):

    g=GSL(country=request.GET['country'],committee=request.session['committee'])
    g.save()
    return HttpResponse("Successful")

def remove_from_gsl(request):

    g=GSL.objects.filter(country=request.GET['country']).order_by('-date')
    g[0].delete()
    return HttpResponse("Successful")

#MOD

def set_current_mod(request):

    c=CommitteeControl.objects.get(committee=request.session['committee'])
    c.current_mod=request.GET["current_mod"]
    c.save()
    return HttpResponse("Successful")

#timer

def timer(request):

    request_context={}
    return render(request,'timer.html',request_context)

#DAIS

def speaking_mode(request):

    sm=CommitteeControl.objects.get(committee=request.session['committee'])
    sm.speaking_mode=request.GET["speaking_mode"]
    sm.save()
    return HttpResponse("Successful")

def set_current_topic(request):

    c=CommitteeControl.objects.get(committee=request.session['committee'])
    c.topic=request.GET["topic"]
    c.save()
    return HttpResponse("Successful")

def enable_motions(request):

    c=CommitteeControl.objects.get(committee=request.session['committee'])
    c.allow_motions=True
    c.save()
    return HttpResponse("Successful")

def disable_motions(request):

    c=CommitteeControl.objects.get(committee=request.session['committee'])
    c.allow_motions=False
    c.save()
    return HttpResponse("Successful")

#DELEGATE

def delegate(request):

    return HttpResponse("")













# Create your views here.
