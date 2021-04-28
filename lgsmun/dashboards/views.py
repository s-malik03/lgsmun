from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
# from lgsmun.login.models import UserInformation
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# general


def index(request):
    return HttpResponse("hi")


@login_required
def set_zoom_link(request):
    c = CommitteeControl.objects.get(committee=request.session['committee'])
    c.zoom_link = request.POST['zoom_link']
    c.save()
    return HttpResponse("Successful")


@login_required
def set_drive_link(request):
    c = CommitteeControl.objects.get(committee=request.session['committee'])
    c.drive_link = request.POST['drive_link']
    c.save()
    return HttpResponse("Successful")


@login_required
def merge_form(request):
    committees = CommitteeControl.objects.values('committee')
    committee_matrix = []

    for c in committees:
        committee_matrix.append(c['committee'])

    request_context = {'committees': committee_matrix}
    return render(request, 'merge.html', request_context)


@login_required
def unmerge_form(request):
    committees = CommitteeControl.objects.values('committee')
    committee_matrix = []

    for c in committees:
        committee_matrix.append(c['committee'])

    request_context = {'committees': committee_matrix}
    return render(request, 'merge.html', request_context)


@login_required
def merge(request):
    committee1 = request.GET['committee1']
    committee2 = request.GET['committee2']
    new_committee = request.GET['new_committee']
    users = User.objects.filter(Q(committee=committee1) | Q(committee=committee2))

    for u in users:
        u.old_committee = u.committee
        u.committee = new_committee
        u.save()

    return HttpResponse('Successful')


@login_required
def unmerge(request):
    committee = request.GET['committee']
    users = UserCommittee.objects.filter(committee=committee)

    for u in users:
        u.committee = u.old_committee
        u.save()

    return HttpResponse('Successful')


@login_required
def logout(request):
    try:

        att = Attendance.objects.get(committee=request.session['committee'], country=request.session['country'])

        att.status = 'Absent'

        att.save()

    except:

        pass

    uinfo = User.objects.get(email=request.session['uid'])

    uinfo.uuid = 'none'

    uinfo.save()

    return redirect('/')


# attendance
@login_required
def hub(request):
    if request.session['utype'] != 'delegate':
        return HttpResponse('Access Denied')

    current_user = request.user

    try:

        committees = UserCommittee.objects.filter(user=current_user)

    except:

        request_context = {'committees': []}
        return render(request, 'hub.html', request_context)

    committee_info = []

    for c in committees:
        committee_info.append(c.committee)

    request_context = {'committees': committee_info}
    return render(request, 'hub.html', request_context)


@login_required
def markattendance(request):
    request.session['committee'] = request.GET['committee']
    user = request.user
    committee_info = UserCommittee.objects.get(user=user)
    request.session['country'] = committee_info.country
    if request.session['utype'] != 'delegate':
        return HttpResponse('Access Denied')

    try:

        att = Attendance.objects.get(country=request.session['country'], committee=request.session['committee'])

    except:

        att = Attendance(country=request.session['country'], committee=request.session['committee'])

    att.status = 'Present'
    att.save()

    c = CommitteeControl.objects.get(committee=request.session['committee'])

    return redirect('delegate')


@login_required
def getcountrylist(request):
    att = Attendance.objects.filter(committee=request.session['committee']).exclude(status="Absent").order_by('country')

    list = ''

    for a in att:
        list = list + a.country + '(' + a.placard + ')' + '<br>'

    return HttpResponse(list)


@login_required
def getattendance(request):
    att = Attendance.objects.filter(committee=request.session['committee']).exclude(status="Absent").order_by('country')

    list = ''

    for a in att:
        list = list + a.country + ' | ' + a.status + ' | Recognized: ' + str(
            a.recognized) + ' | ' + a.placard + '<br>\n'

    return HttpResponse(list)


# GSL
@login_required
def add_to_gsl(Committee, Country):
    g = GSL(country=Country, committee=Committee)
    g.save()
    return ""


@login_required
def remove_from_gsl(Committee):
    try:

        g = GSL.objects.filter(committee=Committee).order_by('date')
        g[0].delete()

    except:

        pass

    return ""


# RSL
@login_required
def add_to_rsl(Committee, Country):
    r = RSL(country=Country, committee=Committee)
    r.save()
    return ""


