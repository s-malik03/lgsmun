from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Attendance,CommitteeControl,Notifications,GSL,RSL
from asgiref.sync import sync_to_async
import time

@sync_to_async
def essentialinfo(Committee):

    att=Attendance.objects.filter(committee=Committee).exclude(status="Absent").order_by('country')

    list=''

    for a in att:

        list=list+a.country+'('+a.placard+')'+'<br>'

    c=CommitteeControl.objects.get(committee=Committee)
    g=GSL.objects.filter(committee=Committee).order_by('date')
    r=RSL.objects.filter(committee=Committee).order_by('date')
    rsl=''
    gsl=''
    for r_ in r:
        rsl=rsl+r_.country+'<br>'
    for g_ in g:
        gsl=gsl+g_.country+'<br>'
    nlist=''
    try:
        n=Notifications.objects.filter(committee=Committee).order_by('-date')
        for n_ in n:

            nlist=nlist+'('+n_.date.strftime("%H:%M:%S")+')'+n_.country+':'+n_.message+'<br>'

    except Exception as e:

        nlist=str(e)

    if len(n)>10:
        n=n[:10]

    dict={

        'countrylist':list,
        'current_topic':c.topic,
        'speaking_mode':c.speaking_mode,
        'current_mod':c.current_mod,
        'notifications':nlist,
        'gsl':gsl,
        'rsl':rsl

    }

    return json.dumps(dict)

class Delegate(AsyncWebsocketConsumer):

    async def connect(self):

        await self.accept()

    async def receive(self,text_data):

        committee=text_data

        einfo=await essentialinfo(committee)

        await self.send(einfo)
