from django.shortcuts import render
from django.http import HttpResponse
from .models import User
from hashlib import sha256

# Create your views here.

def index(request):

    return render(request,'login/login.html')

def post_login(request):

    if request.method=="POST":

        info=request.POST

        try:

            password=User.objects.get(email=request.POST["email"])

        except:

            return HttpResponse("invalid email or password")

        password=password.password

        if password==sha256(request.POST["password"].encode('utf-8')).hexdigest():

            return HttpResponse('nice')

        else:

            return HttpResponse('invalid email or password')
