from django.urls import path

from . import views

urlpatterns = [
    path('admin', views.admin, name='admin'),
    path('dais', views.dais, name='dais'),
    path('delegate', views.delegate, name='delegate'),
    path('changepassword', views.changepassword, name='changepassword'),
    path('adminjoinsession', views.adminjoinsession, name='adminjoinsession'),
    path('joinsession', views.joinsession, name='joinsession'),
    path('setpassword', views.setpassword, name='setpassword'),
]
