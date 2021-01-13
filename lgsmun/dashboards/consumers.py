from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Attendance,CommitteeControl,Notifications,GSL,RSL,Timer,Messages
from asgiref.sync import sync_to_async
import time
from django.db.models import Q

@sync_to_async
def essentialinfo(Committee,Country):

    inbox_text=''
    rsl=''
    gsl=''
    list=''
    try:

        inbox=Messages.objects.filter(Q(committee=Committee),Q(recipient=Country)|Q(sender=Country))

        for i in inbox:

            inbox_text=inbox_text+'('+i.sender+' to '+i.recipient+')'+i.message+'<br>'

    except:

        pass

    try:

        att=Attendance.objects.filter(committee=Committee).exclude(status="Absent").order_by('country')

        for a in att:

            list=list+a.country+'('+a.placard+')'+'<br>'

    except:

        pass

    c=CommitteeControl.objects.get(committee=Committee)
    t=Timer.objects.get(committee=Committee)

    try:
        g=GSL.objects.filter(committee=Committee).order_by('date')
        r=RSL.objects.filter(committee=Committee).order_by('date')

        for r_ in r:
            rsl=rsl+r_.country+'<br>'
        for g_ in g:
            gsl=gsl+g_.country+'<br>'

    except:

        pass

    nlist=''
    try:
        n=Notifications.objects.filter(committee=Committee).order_by('-date')
        if len(n)>10:
            n=n[:10]
        for n_ in n:

            nlist=nlist+'('+n_.date.strftime("%H:%M:%S")+')'+n_.country+':'+n_.message+'<br>'

    except Exception as e:

        nlist=str(e)

    dict={

        'countrylist':list,
        'current_topic':c.topic,
        'speaking_mode':c.speaking_mode,
        'current_mod':c.current_mod,
        'notifications':nlist,
        'gsl':gsl,
        'rsl':rsl,
        'timer_status':t.status,
        'timer_duration':t.duration,
        'total_time':t.total_time,
        'inbox':inbox_text

    }

    return json.dumps(dict)

@sync_to_async

def essentialinfo_dais(Committee,Country):

    inbox_text=''
    rsl=''
    gsl=''
    list=''
    try:

        inbox=Messages.objects.filter(Q(committee=Committee),Q(recipient=Country)|Q(sender=Country))

        for i in inbox:

            inbox_text=inbox_text+'('+i.sender+' to '+i.recipient+')'+i.message+'<br>'

    except:

        pass

    try:

        att=Attendance.objects.filter(committee=Committee).exclude(status="Absent").order_by('country')

        for a in att:

            list=list+a.country+' | '+a.status+' | Recognized: '+str(a.recognized)+' | '+a.placard+'<br>\n'

    except:

        pass

    c=CommitteeControl.objects.get(committee=Committee)
    t=Timer.objects.get(committee=Committee)

    try:
        g=GSL.objects.filter(committee=Committee).order_by('date')
        r=RSL.objects.filter(committee=Committee).order_by('date')

        for r_ in r:
            rsl=rsl+r_.country+'<br>'
        for g_ in g:
            gsl=gsl+g_.country+'<br>'

    except:

        pass

    nlist=''
    try:
        n=Notifications.objects.filter(committee=Committee).order_by('-date')
        if len(n)>10:
            n=n[:10]
        for n_ in n:

            nlist=nlist+'('+n_.date.strftime("%H:%M:%S")+')'+n_.country+':'+n_.message+'<br>'

    except Exception as e:

        nlist=str(e)

    dict={

        'countrylist':list,
        'current_topic':c.topic,
        'speaking_mode':c.speaking_mode,
        'current_mod':c.current_mod,
        'notifications':nlist,
        'gsl':gsl,
        'rsl':rsl,
        'timer_status':t.status,
        'timer_duration':t.duration,
        'total_time':t.total_time,
        'inbox':inbox_text

    }

    return json.dumps(dict)

class Delegate(AsyncWebsocketConsumer):

    async def connect(self):

        await self.accept()

    async def receive(self,text_data):

        json_data=json.loads(text_data)

        committee=json_data['committee']

        country=json_data['country']

        einfo=await essentialinfo(committee,country)

        await self.send(einfo)

class Dais(AsyncWebsocketConsumer):

    async def connect(self):

        await self.accept()

    async def receive(self,text_data):

        json_data=json.loads(text_data)

        committee=json_data['committee']

        country=json_data['country']

        einfo=await essentialinfo_dais(committee,country)

        await self.send(einfo)
