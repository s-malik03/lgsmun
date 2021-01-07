from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import RequestContext
from .models import User
from hashlib import sha256

# Create your views here.

def index(request):

    request_context={}
    return render(request,'login/login.html',request_context)

def post_login(request):

    request_context={}

    if request.method=="POST":

        uinfo=request.POST

        try:

            uinfo=User.objects.get(email=request.POST["email"])

        except:

            return HttpResponse("invalid email or password")

        password=uinfo.password

        if password==sha256(request.POST["password"].encode('utf-8')).hexdigest():

            request.session['uid']=uinfo.email
            request.session['committee']=uinfo.committee
            if uinfo.role=='admin':
                request.session['utype']='admin'
                return redirect('/menu/admin')
            elif uinfo.role=='dais':
                request.session['utype']='dais'
                return redirect('/menu/dais')
            else:
                request.session['utype']='delegate'
                return redirect('/menu/delegate')

        else:

            return HttpResponse('invalid email or password')