@login_required
def remove_from_rsl(Committee):
    try:

        r = RSL.objects.filter(committee=Committee).order_by('date')
        r[0].delete()

    except:

        pass

    return ""


@login_required
def remove_speaker(request):
    C = CommitteeControl.objects.get(committee=request.session['committee'])

    if C.speaking_mode == 'GSL':
        remove_from_gsl(request.session['committee'])

    if C.speaking_mode == 'Mod':
        remove_from_rsl(request.session['committee'])

    return HttpResponse('Successful')


@login_required
def add_speaker(request):
    C = CommitteeControl.objects.get(committee=request.session['committee'])
    recog = Attendance.objects.get(committee=request.session['committee'], country=request.POST['country'])
    recog.recognized = recog.recognized + 1
    recog.save()

    if C.speaking_mode == 'GSL':
        add_to_gsl(request.session['committee'], request.POST['country'])

    if C.speaking_mode == 'Mod':
        add_to_rsl(request.session['committee'], request.POST['country'])

    return HttpResponse('Successful')


# MOD
@login_required
def set_current_mod(request):
    c = CommitteeControl.objects.get(committee=request.session['committee'])
    r = RSL.objects.filter(committee=request.session['committee'])
    r.delete()
    c.current_mod = request.POST["current_mod"]
    c.save()
    return HttpResponse("Successful")


@login_required
def remove_current_mod(request):
    c = CommitteeControl.objects.get(committee=request.session['committee'])
    c.current_mod = "No Moderated Caucus in Progress"
    c.save()
    return HttpResponse("Successful")


# voting
@login_required
def vote(request):
    if request.GET['vote'] == 'Abstain':

        att = Attendance.objects.get(country=request.session['country'], committee=request.session['committee'])

        if 'Voting' in att.status:
            return HttpResponse("You are marked Present and Voting, therefore you cannot abstain.")

    v = Vote.objects.filter(committee=request.session['committee'], country=request.session['country'])

    if not (v.exists()):
        v = Vote(committee=request.session['committee'], country=request.session['country'],
                 vote_status=request.GET['vote'])
        v.save()

    return HttpResponse("Thank you for voting")


# timer
@login_required
def timer(request):
    request_context = {}
    return render(request, 'timer.html', request_context)


@login_required
def start_timer(request):
    t = Timer.objects.get(committee=request.session['committee'])
    t.status = 'start'
    t.save()
    return HttpResponse("Successful")


@login_required
def pause_timer(request):
    t = Timer.objects.get(committee=request.session['committee'])
    t.status = 'pause'
    t.save()
    return HttpResponse("Successful")


@login_required
def stop_timer(request):
    t = Timer.objects.get(committee=request.session['committee'])
    t.status = 'stop'
    t.save()
    return HttpResponse("Successful")


@login_required
def reset_total(request):
    t = Timer.objects.get(committee=request.session['committee'])
    t.total_time = 0
    t.save()
    return HttpResponse("Successful")


@login_required
def set_total_time(request):
    t = Timer.objects.get(committee=request.session['committee'])
    t.total_time = int(request.POST['duration'])
    t.save()
    return HttpResponse("Successful")


@login_required
def set_speaker_time(request):
    t = Timer.objects.get(committee=request.session['committee'])
    t.duration = int(request.POST['duration'])
    t.save()
    return HttpResponse("Successful")


# DAIS
@login_required
def speaking_mode(request):
    sm = CommitteeControl.objects.get(committee=request.session['committee'])
    sm.speaking_mode = request.POST["speaking_mode"]
    sm.save()
    return HttpResponse("Successful")


@login_required
def set_current_topic(request):
    c = CommitteeControl.objects.get(committee=request.session['committee'])
    c.topic = request.POST["topic"]
    c.save()
    return HttpResponse("Successful")


@login_required
def enable_motions(request):
    c = CommitteeControl.objects.get(committee=request.session['committee'])
    c.allow_motions = True
    c.save()
    return HttpResponse("Successful")


@login_required
def disable_motions(request):
    c = CommitteeControl.objects.get(committee=request.session['committee'])
    c.allow_motions = False
    c.save()
    return HttpResponse("Successful")


