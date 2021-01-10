from channels.generic.websocket import WebsocketConsumer
import json
from .models import Attendance

class GetCountryList(WebsocketConsumer):

    def connect(self):

        self.accept()
