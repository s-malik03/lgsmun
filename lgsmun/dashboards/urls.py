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
    path('disable_motions',views.disable_motions,name='disable_motions')

]