@login_required
def dais(request):
    if request.session['utype'] != 'dais' and request.session['utype'] != 'admin':
        return HttpResponse('Access Denied')

    country_matrix = []

    try:

        countries = User.objects.filter(committee=request.session['committee']).exclude(country='Dais').order_by(
            'country').values('country').distinct()
        for c in countries:
            country_matrix.append(c['country'])

    except:

        pass

    request_context = {'committee': request.session['committee'], 'country': request.session['country'],
                       'country_matrix': country_matrix, 'uuid': request.session['uuid']}
    if request.session['utype'] == 'admin':
        return render(request, 'admin.html', request_context)
    return render(request, 'dais.html', request_context)


# DELEGATE
@login_required
def get_current_topic(request):
    c = CommitteeControl.objects.get(committee=request.session['committee'])
    return HttpResponse(c.topic)


@login_required
def get_speaking_mode(request):
    c = CommitteeControl.objects.get(committee=request.session['committee'])
    return HttpResponse(c.speaking_mode)


@login_required
def get_current_mod(request):
    c = CommitteeControl.objects.get(committee=request.session['committee'])
    return HttpResponse(c.current_mod)


@login_required
def delegate(request):
    if request.session['utype'] != 'delegate':
        return HttpResponse("Access Denied")

    country_matrix = ['Dais']

    try:

        countries = User.objects.filter(committee=request.session['committee']).exclude(country='Dais').order_by(
            'country').values('country').distinct()
        for c in countries:
            country_matrix.append(c['country'])

    except:

        pass

    request_context = {'committee': request.session['committee'], 'country': request.session['country'],
                       'country_matrix': country_matrix, 'uuid': 'none'}
    return render(request, 'delegate.html', request_context)


def unraise_all_placard(request):
    att = Attendance.objects.filter(committee=request.session['committee'])

    for a in att:
        a.placard = ''
        a.save()

    return HttpResponse("Successful")


def raise_placard(request):
    att = Attendance.objects.get(country=request.session['country'], committee=request.session['committee'])
    att.placard = "Placard Raised"
    att.save()
    return HttpResponse("Successful")


def lower_placard(request):
    att = Attendance.objects.get(country=request.session['country'], committee=request.session['committee'])
    att.placard = ""
    att.save()
    return HttpResponse("Successful")


def send_notification(request):
    if request.session['country'] == 'Dais':

        msg = '<b>' + request.POST['notification'] + '</b>'
        n = Notifications(country=request.session['country'], committee=request.session['committee'], message=msg)
        n.save()

    elif not (('<' in request.POST['notification']) and ('>' in request.POST['notification'])):

        n = Notifications(country=request.session['country'], committee=request.session['committee'],
                          message=request.POST['notification'])
        n.save()
    return HttpResponse("Successful")


def send_message(request):
    if not (('<' in request.POST['message']) and ('>' in request.POST['message'])):

        if len(request.POST['message']) > 0:
            inbox = Messages(committee=request.session['committee'], sender=request.session['country'],
                             recipient=request.POST['recipient'], message=request.POST['message'])
            inbox.save()
    return HttpResponse("Successful")


def chat_log(request):
    inbox = Messages.objects.filter(committee=request.session['committee']).order_by('date')

    backlog = ''

    for i in inbox:
        backlog = backlog + i.date.strftime(
            "%H:%M:%S") + '(' + i.sender + ' to ' + i.recipient + ')' + i.message + '<br>'

    return HttpResponse(backlog)


def committee_log(request):
    notis = Notifications.objects.filter(committee=request.session['committee']).order_by('date')

    nlist = ''

    for n_ in notis:
        nlist = nlist + '(' + n_.date.strftime("%H:%M:%S") + ')' + n_.country + ':' + n_.message + '<br>'

    return HttpResponse(nlist)


def add_mod(request):
    mod = FloorMods(mod=request.POST["mod"], committee=request.session["committee"])
    mod.save()
    return HttpResponse("Successful")


def remove_mod(request):
    try:

        mod = FloorMods.objects.filter(committee=request.session["committee"]).order_by('date')

        num = int(request.POST["modnum"])

        mod[num - 1].delete()

    except:

        pass

    return HttpResponse("Successful")


def clear_mod(request):
    try:

        mod = FloorMods.objects.filter(committee=request.session["committee"])

        mod.delete()

    except:

        pass

    return HttpResponse("Successful")

# Create your views here.
