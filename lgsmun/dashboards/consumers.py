from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Attendance,CommitteeControl
from asgiref.sync import sync_to_async
import time

@sync_to_async
def essentialinfo(Committee):

    att=Attendance.objects.filter(committee=Committee).exclude(status="Absent").order_by('country')

    list=''

    for a in att:

        list=list+a.country+'('+a.placard+')'+'<br>'

    c=CommitteeControl.objects.get(committee=Committee)

    dict={

        'countrylist':list,
        'current_topic':c.topic,
        'speaking_mode':c.speaking_mode,
        'current_mod':c.current_mod

    }

    return json.dumps(dict)

class Delegate(AsyncWebsocketConsumer):

    async def connect(self):

        await self.accept()

    async def receive(self,text_data):

        committee=text_data

        einfo=await essentialinfo(committee)

        await self.send(einfo)
