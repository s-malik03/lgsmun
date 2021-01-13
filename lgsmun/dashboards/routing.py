from django.urls import path
from .consumers import *

ws_urlpatterns = [

    path('ws/delegate/',Delegate.as_asgi()),
    path('ws/dais/',Dais.as_asgi())

]
