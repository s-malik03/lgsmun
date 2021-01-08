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
    path('logout',views.logout,name='logout')
]
