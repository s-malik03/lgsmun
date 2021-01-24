from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Attendance,CommitteeControl,Notifications,GSL,RSL,Timer,Messages,FloorMods
from asgiref.sync import sync_to_async
import time
from django.db.models import Q
from login.models import User

@sync_to_async

def u_auth(Committee,Country,UUID):

    if UUID=='none':

        return False

    try:

        u=User.objects.get(committee=Committee,country=Country,uuid=UUID)

    except:

        return False

    return True

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

            plcrd=a.placard

            if plcrd=="Placard Raised":

                plcrd=' <span class="dot"></span>'

            list=list+'<div class="btn">'+a.country+plcrd+'</div>'

    except:

        pass

    c=CommitteeControl.objects.get(committee=Committee)
    t=Timer.objects.get(committee=Committee)

    try:
        g=GSL.objects.filter(committee=Committee).order_by('date')
        r=RSL.objects.filter(committee=Committee).order_by('date')

        for r_ in r:
            rsl=rsl+'<div class="btn">'+r_.country+'</div>'
        for g_ in g:
            gsl=gsl+'<div class="btn">'+g_.country+'</div>'

    except:

        pass

    nlist=''
    try:
        n=Notifications.objects.filter(committee=Committee).order_by('-date')
        for n_ in n:

            nlist=nlist+'('+n_.date.strftime("%H:%M:%S")+')'+n_.country+':'+n_.message+'<br>'

    except Exception as e:

        pass

    modlist=''
    mnum=1

    try:

        m=FloorMods.objects.filter(committee=Committee).order_by('date')

        for mod in m:

            modlist=modlist+str(mnum)+'. '+mod.mod+'<br>'
            mnum=mnum+1

    except:

        pass

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
        'inbox':inbox_text,
        'mods':modlist

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

            plcrd=a.placard

            if plcrd=="Placard Raised":

                plcrd='<span class="dot"></span>'

            list=list+'<div class="btn">'+a.country+' | '+a.status+' | Recognized: '+str(a.recognized)+' | '+plcrd+'</div>\n'

    except:

        pass

    c=CommitteeControl.objects.get(committee=Committee)
    t=Timer.objects.get(committee=Committee)

    try:
        g=GSL.objects.filter(committee=Committee).order_by('date')
        r=RSL.objects.filter(committee=Committee).order_by('date')

        for r_ in r:
            rsl=rsl+'<div class="btn">'+r_.country+'</div>'
        for g_ in g:
            gsl=gsl+'<div class="btn">'+g_.country+'</div>'


    except:

        pass

    nlist=''
    try:
        n=Notifications.objects.filter(committee=Committee).order_by('-date')

        for n_ in n:

            nlist=nlist+'('+n_.date.strftime("%H:%M:%S")+')'+n_.country+':'+n_.message+'<br>'

    except Exception as e:

        pass

    modlist=''
    mnum=1

    try:

        m=FloorMods.objects.filter(committee=Committee).order_by('date')

        for mod in m:

            modlist=modlist+str(mnum)+'. '+mod.mod+'<br>'
            mnum=mnum+1

    except:

        pass

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
        'inbox':inbox_text,
        'mods':modlist

    }

    return json.dumps(dict)

class Delegate(AsyncWebsocketConsumer):

    async def connect(self):

        await self.accept()

    async def receive(self,text_data):

        json_data=json.loads(text_data)

        uuid=json_data['uuid']

        committee=json_data['committee']

        country=json_data['country']

        if not(await u_auth(committee,country,uuid)):

            await self.close()

        einfo=await essentialinfo(committee,country)

        await self.send(einfo)

class Dais(AsyncWebsocketConsumer):

    async def connect(self):

        await self.accept()

    async def receive(self,text_data):

        json_data=json.loads(text_data)

        uuid=json_data['uuid']

        committee=json_data['committee']

        country=json_data['country']

        if not(await u_auth(committee,country,uuid)):

            await self.close()

        einfo=await essentialinfo_dais(committee,country)

        await self.send(einfo)
