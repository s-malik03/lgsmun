from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post_login',views.post_login,name='post_login')
]
