from django.urls import path

from . import views

urlpatterns = [
    path('login', views.index, name='login'),
    path('post_login',views.post_login,name='post_login'),
    path('create_user',views.create_user,name='create_user'),
    path('register',views.register,name='register'),
    path('', views.homepage, name='homepage')
]
