from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Attendance, CommitteeControl, Notifications, GSL, RSL, Timer, Messages, FloorMods
from asgiref.sync import sync_to_async
import time
from django.db.models import Q


@sync_to_async
def essentialinfo(Committee, Country):
    inbox_text = ''
    rsl = ''
    gsl = ''
    list = ''
    try:

        inbox = Messages.objects.filter(Q(committee=Committee), Q(recipient=Country) | Q(sender=Country))

        for i in inbox:
            inbox_text = inbox_text + '(' + i.sender + ' to ' + i.recipient + ')' + i.message + '<br>'

    except:

        pass

    try:

        att = Attendance.objects.filter(committee=Committee).exclude(status="Absent").order_by('country')

        for a in att:

            plcrd = a.placard

            if plcrd == "Placard Raised":
                plcrd = ' <span class="dot"></span>'

            list = list + '<div class="btn">' + a.country + plcrd + '</div>'

    except:

        pass

    c = CommitteeControl.objects.get(committee=Committee)
    t = Timer.objects.get(committee=Committee)

    try:
        g = GSL.objects.filter(committee=Committee).order_by('date')
        r = RSL.objects.filter(committee=Committee).order_by('date')

        for r_ in r:
            rsl = rsl + '<div class="btn">' + r_.country + '</div>'
        for g_ in g:
            gsl = gsl + '<div class="btn">' + g_.country + '</div>'

    except:

        pass

    nlist = ''
    try:
        n = Notifications.objects.filter(committee=Committee).order_by('-date')
        for n_ in n:
            nlist = nlist + '(' + n_.date.strftime("%H:%M:%S") + ')' + n_.country + ':' + n_.message + '<br>'

    except Exception as e:

        pass

    modlist = ''
    mnum = 1

    try:

        m = FloorMods.objects.filter(committee=Committee).order_by('date')

        for mod in m:
            modlist = modlist + str(mnum) + '. ' + mod.mod + '<br>'
            mnum = mnum + 1

    except:

        pass

    dict = {

        'countrylist': list,
        'current_topic': c.topic,
        'speaking_mode': c.speaking_mode,
        'current_mod': c.current_mod,
        'notifications': nlist,
        'gsl': gsl,
        'rsl': rsl,
        'timer_status': t.status,
        'timer_duration': t.duration,
        'total_time': t.total_time,
        'inbox': inbox_text,
        'mods': modlist,
        'zoom_link': c.zoom_link,
        'drive_link': c.drive_link,
        'iteration': c.iteration

    }

    return json.dumps(dict)


@sync_to_async
def essentialinfo_dais(Committee, Country):
    inbox_text = ''
    rsl = ''
    gsl = ''
    list = ''
    try:

        inbox = Messages.objects.filter(Q(committee=Committee), Q(recipient=Country) | Q(sender=Country))

        for i in inbox:
            inbox_text = inbox_text + '(' + i.sender + ' to ' + i.recipient + ')' + i.message + '<br>'

    except:

        pass

    try:

        att = Attendance.objects.filter(committee=Committee).exclude(status="Absent").order_by('country').order_by(
            '-placard')

        for a in att:

            plcrd = a.placard

            if plcrd == "Placard Raised":

                plcrd = '<span class="dot"></span>'

            else:

                plcrd = ''

            list = list + '<div class="btn">' + a.country + ' | ' + a.status + ' | Recognized: ' + str(
                a.recognized) + ' | ' + plcrd + '</div>\n'

    except:

        pass

    c = CommitteeControl.objects.get(committee=Committee)
    t = Timer.objects.get(committee=Committee)

    try:
        g = GSL.objects.filter(committee=Committee).order_by('date')
        r = RSL.objects.filter(committee=Committee).order_by('date')

        for r_ in r:
            rsl = rsl + '<div class="btn">' + r_.country + '</div>'
        for g_ in g:
            gsl = gsl + '<div class="btn">' + g_.country + '</div>'


    except:

        pass

    nlist = ''
    try:
        n = Notifications.objects.filter(committee=Committee).order_by('-date')

        for n_ in n:
            nlist = nlist + '(' + n_.date.strftime("%H:%M:%S") + ')' + n_.country + ':' + n_.message + '<br>'

    except Exception as e:

        pass

    modlist = ''
    mnum = 1

    try:

        m = FloorMods.objects.filter(committee=Committee).order_by('date')

        for mod in m:
            modlist = modlist + str(mnum) + '. ' + mod.mod + '<br>'
            mnum = mnum + 1

    except:

        pass

    dict = {

        'countrylist': list,
        'current_topic': c.topic,
        'speaking_mode': c.speaking_mode,
        'current_mod': c.current_mod,
        'notifications': nlist,
        'gsl': gsl,
        'rsl': rsl,
        'timer_status': t.status,
        'timer_duration': t.duration,
        'total_time': t.total_time,
        'inbox': inbox_text,
        'mods': modlist,
        'zoom_link': c.zoom_link,
        'drive_link': c.drive_link,
        'iteration': c.iteration

    }

    return json.dumps(dict)


@sync_to_async
def check_iteration(committee, iteration):
    committee_iteration = CommitteeControl.objects.get(committee=committee).iteration

    if committee_iteration == iteration:

        return False

    else:

        return True


@sync_to_async
def two_cent_time(committee, total_time, speaker_time):

    timer = Timer.objects.get(committee=committee)

    offset_total = int(timer.total_time) - int(total_time)

    offset_speaker = int(timer.duration) - int(speaker_time)

    if 1 <= offset_total < 5:
        timer.total_time = total_time

    if 1 <= offset_speaker < 5:
        timer.duration = speaker_time

    timer.save()

    return 0


@sync_to_async
def goabsent(committee, country):

    att = Attendance.objects.get(country=country, committee=committee)

    att.status = 'Absent'

    c = CommitteeControl.objects.get(committee=committee)

    c.iteration += 1

    att.save()

    c.save()

    return 0


class Delegate(AsyncWebsocketConsumer):

    async def connect(self):

        await self.accept()

    async def receive(self, text_data):

        json_data = json.loads(text_data)

        iteration = int(json_data['iteration'])

        committee = json_data['committee']

        country = json_data['country']

        self.country = country

        self.committee = committee

        total_time = json_data['total_time']

        speaker_time = json_data['speaker_time']

        tct = await two_cent_time(committee, total_time, speaker_time)

        iter_test = await check_iteration(committee, iteration)

        if iter_test:

            einfo = await essentialinfo(committee, country)

            await self.send(einfo)

        else:

            self.send("NULL")

    async def disconnect(self, code):

        g = await goabsent(self.committee, self.country)


class Dais(AsyncWebsocketConsumer):

    async def connect(self):

        await self.accept()

    async def receive(self, text_data):

        json_data = json.loads(text_data)

        iteration = int(json_data['iteration'])

        committee = json_data['committee']

        country = json_data['country']

        total_time = json_data['total_time']

        speaker_time = json_data['speaker_time']

        tct = await two_cent_time(committee, total_time, speaker_time)

        iter_test = await check_iteration(committee, iteration)

        if iter_test:

            einfo = await essentialinfo(committee, country)

            await self.send(einfo)

        else:

            self.send("NULL")
