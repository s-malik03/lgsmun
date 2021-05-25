from django.urls import path

from . import views

urlpatterns = [
    path('login', views.index, name='login'),
    path('post_login', views.post_login, name='post_login'),
    path('create_user', views.create_user, name='create_user'),
    path('register', views.register, name='register'),
    path('routetodestination', views.homepage, name='homepage'),
    path('', views.home, name='home'),
    path('signout', views.signout, name='signout'),
    path('verify/<str:vcode>', views.verify, name='verify'),
    path('remove_unverified', views.remove_unverified, name='remove_unverified')
]
