from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('timer',views.timer,name='timer'),
    path('rollcall',views.rollcall,name='rollcall'),
    path('markattendance',views.markattendance,name='markattendance'),
    path('delegate',views.delegate,name='delegate'),
    path('getattendance',views.getattendance,name='getattendance'),
    path('getcountrylist',views.getcountrylist,name='getcountrylist'),
    path('logout',views.logout,name='logout'),
    path('add_to_gsl',views.add_to_gsl,name='add_to_gsl'),
    path('set_current_mod',views.set_current_mod,name='set_current_mod'),
    path('speaking_mode',views.speaking_mode,name='speaking_mode'),
    path('set_current_topic',views.set_current_topic,name='speaking_mode'),
    path('enable_motions',views.enable_motions,name='enable_motions'),
    path('disable_motions',views.disable_motions,name='disable_motions'),
    path('raise_placard',views.raise_placard,name='raise_placard'),
    path('lower_placard',views.lower_placard,name='lower_placard'),
    path('get_current_mod',views.get_current_mod,name='get_current_mod'),
    path('get_current_topic',views.get_current_topic,name='get_current_topic'),
    path('get_speaking_mode',views.get_speaking_mode,name='get_speaking_mode'),
    path('raise_motion',views.raise_motion,name='raise_motion'),
    path('send_message',views.send_message,name='send_message')

]
