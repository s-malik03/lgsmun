from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from login.models import User

#general

def index(request):

    return HttpResponse("hi")

def logout(request):

    try:

        att=Attendance.objects.get(committee=request.session['committee'],country=request.session['country'])

        att.status='Absent'

        att.save()

    except:

        pass

    return redirect('/login')

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

        list=list+a.country+'('+a.placard+')'+'<br>'

    return HttpResponse(list)

def getattendance(request):

    att=Attendance.objects.filter(committee=request.session['committee']).exclude(status="Absent").order_by('country')

    list=''

    for a in att:

        list=list+a.country+' | '+a.status+' | Recognized: '+str(a.recognized)+' | '+a.placard+'<br>\n'

    return HttpResponse(list)

#GSL

def add_to_gsl(Committee,Country):

    g=GSL(country=Country,committee=Committee)
    g.save()
    return ""

def remove_from_gsl(Committee):

    try:

        g=GSL.objects.filter(committee=Committee).order_by('date')
        g[0].delete()

    except:

        pass

    return ""

#RSL

def add_to_rsl(Committee,Country):

    r=RSL(country=Country,committee=Committee)
    r.save()
    return ""

def remove_from_rsl(Committee):

    try:

        r=RSL.objects.filter(committee=Committee).order_by('date')
        r[0].delete()

    except:

        pass

    return ""

def remove_speaker(request):

    C=CommitteeControl.objects.get(committee=request.session['committee'])

    if C.speaking_mode=='GSL':

        remove_from_gsl(request.session['committee'])

    if C.speaking_mode=='Mod':

        remove_from_rsl(request.session['committee'])

    return HttpResponse('Successful')

def add_speaker(request):

    C=CommitteeControl.objects.get(committee=request.session['committee'])

    if C.speaking_mode=='GSL':

        add_to_gsl(request.session['committee'],request.POST['country'])

    if C.speaking_mode=='Mod':

        add_to_rsl(request.session['committee'],request.POST['country'])

    return HttpResponse('Successful')

#MOD

def set_current_mod(request):

    c=CommitteeControl.objects.get(committee=request.session['committee'])
    c.current_mod=request.POST["current_mod"]
    c.save()
    return HttpResponse("Successful")

def remove_current_mod(request):

    c=CommitteeControl.objects.get(committee=request.session['committee'])
    c.current_mod="No Moderated Caucus in Progress"
    c.save()
    return HttpResponse("Successful")

#voting

def vote(request):

    if request.GET['vote']=='Abstain':

        att=Attendance.objects.get(country=request.session['country'],committee=request.session['committee'])

        if 'Voting' in att.status:

            return HttpResponse("You are marked Present and Voting, therefore you cannot abstain.")

    v=Vote.objects.filter(committee=request.session['committee'],country=request.session['country'])

    if not(v.exists()):

        v=Vote(committee=request.session['committee'],country=request.session['country'],vote_status=request.GET['vote'])
        v.save()

    return HttpResponse("Thank you for voting")

#timer

def timer(request):

    request_context={}
    return render(request,'timer.html',request_context)

def start_timer(request):

    t=Timer.objects.get(committee=request.session['committee'])
    t.status='start'
    t.save()
    return HttpResponse("Successful")

def pause_timer(request):

    t=Timer.objects.get(committee=request.session['committee'])
    t.status='pause'
    t.save()
    return HttpResponse("Successful")

def stop_timer(request):

    t=Timer.objects.get(committee=request.session['committee'])
    t.status='stop'
    t.save()
    return HttpResponse("Successful")

def reset_total(request):
    t=Timer.objects.get(committee=request.session['committee'])
    t.total_time=0
    t.save()
    return HttpResponse("Successful")

def set_total_time(request):
    t=Timer.objects.get(committee=request.session['committee'])
    t.total_time=int(request.POST['duration'])
    t.save()
    return HttpResponse("Successful")

def set_speaker_time(request):
    t=Timer.objects.get(committee=request.session['committee'])
    t.duration=int(request.POST['duration'])
    t.save()
    return HttpResponse("Successful")

#DAIS

def speaking_mode(request):

    sm=CommitteeControl.objects.get(committee=request.session['committee'])
    sm.speaking_mode=request.POST["speaking_mode"]
    sm.save()
    return HttpResponse("Successful")

def set_current_topic(request):

    c=CommitteeControl.objects.get(committee=request.session['committee'])
    c.topic=request.POST["topic"]
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

def dais(request):

    if request.session['utype']!='dais' and request.session['utype']!='admin':
        return HttpResponse('Access Denied')
    request_context={'committee':request.session['committee'],'country':request.session['country']}
    return render(request,'dais.html',request_context)

#DELEGATE

def get_current_topic(request):

    c=CommitteeControl.objects.get(committee=request.session['committee'])
    return HttpResponse(c.topic)

def get_speaking_mode(request):

    c=CommitteeControl.objects.get(committee=request.session['committee'])
    return HttpResponse(c.speaking_mode)

def get_current_mod(request):

    c=CommitteeControl.objects.get(committee=request.session['committee'])
    return HttpResponse(c.current_mod)

def delegate(request):

    if request.session['utype']!='delegate':

        return HttpResponse("Access Denied")

    request_context={'committee':request.session['committee'],'country':request.session['country']}
    return render(request,'delegate.html',request_context)

def raise_placard(request):

    att=Attendance.objects.get(country=request.session['country'])
    att.placard="Placard Raised"
    att.save()
    return HttpResponse("Successful")

def lower_placard(request):

    att=Attendance.objects.get(country=request.session['country'])
    att.placard=""
    att.save()
    return HttpResponse("Successful")

def send_notification(request):

    n=Notifications(country=request.session['country'],committee=request.session['committee'],message=request.POST['notification'])
    n.save()
    return HttpResponse("Successful")

def send_message(request):

    if len(request.POST['message'])>0:
        inbox=Messages(committee=request.session['committee'],sender=request.session['country'],recipient=request.POST['recipient'],message=request.POST['message'])
        inbox.save()
    return HttpResponse("Successful")













# Create your views here.
