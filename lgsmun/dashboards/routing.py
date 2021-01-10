from django.urls import path
from .consumers import *

ws_urlpatterns = [

    path('ws/getcountrylist/',GetCountryList.as_asgi())

]
